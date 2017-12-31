from flask_restful import abort,Resource, marshal,fields
from postgre import postgre
from flask import jsonify

postgre = postgre('', '', '')

prices_fields = {
    'name': fields.String,
    'city': fields.String,
    'min_price': fields.Integer,
    'max_price': fields.Integer,
    'stars': fields.String,
    'url': fields.Url('hotel',absolute=True)
    }
prices_fields['location']={}
prices_fields['location']['full_address'] = fields.String(attribute='address')
prices_fields['location']['zip_code'] = fields.String(attribute='zipcode')
prices_fields['location']['coordinates'] = {}
prices_fields['location']['coordinates']['latitude'] = fields.Float(attribute='latitude')
prices_fields['location']['coordinates']['longitude'] = fields.Float(attribute='longitude')

class City(Resource):

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
    def get(self,name):
        results = postgre.postgre_to_output("select * from tripadvisor where name='{0}'".format(name),
                                            output='jsonapi')
        if len(results)>0:
            return jsonify({'hoteles': results})
        else:
            abort(404, message="La ciudad {} no tiene registros ".format(name))