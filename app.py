from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'chave_acervo_sienna'

def iniciar_banco():
    conn = sqlite3.connect('feed_privado.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS comentarios 
                    (id INTEGER PRIMARY KEY, foto TEXT, autor TEXT, texto TEXT)''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'usuario' not in session:
        if request.method == 'POST':
            session['usuario'] = request.form['nome']
            return redirect(url_for('index'))
        return render_template('login.html')

    # AQUI VOCÊ DEFINE AS FOTOS E AS LEGENDAS DELAS:
    # Cada item tem o nome do arquivo na pasta static e o texto da legenda.
    fotos_com_legendas = [
        {
            'arquivo': '1.JPG', 
            'legenda': 'now you see me, now you dont'
        },
        {
            'arquivo': '2.jpeg', 
            'legenda': 'essa é exclusiva para os de verdade'
        },
        {
            'arquivo': '3.jpeg', 
            'legenda': 'Madgadela Bay - Imaginal Disk, Vampire in the Corner.'
        },
        {
            'arquivo': '4.JPG', 
            'legenda': 'drinking wine and nonbinary'
        },   
        {
            'arquivo': '5.jpg', 
            'legenda': 'jadeish'
        },
        {
            'arquivo': '6.jpeg', 
            'legenda': 'Moment'
        },
        {
            'arquivo': '7.jpg', 
            'legenda': 'como diria o ta bom #### desculpa te beijar com gosto de cigarro'
        },
        {
            'arquivo': '8.jpg', 
            'legenda': 'amo >>>essas<<< pessoas'
        },
        {
            'arquivo': '9.jpeg', 
            'legenda': 'four calendar café'
        }
    ]
    
    conn = sqlite3.connect('feed_privado.db')
    c = conn.cursor()
    c.execute("SELECT foto, autor, texto FROM comentarios")
    todos_comentarios = c.fetchall()
    conn.close()

    comentarios_foto = {f['arquivo']: [] for f in fotos_com_legendas}
    for foto, autor, texto in todos_comentarios:
        if foto in comentarios_foto:
            comentarios_foto[foto].append((autor, texto))

    return render_template('index.html', dados_fotos=fotos_com_legendas, comentarios=comentarios_foto, usuario=session['usuario'])

@app.route('/comentar', methods=['POST'])
def comentar():
    foto = request.form['foto']
    texto = request.form['texto']
    autor = session.get('usuario', 'anônimo')
    
    conn = sqlite3.connect('feed_privado.db')
    conn.execute("INSERT INTO comentarios (foto, autor, texto) VALUES (?, ?, ?)", (foto, autor, texto))
    conn.commit()
    conn.close()
    
    # Se for uma requisição via JavaScript, retorna um JSON de sucesso
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return {'status': 'sucesso', 'autor': autor, 'texto': texto}
        
    return redirect(url_for('index'))
if __name__ == '__main__':
    iniciar_banco()
    app.run(debug=True)