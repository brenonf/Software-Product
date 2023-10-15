from flask import Flask, render_template, request, redirect, url_for
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

@app.route('/lista_livros', methods=['GET'])
def lista_livros():
    search_term = request.args.get('search_term', default='', type=str) 
    tipo = request.args.get('search_type', default='tudo', type=str)
    
    if search_term:
        if tipo == 'titulo':
            cursor.execute("SELECT * FROM livros WHERE titulo LIKE %s", (f"%{search_term}%",))
        elif tipo == 'autor':
            cursor.execute("SELECT * FROM livros WHERE autor LIKE %s", (f"%{search_term}%",))
        else:
            cursor.execute("SELECT * FROM livros WHERE titulo LIKE %s OR autor LIKE %s", (f"%{search_term}%", f"%{search_term}%"))
        livros = cursor.fetchall()
    else:
        cursor.execute("SELECT * FROM livros")
        livros = cursor.fetchall()
    
    return render_template('lista_livros.html', livros=livros, search_term=search_term, search_type=tipo)  



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
