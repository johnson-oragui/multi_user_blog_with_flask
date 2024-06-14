from flask import Flask
from views import dashboard, authenticate, comment

app = Flask(__name__)

app.url_map.strict_slashes = False

app.register_blueprint(comment, url_prefix='/comments')
app.register_blueprint(dashboard, url_prefix='/dashboard')
app.register_blueprint(authenticate)

@app.get('/')
def index():
    return f'INDEX'


@app.route('/about')
def about():
    
    return f'<p>about page</p>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
