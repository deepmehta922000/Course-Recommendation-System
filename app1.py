from flask import Flask,flash , render_template, request , url_for , redirect , session
from flask_session import Session
import pandas as pd
import numpy as np 
from flaskext.mysql import MySQL  
from content import content   
# from gevent.pywsgi import WSGIServer                             

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
    data = pd.read_csv("Coursera.csv",encoding='cp1252')

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
    data.to_csv("Coursera.csv",encoding='cp1252', index=False)
    data.loc[z, 'num_votes'] = update_votes
    data.to_csv("Coursera.csv",encoding='cp1252', index=False)
    data.loc[z, 'sum_rating'] = update_sum_rating
    data.to_csv("Coursera.csv",encoding='cp1252', index=False)
    print(data.loc[z])
    return "Successfully updated dataset"

def content_collab(id,flag1) :                 #content collab
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
        if flag1 != 1 :
            update_dataset = update(stars,session["id"])
            print(update_dataset)
        try :

            stars = int(stars)
            if stars < 3 :
                collab = search_func2()
                print(collab)

            elif stars >= 3 :
                def get_similar(c_name, rating):
                    similar_ratings = x[c_name] * (rating - 2.5)
                    similar_ratings = similar_ratings.sort_values(ascending=False)
                    return similar_ratings

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
            else :
                collab = None
        except :
            collab = None
        
    return my_course , collab



@app.route('/logout',methods = ['POST','GET'])
def logout() :
    error = None
    session['id'] = None
    session['email'] = None
    global home_flag
    home_flag = 0
    return render_template('login.html', error=error)


def search_func(new_login,Name_list,rating_list,x) :            #search engine
    final_list = []
    for i in range (len(new_login)):
        search_list = []
        index = 0

        split_user = new_login[i].split(" ")

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
        
        if len(course_list) > 5 :
            for i in range(5) :
                final_list.append(course_list[i])
        else :
            for i in range(len(course_list)) :
                final_list.append(course_list[i])

    res = []
    [res.append(x) for x in final_list if x not in res]
    if x == 0 :
        return res
    elif x == 1 :
        return course_list


def new_home() :    #user history , preferences , cold start
    conn = mysql.connect()
    cursor =conn.cursor()
    result = cursor.execute('''SELECT history FROM user_history where email = %s''',(session['email']))
    print(result)
    data = cursor.fetchall()
    v = []
    for i in range(result) :
        x = str(data[i]).replace("'","")
        x = x.replace("(","")
        x = x.replace(",","")
        x = x.replace(")","")
        print(x)
        v.append(x)
    return v

def update_u_hist(search) :             #update user history
    try :
        conn = mysql.connect()
        cursor =conn.cursor()
        cursor2 =conn.cursor()
        cursor3 =conn.cursor()

        result = cursor.execute('''SELECT history FROM user_history where email = %s''',(session['email']))
        data = cursor.fetchall()
        print(result)
        if search != None :
            if result >= 5 :
                cursor2.execute('''DELETE FROM user_history where email = %s''',(session['email']))
                conn.commit()
                cursor3.execute('''INSERT INTO user_history(email,history) values(%s,%s)''',(session['email'],search))
                conn.commit()
                return "Deleted and inserted"
            else :
                cursor3.execute('''INSERT INTO user_history(email,history) values(%s,%s)''',(session['email'],search))
                conn.commit()
                return "Inserted"
    except :
        return "Error occured"


