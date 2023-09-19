from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import mysql.connector

app = Flask(__name__)

cx = mysql.connector.connect(host='localhost', user='root', password='banco123', database='crud')
cursor = cx.cursor()




@app.route('/')
def index():
    cursor.execute("SELECT * FROM livros")
    livros = cursor.fetchall()
    return render_template('index.html', livros=livros)


@app.route('/adicionar_livro', methods=['POST'])
def adicionar_livro():
    titulo = request.form['titulo']
    autor = request.form['autor']
    ano = request.form['ano']
    preco = request.form['preco']
    
    cursor.execute("INSERT INTO livros (titulo, autor, ano, preco) VALUES (%s, %s, %s, %s)",
                   (titulo, autor, ano, preco))
    cx.commit()
    
    return redirect(url_for('index'))


@app.route('/excluir_livro/<int:idLivros>')
def excluir_livro(idLivros):
    cursor.execute("DELETE FROM livros WHERE idLivros = %s", (idLivros,))
    cx.commit()
    
    return redirect(url_for('index'))




if __name__ == "__main__":
    app.run(debug=True)
