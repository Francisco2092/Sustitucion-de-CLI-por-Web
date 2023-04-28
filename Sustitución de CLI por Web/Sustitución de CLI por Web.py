from flask import Flask, render_template, request
import redis

cliente = redis.Redis(host="servidor", port=puerto, password="contraseña")
app = Flask(__name__)

@app.route("/")
def inicio():
    palabras = cliente.keys("*")
    return render_template("inicio.html", palabras=palabras)

@app.route("/agregar", methods=["GET", "POST"])
def agregar_palabra():
    if request.method == "POST":
        palabra = request.form["palabra"]
        significado = request.form["significado"]
        cliente.set(palabra, significado)
        return redirect("/")
    return render_template("agregar.html")

@app.route("/editar/<palabra>", methods=["GET", "POST"])
def editar_palabra(palabra):
    if request.method == "POST":
        nuevo_significado = request.form["significado"]
        if cliente.exists(palabra):
            cliente.set(palabra, nuevo_significado)
            return redirect("/")
        else:
            return "La palabra no fue encontrada en el diccionario."
    significado = cliente.get(palabra)
    return render_template("editar.html", palabra=palabra, significado=significado)

@app.route("/eliminar/<palabra>")
def eliminar_palabra(palabra):
    if cliente.exists(palabra):
        cliente.delete(palabra)
        return redirect("/")
    else:
        return "La palabra no fue encontrada en el diccionario."

@app.route("/buscar", methods=["GET", "POST"])
def buscar_palabra():
    if request.method == "POST":
        palabra = request.form["palabra"]
        significado = cliente.get(palabra)
        if significado:
            return render_template("resultado_busqueda.html", palabra=palabra, significado=significado.decode())
        else:
            return "La palabra no fue encontrada en el diccionario."
    return render_template("buscar.html")

if __name__ == "__main__":
    app.run(debug=True)
