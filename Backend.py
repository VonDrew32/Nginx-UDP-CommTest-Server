# -*- coding: utf-8 -*-
import psycopg2
from flask import Flask, render_template_string, jsonify
from waitress import serve

app = Flask(__name__)

HTML_BASE = """
<!DOCTYPE html>
<html>
<head>
    <title>GPS Tracker - Tiempo Real</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; background: #eceff1; padding-top: 50px; }
        .card { background: white; padding: 30px; border-radius: 15px; display: inline-block; 
                box-shadow: 0 10px 20px rgba(0,0,0,0.1); transition: background 0.5s; }
        .coords { font-size: 2.5em; color: #2c3e50; font-weight: bold; margin: 20px 0; }
        .label { color: #7f8c8d; font-size: 0.9em; text-transform: uppercase; }
        /* Animación de destello */
        .flash-update { background: #d4edda !important; }
    </style>
</head>
<body>
    <div class="card" id="main-card">
        <span class="label">Última Ubicación (ID: <span id="reg-id">...</span>)</span>
        <div class="coords">
            <span id="lat">0.00</span>, <span id="lng">0.00</span>
        </div>
        <p class="label">Sincronizado: <span id="timestamp">...</span></p>
    </div>

    <script>
        let ultimoId = null;

        function actualizar() {
            fetch('/api/datos')
                .then(response => response.json())
                .then(data => {
                    if (!data.error) {
                        // Solo si el ID es diferente, actualizamos y animamos
                        if (ultimoId !== data.id) {
                            document.getElementById('reg-id').innerText = data.id;
                            document.getElementById('lat').innerText = data.lat;
                            document.getElementById('lng').innerText = data.lng;
                            document.getElementById('timestamp').innerText = data.fecha + " " + data.hora;

                            // Efecto visual si no es la primera carga
                            if (ultimoId !== null) {
                                const card = document.getElementById('main-card');
                                card.classList.add('flash-update');
                                setTimeout(() => card.classList.remove('flash-update'), 1000);
                            }
                            ultimoId = data.id;
                        }
                    }
                });
        }

        setInterval(actualizar, 2000);
        actualizar();
    </script>
</body>
</html>
"""

def obtener_ultima_fila():
    try:
        # Configuración de conexión para PostgreSQL en Windows
        conn = psycopg2.connect(
            host="localhost", # 'localhost' a veces falla en Windows sin red activa
            database="postgres",
            user="postgres",
            password="password",
            port="5432" 
        )
        cur = conn.cursor()
        # Consulta para traer solo la última fila basada en un ID o fecha
        cur.execute('SELECT * FROM "Location-Data" ORDER BY "ID" DESC LIMIT 1;')
        fila = cur.fetchone()
        cur.close()
        conn.close()
        return fila
    except Exception as e:
        return f"Error de conexión: {e}"

@app.route('/')
def index():
    # Esta es la página principal que carga el diseño
    return render_template_string(HTML_BASE)
@app.route('/api/datos')
def api_datos():
    # Esta ruta solo devuelve la data pura
    fila = obtener_ultima_fila()
    if isinstance(fila, tuple):
        return jsonify({
            "lat": fila[0],
            "lng": fila[1],
            "fecha": fila[2],
            "hora": fila[3],
            "id": fila[4]
        })
    return jsonify({"error": "No hay datos"}), 500
if __name__ == "__main__":
    print("Servidor Waitress corriendo en http://0.0.0.0:5000")
    # Waitress sirve la app en el puerto 8080
    serve(app, host='0.0.0.0', port=5000)
