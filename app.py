from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS, cross_origin
import json
from crud_funcs import create_item, delete_item, get_items


app = Flask(__name__)
cors = CORS(app, resources={r"/": {"origins": "localhost:5000"}})
app.config['SECRET_KEY'] = 'all right then keep your secrets'
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)
  
  
@app.route('/')
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def dashboard_redirect():  
    return redirect(url_for('dashboard'))

  
@app.route('/dashboard')
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def dashboard():  
    return render_template("crud_dashboard.html")


@app.route('/dashboard_api', methods=['GET', 'POST', 'PUT', 'DELETE'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def dashboard_api():

    result = None

    if request.method == 'GET':

        # Get/Update
        redis_key = request.args.get("key")
        response = get_items(redis_key)
        result = response

    elif request.method == 'POST' or request.method == 'PUT':

        # Create/Update
        item_dict = request.data
        response = create_item(item_dict)
        result = response

    elif request.method == 'DELETE':

        # Delete
        item_dict = request.data
        response = delete_item(item_dict)
        result = response

    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)