def search_func2() :             #user preferences
    conn = mysql.connect()
    cursor =conn.cursor()
    result = cursor.execute(''' SELECT interests FROM registration WHERE email = %s''',(session['email']))
    data = cursor.fetchone()
    print(data)

    preferences = str(data).replace("(","")
    preferences = preferences.replace("'","")
    preferences = preferences.replace("'","")
    preferences = preferences.replace(")","")
    preferences = preferences[:-1]
    print(preferences)
    preferences = preferences.replace(",","").split()

    data = pd.read_csv('Coursera.csv',encoding='cp1252')
    Keyword_list = data['keyword']
    Name_list = data['name']
    
    final_list = []
    for i in range (len(preferences)):
        search_list = []
        index = 0
        split_user = preferences[i].split(" ")
        print(preferences[i])
        for course in Keyword_list:
            index += 1
            split_Keyword_list = course.split(" ")
            for keyword1 in split_user:
                for keyword2 in split_Keyword_list:
                    if keyword1.lower() == keyword2.lower():
                        search_list.append(index)

        print(len(search_list), "Results Found\n")
        course_list = []
        for index in search_list:
            print(Keyword_list.iloc[index - 1], end=" : ")
            print(Name_list[index - 1], "\n")

            # course_list.append((Name_list.iloc[index - 1])+" : "+str(rating_list.iloc[index - 1]))
            course_list.append((Name_list.iloc[index - 1]))
        if len(course_list) > 5 :
            for i in range(5) :
                final_list.append(course_list[i])
        else :
            for i in range(len(course_list)) :
                final_list.append(course_list[i])

    return final_list



def check_courses(list_of_courses) :
    conn = mysql.connect()
    cursor =conn.cursor()
    result = cursor.execute(''' SELECT course_name FROM completed_courses WHERE email = %s''',("jagjot@gmail.com"))
    result2 = cursor.fetchall()
    print(result)

    result2 = str(result2).replace("(","")
    result2 = result2.replace("'","")
    result2 = result2.replace(",))","")
    result2 = result2.split(",), ")
    print(result2)
    dummy = []
    flag = 0
    for i in range(len(list_of_courses)) :
        for j in range(len(result2)) :
            if list_of_courses[i] != result2[j] :
                flag = 1
            else :
                flag = 0
                break
        if flag == 1 :
            dummy.append(list_of_courses[i])
    return dummy
    
def save_completed_course(id) :
    conn = mysql.connect()
    cursor =conn.cursor()
    conn2 = mysql.connect()
    cursor2 =conn2.cursor()
    result = cursor.execute(''' SELECT * FROM completed_courses WHERE email = %s and course_name = %s''',(session['email'],id))
    print(result)
    if result == 0 :
        cursor2.execute(''' INSERT INTO completed_courses(email,course_name) values(%s,%s)''',(session['email'],id))
        conn2.commit()
        return "Successful inserted in database"
    return "Already there"
    

