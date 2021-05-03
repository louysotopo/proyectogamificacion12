from flask import Flask,render_template,request
from nivel1 import getTitle

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('inicio.html')

@app.route('/basico')
def basico():
    titulo, rand_number = getTitle(2)
    return render_template('basico.html',titulo=titulo, rand_number=rand_number)

@app.route('/intermedio')
def intermedio():
    return render_template('intermedio.html')

@app.route('/avanzado')
def avanzado():
    return render_template('avanzado.html')


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
    arr=[pc01,pc02,pc03,pc04,pc05,pc06,pc07,pc08]
    
    list1 = ["lista1","hola"] # detectadas por IA
    list2 = [pc01,"item2","item3","item4"] # correctas 
    list3 = ["item1","item2","item3","item4"] # incorrectas
    list4 = ["item1","item2","item3","item4"] # posibles 
   
    return render_template('resultado.html',list1 = list1,list2=list2,list3=list3,list4=list4)

if __name__ == '__main__':
    app.run(debug=True)