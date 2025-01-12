from flask import Flask,flash , render_template, request , url_for , redirect , session
from flask_session import Session
import pandas as pd
import numpy as np 
from flaskext.mysql import MySQL  
from content import content                                

app = Flask(__name__) 
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.config['SECRET_KEY'] = 'secret!' 

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'test'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
mysql.init_app(app)

def update(stars,id) :
    print("update stars",stars)
    print("course name",id)
    data = pd.read_csv("Coursera.csv")

    df = data[['index','name','num_votes','sum_rating']].values.tolist()
    for index,name,num_votes,rating in df:
        if(name == id):
            update_votes = num_votes+1
            update_sum_rating = rating + int(stars)
            z = index
    print(data.loc[z])
    update_rating = round(update_sum_rating/update_votes,2)

    print(z,round(update_sum_rating/update_votes,2))
    data.loc[z, 'rating'] = update_rating
    data.to_csv("Coursera.csv", index=False)
    data.loc[z, 'num_votes'] = update_votes
    data.to_csv("Coursera.csv", index=False)
    data.loc[z, 'sum_rating'] = update_sum_rating
    data.to_csv("Coursera.csv", index=False)
    print(data.loc[z])
    return "Successfully updated dataset"

def check(id) :
    stars = request.form.get('star')
    print(stars)
    temp = request.args.get('home')
    session["id"] = id
    if temp != None :
        session["id"] = temp
    print(session["id"])

    my_course = content.content_based(session["id"])

    collab = []

    if stars != None:
        update_dataset = update(stars,session["id"])
        print(update_dataset)
        try :
            def get_similar(c_name, rating):
                similar_ratings = x[c_name] * (rating - 2.5)
                similar_ratings = similar_ratings.sort_values(ascending=False)
                return similar_ratings

            stars = int(stars)

            x = pd.read_csv('dummy.csv', index_col=[0])
            # x = x.corr(method='pearson')
            print("collab session id",session["id"])
            selected_course = [(session["id"], stars)]
            compare = session["id"]

            similar_courses = pd.DataFrame()
            for c_name, rating in selected_course:
                similar_courses = similar_courses.append(get_similar(c_name, rating), ignore_index=True)

            cf = pd.Series(similar_courses.sum().sort_values(ascending=False).head(10))


            for index, val in cf.iteritems():
                if index != compare :
                    collab.append(index)
        except :
            collab = None
        
    return my_course , collab



@app.route('/logout',methods = ['POST','GET'])
def logout() :
    error = None
    session['id'] = None
    return render_template('home.html', error=error)

home_flag = 0
@app.route('/home',methods = ['POST','GET'])
def home() :
        error = None
        app.route('/home')
        global home_flag
        search = request.form.get('search')
        temp = request.args.get('home')
        session["stars"] = request.form.get('star') #collab
        if home_flag == 0 :
            session["id"] = None
            home_flag += 1
        if temp != None :
            session["id"] = temp
        print(session["stars"])
        print(search)
        print("successful")

        if session["id"] != None :
            print(session["id"])
            try :
                session['my_course'] , session['collab'] = check(session["id"])
                # flash("Content Based","content")
                print("Content Based")
                for i in session['my_course'] :
                    print(i)
                    flash(i,"content")
                flag = 0   
                flash(session['id'],'id')
                if session['collab'] != None :  
                    # flash("Collaborative","collaborative")
                    print("Collaborative")   
                    for i in session['collab'] :
                        for j in session['my_course'] :
                            if i != j :
                                flag = 1
                            else :
                                flag = 0
                                break
                        if flag == 1 :
                            print(i)
                            flash(i,"collaborative")
            except :
                print("Sorry! We couldn't find any recommendation","rec_error")
            # return render_template('home.html', message=id , error=error)


        if search != None :
            try :
                data = pd.read_csv('Coursera.csv')
                Name_list = data['name']
                rating_list = data['rating']
                search_list = []
                index = 0


                split_user = search.split(" ")

                for course in Name_list:
                    index += 1
                    split_Name_list = course.split(" ")
                    for keyword1 in split_user:
                        for keyword2 in split_Name_list:
                            if keyword1.lower() == keyword2.lower():
                                search_list.append(index)

                print(len(search_list), "Results Found\n")
                course_list = []
                for index in search_list:
                    print(Name_list.iloc[index - 1], end=" : ")
                    print(rating_list[index - 1], "\n")

                    # course_list.append((Name_list.iloc[index - 1])+" : "+str(rating_list.iloc[index - 1]))
                    course_list.append((Name_list.iloc[index - 1]))
                if course_list != [] :    
                    for i in range(len(course_list)):
                        flash(course_list[i],"search")
                else :
                    flash("Sorry! We couldn't find any recommendation","search_error")
            except :
                flash("Sorry! We couldn't find any recommendation","search_error")

        return render_template('home.html', message=id , error=error)


@app.route('/login',methods = ['POST','GET'])
def login() :
        print("successful")
        error = None
        email = request.form.get('email')
        print(email)
        password = request.form.get('password')
        if email != None :
            conn = mysql.connect()
            cursor =conn.cursor()

            cursor.execute(''' SELECT * FROM registration WHERE email = %s and password = %s''',(email,password))
            data = cursor.fetchone()
            print('successfull')
            if data :
                print('successfull')
                flash('Logged in successfully')
                return render_template('home.html', error=error)
            else :
                flash('Invalid Username/Password')
        return render_template('login.html', error=error)

@app.route('/registration',methods = ['POST','GET'])
def registration() :
        error = None
        print("successful")
        error = None
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        gender = request.form.get('gender')
        phone_num = request.form.get('number')
        email = request.form.get('email')
        password = request.form.get('password')
        rpassword = request.form.get('rpassword')
        if email != None :
            fullname = fname+" "+lname
            print(fullname)
            conn = mysql.connect()
            cursor =conn.cursor()

            cursor.execute(''' INSERT INTO registration(fullname,email,gender,phone_num,password) values(%s,%s,%s,%s,%s)''',(fullname,email,gender,phone_num,password))
            data = conn.commit()
            print('successfull')
            flash('Registered Successfully')
            # flash('Sorry! could not register , Please try again')
        return render_template('registration.html', error=error)


app.run(host='localhost', port=5000)