from flask import Flask, jsonify
import requests

app = Flask(__name__)

LAT = 42.8805
LON = -8.5457

def evaluar_deporte(temp, lluvia, viento):
    """Aquí mantenemos la lógica del primer código"""
    if lluvia > 0.1:
        return "No recomendado - Lluvia"
    if temp < 5:
        return "No recomendado - Frío extremo"
    if temp > 30:
        return "No recomendado - Calor extremo"
    if viento > 25:
        return "No recomendado - Mucho viento"
    return "¡Ideal para deporte!"
    
@app.route('/api/galicia/deporte', methods=['GET'])
def obtener_datos():
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,precipitation,wind_speed_10m&timezone=Europe%2FMadrid"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()['current']

        t = data['temperature_2m']
        p = data['precipitation']
        v = data['wind_speed_10m']

        estado = evaluar_deporte(t, p, v)
        es_apto_real = 1 if "Ideal" in estado else 0

        fijo_para_alerta = 1

        res = jsonify([{
            "ciudad": "Santiago de Compostela",
            "temperatura": t,
            "lluvia": p,
            "viento": v,
            "recomendacion": estado,
            "apto": es_apto_real,
            "trigger_alerta": fijo_para_alerta
        }])
        res.headers.add("ngrok-skip-browser-warning", "true")
        return res

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # El puerto 5000 es el estándar de Flask
    app.run(host='0.0.0.0', port=5000)
