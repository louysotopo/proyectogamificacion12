from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('inicio.html')

@app.route('/basico')
def basico():
    return render_template('basico.html')

@app.route('/intermedio')
def intermedio():
    return render_template('intermedio.html')

@app.route('/resultado')
def resultado():
    arr= ["qasdasd"]
    return render_template('resultado.html')

if __name__ == '__main__':
    app.run(debug=True)