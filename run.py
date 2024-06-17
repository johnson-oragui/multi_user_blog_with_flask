from app import flask_app


if __name__ == '__main__':
    app = flask_app()
    app.run(host='0.0.0.0', port=5000, debug=True)