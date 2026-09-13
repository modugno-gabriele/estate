from flask import Flask, jsonify
import pymysql
from pymysql.cursors import DictCursor

app = Flask(__name__)

def get_connection():
    return pymysql.connect(
        host="gateway01.eu-central-1.prod.aws.tidbcloud.com",
        port=4000,
        user="2SZc5k7KdZYPqyW.root",
        password="72Y5VOscDuPCXRkX",
        database="Estate",
        cursorclass=DictCursor,
        ssl={"ssl": {}}
    )

@app.route("/")
def home():
    return "Server attivo!"

@app.route("/api/prodotti", methods=["GET"])
def get_prodotti():
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, nome, prezzo,ROUND( prezzo * 1.22, 2) AS prezzo_ivato
                FROM prodotti
            """)
            prodotti = cursor.fetchall()
        conn.close()
        return jsonify(prodotti), 200
    except Exception as e:
        return jsonify({"errore": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)