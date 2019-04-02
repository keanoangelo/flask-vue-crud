# CRUD with Flask and Vue

### Flask Setup
Setup for your Flask app
```bash
mkdir flask-vue-crud
cd flask-vue-crud
virtualenv -p python3.7 venv
source venv/bin/activate
pip install flask flask_cors redis
pip freeze > requirements.txt
touch app.py .gitignore README.md
```

Write in your `.gitignore` file
```
venv/
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

Make a `templates` directory parallel to your `app.py` file for your html files and then make an `index.html` file inside it
```
mkdir templates
touch templates/index.html
```

Write in your index.html
```
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="UTF-8">
		<meta name="viewport"  content="width=device-width,initial-scale=1.0">
		<title>Index</title>
	</head>
	<body>
        <h1>Hello</h1>
	</body>
</html>
```

### Redis Setup

This guide assumes that your Redis is already set up but if not check out this tutorial by Digitial Ocean: https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-redis-on-ubuntu-16-04

### Flask CRUD functions

Make a file called `crud_funcs.py`. This is where we're going to put our database query functions

```python
from redis import Redis
import json

# Redis server
r_server = Redis(host='localhost',port='6379', db='0')

if __name__ == "__main__":
    pass
```

Make a file called `utils.py` for your utility functions
```python
def item_generator(num_of_items):

    """ 
    Generate a list of items for Redis insertion 

    Args: 
        num_of_items(int): number of items 
        you want to make
    """

    generated_items = []

    for i in range(0, num_of_items):

        item_dict = {
            "key": "000{}".format(i),
            "details": "Item #{} Details".format(i),
        }
        generated_items.append(item_dict)

    return generated_items
```

Create/Update
```python
def create_item(item_):

    """
    Set/Update item in Redis

    Args: 
        item_(dictionary): item 
        to be put/updated in Redis
    """
    
    try:
        item_dict = {
            "key": item_["key"],
            "details": item_["details"],
        }

        json_dict = json.dumps(item_dict)
        item_key = item_["key"]
        r_server.set(item_key, json_dict)
        result = {"status": 1, "message": "Item Created", "item": item_dict}

    except (Exception) as e:
        error = type(e)
        result = {"status": 0, "message": "Error", "error": error}

    return result
```

Read
```python
def get_items(redis_match):

    """
    Get item(s) in Redis

    Args:
        redis_match(str): string for 
        scan match
    """

    cursor_ = 0
    match_ = "{}*".format(redis_match)

    try:
        
        cursor, keys_ = r_server.scan(cursor=cursor_, match=match_)

        r_response = r_server.mget(keys_)
        json_val_list = []
        
        # Jsonify object(s)
        for val_ in r_response:
            json_val = json.loads(val_)
            json_val_list.append(json_val)

        result = json_val_list

    except (Exception) as e:
        error = type(e)
        result = {"status": 0, "message": "Error", "error": error}

    return result
```

Delete
```python
def delete_item(item_):

    """ 
    Delete item in Redis

    Args: 
        item_(dictionary): item 
        to be deleted in Redis
    """

    try:
        item_key = item_["key"]
        r_server.delete(item_key)
        result = {"status": 1, "message": "Item Deleted", "item_key": item_key}

    except (Exception) as e:
        error = type(e)
        result = {"status": 0, "message": "Error", "error": error}

    return result
```

