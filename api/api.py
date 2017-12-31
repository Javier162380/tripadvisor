from flask import Flask
from flask_restful import Api
from views import *


app = Flask(__name__)
api = Api(app)

api.add_resource(City, '/city/<name>')
api.add_resource(Prices,'/city/<name>&min_price=<min_price>&max_price=<max_price>')
api.add_resource(Hotel,'/hotel/<name>')

if __name__ == '__main__':
    app.run(debug=True)