home_flag = 0
@app.route('/home',methods = ['POST','GET'])                #home page
def home() :
        error = None
        app.route('/home')
        global home_flag
        search = request.form.get('search')
        temp = request.args.get('home')
        session["stars"] = request.form.get('star') #collab
        data = pd.read_csv('Coursera.csv',encoding='cp1252')
        Name_list = data['name']
        rating_list = data['rating']

        if temp != None :
            session["id"] = temp
            home_flag += 1

        if home_flag == 0 :
                session["id"] = None
            # try:
                new_login = new_home()
                print(new_login)
                x = 0
                u_hist = search_func(new_login,Name_list,rating_list,x)
                u_hist = check_courses(u_hist)
                print(u_hist)

                u_preference = search_func2()
                u_preference = check_courses(u_preference)
                print(u_preference)

                new_added_courses = data[['num_votes','name']].values.tolist()
                cold_start = []
                for num_votes,name in new_added_courses :
                    if num_votes <= 10 :
                        cold_start.append(name)
                    
                print(cold_start)

                for i in range (len(u_hist)):
                    flash(u_hist[i],"user_history")

                for i in range (len(u_preference)):
                    flash(u_preference[i],"user_preference")

                for i in range (len(cold_start)):
                    flash(cold_start[i],"cold_start")
            # except:
            #     print("New home error")
            
        print(session["stars"])
        print(search)
        print("successful")

        if session["id"] != None :
            print(session["id"])

            try :
                flag1 = 0
                conn = mysql.connect()
                cursor =conn.cursor()
                flag1 = cursor.execute(''' SELECT * FROM completed_courses WHERE email = %s and course_name = %s''',(session['email'],session["id"]))
                print("Flag : ",flag1)
                if flag1 >= 1:
                    flag1 = 1
                    if search == None :
                        flash("Your review has already been recorded!","al_rev")
                
                session['my_course'] , session['collab'] = content_collab(session["id"],flag1)
                data = pd.read_csv('Coursera.csv',encoding='cp1252')
                df = data[['name','rating']].values.tolist()
                print("Content Based")
                print("Before Checking")
                print(session['my_course'])
                print("After Checking")
                session['my_course'] = check_courses(session['my_course'])
                print(session['my_course'])

                for i in session['my_course'] :
                    print(i)
                    flash(i,"content")
                    # for name,rating in df:
                    #     if(name == i):
                    #         print(session['id']+" : "+str(rating))
                    #         flash(rating,"rating")
                lag = 0 
                df = data[['name','rating','institution','num_votes','course_url']].values.tolist()
                for name,rating,institution,num_votes,course_url in df:
                    if(name == session['id']):
                        print(name,rating,institution,num_votes,course_url)
                        flash(session['id'],'id_name')
                        flash(str(rating)+" / 5.0",'id_rating')
                        flash(institution,'id_institution')
                        flash(str(num_votes),'id_students')
                        flash(course_url,'id_url')
                        
                if session['stars'] != None :
                        update_completed_courses = save_completed_course(session["id"]) 
                        print(update_completed_courses)

                if session['collab'] != None : 
                    print("Collaborative")  
                    session['collab'] = check_courses(session['collab']) 
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
                if session['my_course'] == [] :
                    flash("Sorry! We couldn't find any recommendation","rec_error")
            except :
                print("Sorry! We couldn't find any recommendation","rec_error")
            # return render_template('home.html', message=id , error=error)


        if search != None :
            if temp != None :
                home_flag += 1
            try :
                u_u_hist = update_u_hist(search)
                print(u_u_hist)
                new_login = []
                new_login.append(search)
                x = 1
                course_list = search_func(new_login,Name_list,rating_list,x)
                if course_list != [] :  
                    course_list = check_courses(course_list)  
                    for i in range(len(course_list)):
                        flash(course_list[i],"search")
                else :
                    flash("Sorry! We couldn't find any recommendation","search_error")
            except :
                flash("Sorry! We couldn't find any recommendation","search_error")

        flash(session['email'],"user")
        return render_template('home.html', message=id , error=error)


@app.route('/login',methods = ['POST','GET'])
def login() :
        print("successful")
        error = None
        session['email']  = request.form.get('email')
        print(session['email'])
        password = request.form.get('password')
        if session['email'] != None :
            conn = mysql.connect()
            cursor =conn.cursor()

            cursor.execute(''' SELECT * FROM registration WHERE email = %s and password = %s''',(session['email'],password))
            data = cursor.fetchone()
            if data :
                print('successfull')
                flash("Welcome "+session['email']+" , you have logged in successfully!!!","user_login")
                return redirect('/home')
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
        interest = request.form.getlist('interest')

        print(interest)
        x = ""
        if interest != None:
            for i in range (len(interest)):
                if i ==0:
                    x = interest[i]
                else:
                    x = x+" , "+interest[i]
        print(x)

        if email != None :
                fullname = fname+" "+lname
                print(fullname)
                conn = mysql.connect()
                cursor =conn.cursor()

                cursor.execute(''' INSERT INTO registration(fullname,email,gender,phone_num,password,interests) values(%s,%s,%s,%s,%s,%s)''',(fullname,email,gender,phone_num,password,x))
                data = conn.commit()
                print('successfull')
                flash('Registered Successfully')
                # flash('Sorry! could not register , Please try again')
                
        return render_template('registration.html', error=error)



@app.route('/admin_logout',methods = ['POST','GET'])
def admin_logout() :
    error = None
    session['admin'] = None
    return render_template('admin_login.html', error=error)


