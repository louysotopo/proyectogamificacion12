from flask import Flask,render_template,request
from nivel1 import getTitle, get_row, nivel_1_resultados, divideArrays, getDiference

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('inicio.html')

@app.route('/basico')
def basico():
    titulo, rand_number = getTitle()
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

    arr_usuario=[pc01,pc02,pc03,pc04,pc05,pc06,pc07,pc08]

    _title, _summary, _keyword, _full_article = get_row(int(rand_number))
    matching_user_original, matching_user_prediction, matching_original_prediction = nivel_1_resultados(_title, _summary, arr_usuario)
   
    arr1 = [rand_number]
    arr1, arr2 = divideArrays(matching_original_prediction)
    list1 = arr1 # detectadas por IA

    arr1, arr2 = divideArrays(matching_user_prediction)
    list2 = arr1 # correctas 

    arr3 = getDiference(arr_usuario,arr2) # incorrectas
    list3 = getDiference(arr3, arr1)

    arr1, arr2 = divideArrays(matching_user_original)
    list4 = ["Esta parte aun se esta diseñando"] # posibles 
   
    return render_template('resultado.html',list1 = list1,list2=list2,list3=list3,list4=list4)

if __name__ == '__main__':
    app.run()