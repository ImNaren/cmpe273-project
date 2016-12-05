from flask import Flask
from flask import request
from model import db
from model import Location_API
from model import CreateDB
from model import app as application
import simplejson as json
from sqlalchemy.exc import IntegrityError
import os
import requests
import google_coordinates


app = Flask(__name__)

@app.route('/')
def homepage():
	return " Welcome to the Location api application, feel free to add your trip locations "

@app.route('/locations', methods=['POST'])
def post():
	try:
		data = json.loads(request.data)
		if not data or not 'name' in data:
			abort(404)
		database = CreateDB(hostname = 'mysqlserver')
		db.create_all()
		coordinate = google_coordinates.address_to_cordinate(data['address']+ data['city'] + data['state'] + data) 
		new_location = Location_API(data['name'], data['email'], data['category'], data['description'], data['link'], data['estimated_costs'], data['submit_date'])
		db.session.add(new_expense)
		db.session.commit()
		added_expense = {'id': new_expense.id, 'name': new_expense.name, 'email': new_expense.email, 'category': new_expense.category, 'description': new_expense.description, 'link': new_expense.link, 'estimated_costs': new_expense.estimated_costs, 'submit_date': new_expense.submit_date, 'status': new_expense.status, 'decision_date': new_expense.decision_date}
		return json.dumps(added_expense), 201

	except IntegrityError:
		return json.dumps({'status':False})

@app.route('/v1/expenses', methods=['GET'])
def get_all_expenses():
	try:
		expenses = Expense.query.all()
		expense_details = {}
		for expense in expenses:
			expense_details[expense.id] = {'id': expense.id, 'name': expense.name, 'email': expense.email, 'category': expense.category, 'description': expense.description, 'link': expense.link, 'estimated_costs': expense.estimated_costs, 'submit_date': expense.submit_date, 'status': expense.status, 'decision_date': expense.decision_date}

		return json.dumps(expense_details)

	except IntegrityError:
		return json.dumps({'status':False})

@app.route('/v1/expenses/<expense_id>',methods =['GET'])
def get_expenseID(expense_id):
	try:
		expense = Expense.query.filter_by(id=expense_id).first_or_404()
		return json.dumps({'id': expense.id, 'name': expense.name, 'email': expense.email, 'category': expense.category, 'description': expense.description, 'link': expense.link, 'estimated_costs': expense.estimated_costs, 'submit_date': expense.submit_date, 'status': expense.status, 'decision_date': expense.decision_date})
	except IntegrityError:
		return json.dumps({'status':False})

@app.route('/v1/expenses/<expense_id>',methods=['PUT'])
def update_expenseID(expense_id):
	try:
		expense_data = json.loads(request.data)
		expense = Expense.query.get(expense_id)
		expense.estimated_costs = expense_data['estimated_costs']
		db.session.commit()
		return json.dumps("Accepted"),202

	except IntegrityError:
		return json.dumps({'status':False})

@app.route('/v1/expenses/<int:expense_id>',methods=['DELETE'])
def delete_expense(expense_id):
	db.session.delete(Expense.query.get(expense_id))
        db.session.commit()
        return json.dumps({}),204

@app.route('/createdb')
def createDatabase():
	HOSTNAME = 'localhost'
	try:
		HOSTNAME = request.args['hostname']
	except:
		pass
	database = CreateDB(hostname = HOSTNAME)
	return json.dumps({'status':True})

@app.route('/info')
def app_status():
	return json.dumps({'server_info':application.config['SQLALCHEMY_DATABASE_URI']})

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=6000, debug=True)

