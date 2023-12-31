from functools import wraps
from flask import Flask, request, jsonify
from misc import misc

WHITE_LIST = ['demo3', 'misc.demo5']

app = Flask(__name__)
app.register_blueprint(misc)


def bypass_token_check(f):
    f._bypass_token = True
    return f


@app.before_request
def check_jwt_token():
    bypass = hasattr(
        app.view_functions[request.endpoint],
        '_bypass_token'
    )
    if bypass or request.endpoint in WHITE_LIST:
        return None
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token is missing'}), 403  # maybe 401?
    else:
        pass  # we can do certain further validations here

@app.route('/endpoint1')
@bypass_token_check
def demo1():
    return jsonify({'message': 'You made it'})


@app.route('/endpoint2')
def demo2():
    return jsonify({'message': 'You made it'})


@app.route('/endpoint3')
def demo3():
    return jsonify({'message': 'You made it'})


if __name__ == '__main__':
    app.run(debug=True)
