from flask import Flask, jsonify
from postgre import postgre
import gmaps

postgre = postgre('', '', '')

app = Flask(__name__)


@app.route("/city/<name>", methods=['GET'])
def cityhotels(name):
    results = postgre.postgre_to_jsonapi("select * from tripadvisor where city='{0}'".format(name))
    if results is None or len(results) == 0:
        return "Ciudad no disponible"
    else:
        return jsonify({'hoteles': results})


if __name__ == '__main__':
    app.run(debug=True)