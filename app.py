from flask import Flask,render_template


app = Flask(__name__)

@app.route('/')
def index():
    titulo = "app gamificacion"
    lista = ['footer','header','info','hola']
    return render_template('index.html',titulo=titulo,lista=lista)

@app.route('/intermedio')
def hoja1():
    return render_template('intermedio.html')

if __name__ == '__main__':
    app.run(debug=True)