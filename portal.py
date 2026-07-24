# -*- coding: utf-8 -*-
"""
@author: JUAN CARLOS HERNANEZ FUNES
"""
#import pyodbc
from flask_mysqldb import MySQL
from flask import Flask, render_template , request , redirect, url_for, flash
import os
import random
import string
#print(os.getcwd() + '\\templates')
#Se agregó esta linea de codigo para que funcione el ejecutable con pyinstaller y poder correr el servicio como un exe
app = Flask(__name__, template_folder= os.getcwd() + '\\templates')
#app.config['SECRET_KEY'] = '1111'

# Pasarlo a un archivo .conf
app.config["MYSQL_HOST"] = 'localhost'
app.config["MYSQL_USER"] = 'root'
app.config["MYSQL_PASSWORD"] = 'Books2026'
app.config["MYSQL_DB"] = 'bd_library'
mysql = MySQL(app)

def generate_code_book():
    code_existe=False
    while code_existe == False:
        # Selecciona una letra aleatoria de la A a la Z
        letra = random.choice(string.ascii_uppercase)
        # Genera un número aleatorio de dos dígitos (del 01 al 99)
        numero = random.randint(1, 12)
        if numero < 10:
            numero = '0'+ str(numero)   
        # Combina ambos elementos en un solo texto
        code_book = f"{letra}{numero}"
        #print(code_book)
        cur = mysql.connection.cursor()
        cur.execute("SELECT code FROM BOOKS WHERE code= %s", (code_book,))
        res_codes = cur.fetchone()
        #print(res_codes)
        if res_codes is None:
            #print("El code no existe.")
            code_existe = True
    return code_book

@app.route("/")
def index():
    cur = mysql.connection.cursor()
    cur.execute('select * from books')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', books = data)

@app.route("/add", methods=["POST"])
def add_book():
    if request.method== 'POST':
        name = request.form['name']
        author = request.form['author']
        genre = request.form['genre']
        code_book = generate_code_book()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO BOOKS (code, name,author,genre) VALUES (%s,%s,%s,%s)", (code_book,name,author,genre))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

@app.route("/edit/<int:id>", methods=["POST","GET"])
def edit_book(id):
    if request.method== 'POST':
        name = request.form['name']
        author = request.form['author']
        genre = request.form['genre']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE BOOKS SET NAME = %s, AUTHOR = %s ,GENRE = %s WHERE id = %s", (name,author,genre, id,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM BOOKS WHERE ID= %s", (id,))
        data = cur.fetchone()
        cur.close()
        return render_template('edit.html', books = data)

@app.route("/search", methods=["GET"])
def search_book():
    # Captura el término de búsqueda enviado desde el formulario HTML
    query = request.args.get('query', '').strip()
    cur = mysql.connection.cursor()  
    if query:
        # Busca coincidenzas parciales en code, titulo, autor o género
        # El %s se acompaña de '%' para que busque "contiene este texto"
        search_pattern = f"%{query}%"
        cur.execute(
            "SELECT * FROM books WHERE code LIKE %s OR name LIKE %s OR author LIKE %s OR genre LIKE %s", 
            (search_pattern, search_pattern, search_pattern, search_pattern)
        )
    else:
        # Si el usuario presiona buscar con el campo vacío, muestra todos los libros
        cur.execute("SELECT * FROM books")     
    data = cur.fetchall()
    cur.close()
    # Reutiliza tu plantilla index.html enviando los resultados filtrados
    return render_template('index.html', books=data, query=query)

@app.route("/delete/<int:id>")
def delete_book(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM BOOKS WHERE ID= %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

#if(__name__ == "__main__"):
#PARA ENTRAR REMOTAMENTE
#app.run(host='CO-JUHERNANDEZF',port=8080)
#LOCALMENTE
app.run(host='localhost',port=3000, debug=True)
#Cuando se quiera ejecutar en un servidor SRV-CFDI(172.18.3.83)
#app.run(host='SRV-CFDI',port=3000)

    
    
