@app.route('/cf',methods = ['POST','GET'])
def cf() :
    error = None
    stars = request.form.get('star')
    print(stars)
    temp = request.args.get('cf')
    if temp != None :
        session["id"] = temp
    print(session["id"])

    my_course = content.content_based(session["id"])

    flash("Content Based","content")
    print("Content Based")
    for i in my_course :
        print(i)
        flash(i,"content")

    if stars != None:

        def get_similar(c_name, rating):
            similar_ratings = x[c_name] * (rating - 2.5)
            similar_ratings = similar_ratings.sort_values(ascending=False)
            return similar_ratings

        stars = int(stars)

        x = pd.read_csv('dummy.csv')
        x = x.corr(method='pearson')

        selected_course = [(session["id"], stars)]
        compare = session["id"]

        similar_courses = pd.DataFrame()
        for c_name, rating in selected_course:
            similar_courses = similar_courses.append(get_similar(c_name, rating), ignore_index=True)

        # print(similar_courses.sum().sort_values(ascending=False).head(10))
        cf = pd.Series(similar_courses.sum().sort_values(ascending=False).head(10))
        flash("Collaborative","collaborative")
        print("Collaborative")
        collab = []
        for index, val in cf.iteritems():
            if index != compare :
                collab.append(index)
        check = 0        
        for i in collab :
            for j in my_course :
                if i != j :
                    check = 1
                else :
                    check = 0
                    break
            if check == 1 :
                flash(i,"collaborative")

    return render_template('cf.html', message=id , error=error)