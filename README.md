# CRUD with Flask and Vue

### Flask Setup
Setup for your Flask app
```bash
mkdir flask-vue-crud
virtualenv -p python3.7 venv
source venv/bin/activate
pip install flask flask_cors
touch app.py .gitignore README.md
```

Write in your `.gitignore` file
```
venv/
.vscode/ # This is for vscode
.Idea/
*.pyc
```

Write in your `app.py` file
```python
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
    return "Hello"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
```

Run your application and go to http://0.0.0.0:5000/
```bash
python app.py

# Terminal output after running your app.py 
* Serving Flask app "app" (lazy loading)
* Environment: production
  WARNING: Do not use the development server in a production environment.
  Use a production WSGI server instead.
* Debug mode: on
* Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
* Restarting with stat
* Debugger is active!
* Debugger PIN: 760-681-493
```