from flask import Flask
from bluoPrint.end_points import crashes_bp

app = Flask(__name__)

app.register_blueprint(crashes_bp)

@app.route('/')
def index():
    return 'Hello to chicago crashes!'



if __name__ == '__main__':
    app.run(debug=True)
