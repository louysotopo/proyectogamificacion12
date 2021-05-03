from flask import Flask,render_template,request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('inicio.html')

@app.route('/basico')
def basico():
    titulo = "este es un titulo"
    return render_template('basico.html',titulo=titulo)

@app.route('/intermedio')
def intermedio():
    return render_template('intermedio.html')

@app.route('/avanzado')
def avanzado():
    return render_template('avanzado.html')


@app.route('/resultado', methods=["GET","POST"])
def resultado():
    list1 = ["item1","item2","item3","item4"]
    list2 = ["item1","item2","item3","item4"]
    list3 = ["item1","item2","item3","item4"]
    list4 = ["item1","item2","item3","item4"]

    if request.method == "POST":
        pc01 = request.form["pc01"]
        pc02 = request.form["pc02"]
        pc03 = request.form["pc03"]
        pc04 = request.form["pc04"]
        pc05 = request.form["pc05"]
        pc06 = request.form["pc06"]
        pc07 = request.form["pc07"]
        pc08 = request.form["pc08"]           
        
    return render_template('resultado.html',list1 = list1,list2=list2,list3=list3,list4=list4)

if __name__ == '__main__':
    app.run(debug=True)