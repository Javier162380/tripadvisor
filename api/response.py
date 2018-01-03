from flask_restful import fields

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

city_fields={

    'city':fields.String
}
