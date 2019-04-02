from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
  
app = Flask(__name__)
cors = CORS(app, resources={r"/": {"origins": "localhost:5000"}})
app.config['SECRET_KEY'] = 'all right then keep your secrets'
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)
  
  
@app.route('/')
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def index():  
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)