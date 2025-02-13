from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("geofind.html")

@app.route("/location", methods=["POST"])
def get_location():
    data = request.json
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    return jsonify({"message": f"Localização recebida: {latitude}, {longitude}"}), 200

if __name__ == "__main__":
    app.run(debug=True)
