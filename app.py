import pyrebase
from flask import Flask,render_template,request,session,escape
from nivel1 import getRandom, nivel_1_resultados, nivel_2_resultados, divideArrays, getDiference, gettingData, getPuntaje
#from keywords_difficult_level import evaluar,comparativa_estudiante

config = {
    "apiKey": "AIzaSyCsFmrjvIHBODBf0Vsb0Rvfqn5mgY2I7Lw",
    "authDomain": "gamip-e2a54.firebaseapp.com",
    "projectId": "gamip-e2a54",
    "storageBucket": "gamip-e2a54.appspot.com",
    "messagingSenderId": "783180904629",
    "appId": "1:783180904629:web:e747cd4ca127296f9b66fc",
    "measurementId": "G-17NVEBGH3M",
    "databaseURL":"https://gamip-e2a54-default-rtdb.firebaseio.com"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__)

_titles, _summaries, _keywords, _full_articles, size = gettingData()
rand_number = getRandom(size)

@app.route('/', methods=['GET','POST'])
def login():
    mes = ""
    if request.method == 'POST':
        email = request.form['user_email']
        pwd   = request.form['user_pwd']
        try:
            user = auth.sign_in_with_email_and_password(email,pwd)
            user__ = auth.get_account_info(user['idToken'])
            #print(user)
            session["userid"] = user['localId']
            session["email"] = user['email']
            session["nivel1"] = "0"
            session["nivel2"] = "0"
            
            return render_template('inicio.html',message=mes)
        except:
            mes = "Usuario o contraseña incorrecta"
            return render_template('login.html',message=mes)

    return render_template('login.html',message=mes)    

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
                session["userid"] = new_user['localId']
                session["email"] = new_user['email']
                session["nivel1"] = "0"
                session["nivel2"] = "0"              

                return render_template("create_account.html",message=existing_account)                
            except:
                existing_account = "Este correo ya esta registrado"
                return render_template("create_account.html", message= existing_account)

    return render_template('create_account.html')


@app.route('/inicio')
def index():
    return render_template('inicio.html')

@app.route('/basico', methods=["GET","POST"])
def basico():
    puntaje = 0
    try:
        if request.method == "POST":
            puntaje_actual = request.form["puntaje_actual"]
            puntaje = puntaje_actual
    except:
        puntaje = 0
    rand_number = getRandom(size)
    titulo = _titles[rand_number]
    return render_template('basico.html',titulo=titulo, rand_number=rand_number, puntaje=puntaje, puntaje_actual=puntaje)

@app.route('/intermedio' , methods=["GET","POST"])
def intermedio():
    puntaje = 0
    try:
        if request.method == "POST":
            puntaje_actual = request.form["puntaje_actual"]
            puntaje = puntaje_actual
    except:
        puntaje = 0
    rand_number = getRandom(size)
    resumen = _summaries[rand_number]
    return render_template('intermedio.html', resumen=resumen, rand_number=rand_number, puntaje=puntaje, puntaje_actual=puntaje)

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
        puntaje_actual = request.form["puntaje_actual"]
        #enviar_datos()


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
   
    puntaje_obtenido = getPuntaje(list2,list3)
    puntaje_actual = int(puntaje_actual) + puntaje_obtenido
    
    return render_template('resultado.html',list1 = list1,list2=list2,list3=list3,list4=list4, puntaje_obtenido=puntaje_obtenido, puntaje_actual=puntaje_actual)

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
        puntaje_actual = request.form["puntaje_actual"]

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
   
    puntaje_obtenido = getPuntaje(list2,list3)
    puntaje_actual = int(puntaje_actual) + puntaje_obtenido

    return render_template('resultado3.html',list1 = list1,list2=list2,list3=list3,list4=list4, puntaje_obtenido=puntaje_obtenido, puntaje_actual=puntaje_actual)

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
    list1 = ["q","q"]
    list2 = ["q","q"]
    list3 = ["q","q"]
    list4 = ["q","q"]
    return render_template('resultado2.html',list1 = list1,list2=list2,list3=list3,list4=list4)

@app.route("/logout")
def logout():
    session.pop("userid",None)
    session.pop("email",None)
    session.pop("nivel1",None)
    session.pop("nivel2",None)
    return "You are logged Out"

@app.route("/enviar_datos")
def enviar_datos():
    if "userid" in session:
        #print(session["userid"])
        data = {"email": session["email"],"nivel1":session["nivel1"],"nivel2":session["nivel2"]}
        db.child("students").child(session["userid"]).set(data)
        #db.child("students").push({"aaaa":"aaaa"})
        return "Your are loged"
    return "You must log in first"

    #db.child("students").update("a@unsa.edu.pe").push({"nombre":"juan alberto","nivel1":12,"nivel2":15})
    #db.child("students").update({"name":"joshi"})

app.secret_key = "12345"
if __name__ == '__main__':
    app.run()