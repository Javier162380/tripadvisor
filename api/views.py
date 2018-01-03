from flask_restful import abort,Resource, marshal
from postgre import postgre
from flask import jsonify,session
from flask_httpauth import HTTPBasicAuth
from response import *

postgre = postgre('', '', '')
auth = HTTPBasicAuth()



@auth.verify_password
def verify_credentials(username,password):
    credentials = postgre.postgre_to_output("select username,password from login", output='login')
    if username in credentials.keys():
        if password == credentials[username]:
            return True
        else:
            return False
    return False

class cities(Resource, metho):
    @auth.login_required
    def get(self,):
        cities = postgre.postgre_to_output("select distinct city from tripadvisor", output='jsonapi')
        return marshal(cities,city_fields),200
class City(Resource):
    @auth.login_required
    def get(self, name):
        cities = postgre.postgre_to_output("select distinct city from tripadvisor", output='tuple')
        if name not in cities:
            abort(404, message="La ciudad {} no tiene registros ".format(name))
        else:
            pass
        results = postgre.postgre_to_output("select * from tripadvisor where city='{0}'".format(name),
                                            output='jsonapi')
        number_of_hotels = postgre.postgre_to_output("select count(*) from tripadvisor where city='{0}'".format(name),
                                                     output='jsonapi')
        return jsonify({'hoteles': results, 'number_of_hotels': number_of_hotels})

class Prices(Resource):
    @auth.login_required
    def get(self,name,min_price,max_price=None):
        cities = postgre.postgre_to_output("select distinct city from tripadvisor", output='tuple')
        if name not in cities:
            abort(404, message="La ciudad {} no tiene registros ".format(name))
        else:
            pass

        results = postgre.postgre_to_output("select * from tripadvisor where city='{0}'and min_price>={1}"
                                            " and max_price<={2}".format(name,min_price,max_price),
                                            output='jsonapi')
        return marshal(results, prices_fields),200
class Hotel(Resource):
    @auth.login_required
    def get(self, name):
        results = postgre.postgre_to_output("select * from tripadvisor where name='{0}'".format(name),
                                            output='jsonapi')
        if len(results)>0:
            return jsonify({'hoteles': results})
        else:
            abort(404, message="La ciudad {} no tiene registros ".format(name))