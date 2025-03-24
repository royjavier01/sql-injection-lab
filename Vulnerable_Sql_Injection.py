from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
    """)
    c.execute("INSERT INTO users (username, password) VALUES ('admin', 'password123')")
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        c.execute(query)
        user = c.fetchone()
        conn.close()
        
        if user:
            return "Login exitoso!"  # Simula el acceso a la aplicación
        else:
            return "Credenciales incorrectas"
    
    return render_template_string('''
        <form method="post">
            <label>Usuario:</label>
            <input type="text" name="username"><br>
            <label>Contraseña:</label>
            <input type="password" name="password"><br>
            <input type="submit" value="Ingresar">
        </form>
    ''')

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