@app.route('/admin_check_users',methods = ['POST','GET'])
def admin_check_users() :
    error = None
    conn = mysql.connect()
    cursor =conn.cursor()
    result = cursor.execute(''' SELECT id,fullname,email,gender,phone_num,interests FROM registration''')
    result2 = cursor.fetchall()
    print(result)
    print(result2)

    for row in result2:
        flash(row[0],"id")
        flash(row[1],"name")
        flash(row[2],"email")
        flash(row[3],"gender")
        flash(row[4],"phone_num")
        flash(row[5], "interests")
    return render_template('admin_check_users.html', error=error)

@app.route('/admin_home',methods = ['POST','GET'])
def admin_home() :
        print("successful")
        error = None
        name  = request.form.get('name')
        institute  = request.form.get('institute')
        course_id  = request.form.get('course_id')
        keyword  = request.form.get('keyword')
        course_url  = request.form.get('course_url')
        year  = request.form.get('year')
        title  = request.form.get('title')
        rating = 0
        num_votes = 0
        sum_rating = 0
        print(name,institute,course_id,keyword,course_url,year,title)
        data = pd.read_csv("Coursera.csv",encoding='cp1252')
        z = len(data) + 1
        index = z-1
        print(z,name,institute,course_id,keyword,course_url,year,title,rating,num_votes,sum_rating)
        if name != None :
            data2 = pd.DataFrame({"index" : [index],
                     "name" : [name],
                     "rating" : [rating],
                     "num_votes" : [num_votes],
                     "institution" : [institute],
                     "course_id" : [course_id],
                     "keyword" : [keyword],
                     "course_url" : [course_url],
                     "start_year" : [year],
                     "title_type" : [title],
                     "sum_rating" : [sum_rating]})
            data = data.append(data2, ignore_index = True)
            data.to_csv("Coursera.csv",index=None)
            # data.loc[z, 'index'] = index
            # data.to_csv("Coursera.csv",float_format=None, index=False)
            # data.loc[z, 'name'] = name
            # data.to_csv("Coursera.csv",float_format=None, index=False)
            # data.loc[z, 'rating'] = rating
            # data.to_csv("Coursera.csv",float_format=None, index=False)
            # data.loc[z, 'num_votes'] = num_votes
            # data.to_csv("Coursera.csv",float_format=None, index=False)
            # data.loc[z, 'institution'] = institute
            # data.to_csv("Coursera.csv",float_format=None, index=False)
            # data.loc[z, 'course_id'] = course_id
            # data.to_csv("Coursera.csv",float_format=None, index=False)
            # data.loc[z, 'keyword'] = keyword
            # data.to_csv("Coursera.csv",float_format=None, index=False)
            # data.loc[z, 'course_url'] = course_url
            # data.to_csv("Coursera.csv",float_format=None, index=False)
            # data.loc[z, 'start_year'] = year
            # data.to_csv("Coursera.csv",float_format=None, index=False)
            # data.loc[z, 'title_type'] = title
            # data.to_csv("Coursera.csv",float_format=None, index=False)
            # data.loc[z, 'sum_rating'] = sum_rating
            # data.to_csv("Coursera.csv",float_format=None, index=False)
            print("Success")
            flash("Data Saved Successfully","success")
        return render_template('admin_home.html', error=error)


@app.route('/admin_login',methods = ['POST','GET'])
def admin_login() :
        print("successful")
        error = None
        session['admin']  = request.form.get('email')
        print(session['admin'])
        password = request.form.get('password')
        print(password)
        if session['admin'] != None :
            if session['admin'] == "admin@gmail.com" and password == "admin":
                print('successfull')
                flash("Welcome "+session['admin']+" , you have logged in successfully!!!","admin_login")
                return redirect('/admin_home')
            else :
                flash('Invalid Username/Password')
        return render_template('admin_login.html', error=error)

app.run(host='localhost', port=5000)