from flask import Flask, request, render_template_string, g
import sqlite3
import bcrypt

app = Flask(__name__)

# Base de datos SQLite
DATABASE = "users_secure.db"

def get_db():
    """Obtiene una conexión a la base de datos"""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # Permite acceder a las columnas por nombre
    return db

def init_db():
    """Inicializa la base de datos con un usuario seguro"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)")
        
        # Hashear la contraseña antes de almacenarla
        hashed_password = bcrypt.hashpw("admin123".encode("utf-8"), bcrypt.gensalt())

        cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ("admin", hashed_password))
        conn.commit()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()  # Sanitiza el input
        password = request.form["password"].strip()

        conn = get_db()
        cursor = conn.cursor()

        # ✅ CONSULTA PARAMETRIZADA: Previene SQL Injection
        cursor.execute("SELECT username, password FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode("utf-8"), user["password"]):
            return f"Bienvenido {user['username']}"
        else:
            return "Credenciales incorrectas"

    return render_template_string('''
        <form method="post">
            <input type="text" name="username" placeholder="Usuario" required><br>
            <input type="password" name="password" placeholder="Contraseña" required><br>
            <button type="submit">Iniciar sesión</button>
        </form>
    ''')

if __name__ == "__main__":
    init_db()  # Inicializa la base de datos
    app.run(debug=True)
