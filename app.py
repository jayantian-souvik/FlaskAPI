from flask import Flask
app = Flask(__name__)
from controller.user_controller import user_blueprint

app.register_blueprint(user_blueprint)
# app.register_blueprint(user_blueprint, url_prefix="/user")
# __all__ = ["user_controller", "product_controller"]

@app.route('/')
def index():
    return 'Hello World'

@app.route('/<name>')
def print_name(name):
    return 'Hi , {}'.format(name)


# from controller import product_controller,user_controller
# import controller.user_controller

if __name__ == '__main__':
    app.run(debug=True)
    