from flask import Flask
from flaskext.mysql import MySQL  
import pandas as pd 
app = Flask(__name__) 
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'secret!' 

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'test'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
mysql.init_app(app)

# # conn = mysql.connect()
# # cursor =conn.cursor()
# # cursor2 =conn.cursor()
# # cursor3 =conn.cursor()

# # search = 'ai'
# # result = cursor.execute('''SELECT history FROM user_history where email = %s''',("jagjot@gmail.com"))
# # data = cursor.fetchall()
# # print(result)
# # if search != None :
# #     if result >= 2 :
# #         cursor2.execute('''DELETE FROM user_history where email = %s''',("jagjot@gmail.com"))
# #         conn.commit()
# #         cursor3.execute('''INSERT INTO user_history(email,history) values(%s,%s)''',("jagjot@gmail.com",search))
# #         conn.commit()
# #         print("Deleted and inserted")
# #     else :
# #         cursor3.execute('''INSERT INTO user_history(email,history) values(%s,%s)''',("jagjot@gmail.com",search))
# #         conn.commit()
# #         print("Inserted")

# # x = "AI for everyone , Average Rating : 4.8 / 5"
# # x = x[:-27]
# # print(x)

def search_func2(new_login,Name_list,rating_list) :
    for i in range (len(new_login)):
        search_list = []
        index = 0
        split_user = new_login[i].split(" ")
        print(new_login[i])
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
    return course_list

# x = "AI , Python , AWS"
# x = x.replace(",","").split()
# print(x)

conn = mysql.connect()
cursor =conn.cursor()
result = cursor.execute(''' SELECT interests FROM registration WHERE email = %s''',("raman@gmail.com"))
data = cursor.fetchone()
print(data)

x = str(data).replace("(","")
x = x.replace("'","")
x = x.replace("'","")
x = x.replace(")","")
x=x[:-1]
print(x)
x = x.replace(",","").split()
print(x)

data = pd.read_csv("Coursera.csv")
Name_list = data["keyword"]
rating_list = data["name"]
y = search_func2(x,Name_list,rating_list)
print(y)

# data = pd.read_csv("Coursera.csv")
# x = data[['num_votes','name']].values.tolist()
# cold_start = []
# for num_votes,name in x :
#     if num_votes <= 0 :
#         cold_start.append(name)
    
# print(cold_start)


# conn = mysql.connect()
# cursor =conn.cursor()
# result = cursor.execute(''' SELECT course_name FROM completed_courses WHERE email = %s''',("jagjot@gmail.com"))
# result2 = cursor.fetchall()
# print(result)
# print(result2)
# result2 = str(result2).replace("(","")
# result2 = result2.replace("'","")
# result2 = result2.replace(",))","")
# result2 = result2.split(",), ")
# print(result2)
# data = pd.read_csv("Coursera.csv")
# y = data['name']

# conn = mysql.connect()
# cursor =conn.cursor()
# result = cursor.execute(''' SELECT * FROM registration''')
# result2 = cursor.fetchall()
# print(result)
# print(result2)

# user_data = []
# for row in result2:
#     print("Id = ", row[0], )
#     print("fullname = ", row[1])
#     print("email  = ", row[2])
#     print("gender  = ", row[3])
#     print("phone_num  = ", row[4])
#     print("interests  = ", row[5], "\n")

# data = pd.read_csv("Coursera.csv")
# print(len(data))
data = pd.read_csv('Coursera.csv',encoding='cp1252')
# Name_list = data['keyword']
# rating_list = data['name']
# preferences = ['coding','aws','business','computer']
# final_list = []
# for i in range (len(preferences)):
#         search_list = []
#         index = 0
#         split_user = preferences[i].split(" ")
#         print(preferences[i])
#         for course in Name_list:
#             index += 1
#             split_Name_list = course.split(" ")
#             for keyword1 in split_user:
#                 for keyword2 in split_Name_list:
#                     if keyword1.lower() == keyword2.lower():
#                         search_list.append(index)

#         print(len(search_list), "Results Found\n")
#         course_list = []
#         for index in search_list:
#             print(Name_list.iloc[index - 1], end=" : ")
#             print(rating_list[index - 1], "\n")

#             # course_list.append((Name_list.iloc[index - 1])+" : "+str(rating_list.iloc[index - 1]))
#             course_list.append((Name_list.iloc[index - 1]))
#         if len(course_list) > 5 :
#             for i in range(5) :
#                 final_list.append(course_list[i])
#         else :
#             for i in range(len(course_list)) :
#                 final_list.append(course_list[i])

# print(data.info())
# index = 600
# name  = "Engineering Mathematics 1"
# institute  = "MU"
# course_id  = "EM-1"
# keyword  = "maths"
# course_url  = "https://maths.com"
# year  = 2016
# title  = 3
# rating = 0
# num_votes = 0
# sum_rating = 0
# data2 = pd.DataFrame({"index" : [index],
#                      "name" : [name],
#                      "rating" : [rating],
#                      "num_votes" : [num_votes],
#                      "institution" : [institute],
#                      "course_id" : [course_id],
#                      "keyword" : [keyword],
#                      "course_url" : [course_url],
#                      "start_year" : [year],
#                      "title_type" : [title],
#                      "sum_rating" : [sum_rating]})
# print(data2)

# data = data.append(data2, ignore_index = True)
# print(data.tail())
# data.to_csv("Coursera.csv",index=None)
# data = pd.read_csv('Coursera.csv',encoding='cp1252')
# print(data.tail())
