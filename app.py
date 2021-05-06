import pyrebase
from flask import Flask,render_template,request
from nivel1 import getRandom, nivel_1_resultados, nivel_2_resultados, divideArrays, getDiference, gettingData
#from keywords_difficult_level import evaluar,comparativa_estudiante

config = {
    "apiKey": "AIzaSyCsFmrjvIHBODBf0Vsb0Rvfqn5mgY2I7Lw",
    "authDomain": "gamip-e2a54.firebaseapp.com",
    "projectId": "gamip-e2a54",
    "storageBucket": "gamip-e2a54.appspot.com",
    "messagingSenderId": "783180904629",
    "appId": "1:783180904629:web:e747cd4ca127296f9b66fc",
    "measurementId": "G-17NVEBGH3M",
    "databaseURL":""
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

app = Flask(__name__)

_titles, _summaries, _keywords, _full_articles, size = gettingData()
rand_number = getRandom(size)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/create_account', methods=['GET','POST'])
def create_account():
    if request.method == 'POST':
        pwd0 = request.form['user_pwd0']
        pwd1 = request.form['user_pwd1']
        if pwd0 == pwd1 :
            try: 
                email = request.form['user_email']
                password = request.form['user_pwd1']
                new_user = auth.create_user_with_email_and_password(email,password)
                auth.send_email_verification(new_user['idToken'])
                existing_account = "Revise su correo para la confirmacion"
                return render_template("create_account.html",message=existing_account)                
            except:
                existing_account = "Este correo ya esta registrado"
                return render_template("create_account.html", message= existing_account)

    return render_template('create_account.html')


@app.route('/')
def index():
    return render_template('inicio.html')

@app.route('/basico')
def basico():
    
    rand_number = getRandom(size)
    titulo = _titles[rand_number]
    return render_template('basico.html',titulo=titulo, rand_number=rand_number)

@app.route('/intermedio')
def intermedio():
    rand_number = getRandom(size)
    resumen = _summaries[rand_number]
    return render_template('intermedio.html', resumen=resumen, rand_number=rand_number)

@app.route('/avanzado')
def avanzado():

    rand_number= getRandom(7)
    #nombre_pdf = buscarNombre(rand_number,pdf_)    
    #print(nombre_pdf)
    #return render_template('avanzado.html')
    return render_template('avanzado.html',rand_number=rand_number)

@app.route('/resultado', methods=["GET","POST"])
def resultado():
    if request.method == "POST":
        pc01 = request.form["pc01"]
        pc02 = request.form["pc02"]
        pc03 = request.form["pc03"]
        pc04 = request.form["pc04"]
        pc05 = request.form["pc05"]
        pc06 = request.form["pc06"]
        pc07 = request.form["pc07"]
        pc08 = request.form["pc08"]
        rand_number = request.form["rand_number"]

    arr_usuario=[pc01,pc02,pc03,pc04,pc05,pc06,pc07,pc08]

    _title, _summary, _keyword, _full_article = _titles[int(rand_number)], _summaries[int(rand_number)], _keywords[int(rand_number)], _full_articles[int(rand_number)]
    matching_user_original, matching_user_prediction, matching_original_prediction = nivel_1_resultados(_title, _summary, arr_usuario)
   
    arr1 = [rand_number]
    arr1, arr2 = divideArrays(matching_original_prediction)
    list1 = arr1 # detectadas por IA

    arr1, arr2 = divideArrays(matching_user_prediction)
    list2 = arr1 # correctas 

    list3 = getDiference(arr_usuario,arr2) # incorrectas
    #list3 = getDiference(arr3, arr1)

    arr1, arr2 = divideArrays(matching_user_original)
    list4 = ["Esta parte aun se esta diseñando"] # posibles 
   
    return render_template('resultado.html',list1 = list1,list2=list2,list3=list3,list4=list4)

@app.route('/resultado3', methods=["GET","POST"])
def resultado3():
    if request.method == "POST":
        pc01 = request.form["pc01"]
        pc02 = request.form["pc02"]
        pc03 = request.form["pc03"]
        pc04 = request.form["pc04"]
        pc05 = request.form["pc05"]
        pc06 = request.form["pc06"]
        pc07 = request.form["pc07"]
        pc08 = request.form["pc08"]
        rand_number = request.form["rand_number"]

    arr_usuario=[pc01,pc02,pc03,pc04,pc05,pc06,pc07,pc08]

    _title, _summary, _keyword, _full_article = _titles[int(rand_number)], _summaries[int(rand_number)], _keywords[int(rand_number)], _full_articles[int(rand_number)]
    matching_user_original, matching_user_prediction, matching_original_prediction = nivel_2_resultados(_keyword, _full_article, arr_usuario)
   
    arr1 = [rand_number]
    arr1, arr2 = divideArrays(matching_original_prediction)
    list1 = arr1 # detectadas por IA

    arr1, arr2 = divideArrays(matching_user_prediction)
    list2 = arr1 # correctas 

    list3 = getDiference(arr_usuario,arr2) # incorrectas
    #list3 = getDiference(arr3, arr1)

    arr1, arr2 = divideArrays(matching_user_original)
    list4 = _keyword.split(",") # palabras clave del autor
   
    return render_template('resultado3.html',list1 = list1,list2=list2,list3=list3,list4=list4)

@app.route('/resultado2', methods=["GET","POST"])
def resultado2():
    if request.method == "POST":
        pc01 = request.form["pc01"]
        pc02 = request.form["pc02"]
        pc03 = request.form["pc03"]
        pc04 = request.form["pc04"]
        pc05 = request.form["pc05"]
        pc06 = request.form["pc06"]
        pc07 = request.form["pc07"]
        pc08 = request.form["pc08"]
        rand_number = request.form["rand_number"]
   
    arr_usuario=[pc01,pc02,pc03,pc04,pc05,pc06,pc07,pc08]
    #diccionario_D = evaluar(rand_number,_keywords, _full_articles)
    #res1,res2,res3 = comparativa_estudiante(diccionario_D,arr_usuario)   

    #list1 = res1
    #list2 = res2
    #list3 = res3
    list1 = ["q","q"]
    list2 = ["q","q"]
    list3 = ["q","q"]
    list4 = ["q","q"]


    return render_template('resultado2.html',list1 = list1,list2=list2,list3=list3,list4=list4)

if __name__ == '__main__':
    app.run()