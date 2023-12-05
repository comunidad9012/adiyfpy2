# app.py

from apiwsgi import Wsgiclass

app = Wsgiclass()

@app.ruta("/home")
def home(request, response):
    # response.text = "<h3>Pagina Home</h3>"
    response.text = app.template(
    "home.html", context={"titulo": "Pagina Principal", "usuario": "Terricola"})

@app.ruta("/otra")
def otra(request, response):
    response.text = "Otra Pagina"

@app.ruta("/ultima")
def ultima(request, response):
    response.text = "Ultima Pagina"

@app.ruta("/saludo/{nombre}")
def saludo(request, response, nombre):
	response.text = f"Hola, {nombre}"