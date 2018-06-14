from get_items import get_receipt_items
import json

from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from flask import request

app = Flask(__name__)
CORS(app, send_wildcard=True)
api = Api(app)

# lol database
in_memory_python_native_database_item_names = {"BOUNTY SAS" : "Paper towels", "CLIF BAR" : "Peanut Butter Brick"}
inventory = {"Onions" : 5.00, "Chocolate" : 6.50}
policy_info = {"points" : 0, "total_covered" : 20.00}

high_scores = {'Gary' : 100, 'You' : 0, 'Kilroy' : 10, 'Background Character' : 15, 'AAAAAA' : 25}

class Itemizer(Resource):

	def get(self):

		# lol hackday
		from walmart_response import walmart_response
		items = get_receipt_items(walmart_response)
		item_names = [x['item'] for x in items]
		item_values = [x['value'] for x in items]

		matched_items = []
		for item, value in zip(item_names, item_values):

			if item in in_memory_python_native_database_item_names.keys():
				matched_items.append({'name' : in_memory_python_native_database_item_names[item], 'value' : value, 'found' : True, 'original_name' : item})
				high_scores['You'] += 1
			else:
				matched_items.append({'name' : item, 'value' : value, 'found' : False})

		to_send = json.dumps(matched_items)

		return to_send

api.add_resource(Itemizer, '/itemizer')

class Update(Resource):

	def put(self):
		r = request.get_json()
		in_memory_python_native_database_item_names[r['unlabeled']] = r['labeled']

api.add_resource(Update, '/update')

class Scores(Resource):

	def put(self):

		high_scores['You'] += 10

	def get(self):

		rev = {high_scores[x] : x for x in high_scores}

		in_order = sorted(rev.keys(), reverse=True)

		scores = [{'name' : rev[x], 'score' : x} for x in in_order]

		return json.dumps(scores)

api.add_resource(Scores, '/scores')

if __name__ == '__main__':
	app.run(debug=True, port=5001)
