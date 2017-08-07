import json
from decimal import Decimal
from system.models import Company, People
from dateutil import parser
from nltk.corpus import wordnet as wn

# get fruit list from Wordnet
def get_fruit_list():
	fruit = wn.synset('fruit.n.01')
	fruit_list = list(set([w for s in fruit.closure(lambda s:s.hyponyms()) for w in s.lemma_names()]))
	return fruit_list

# get vegetable list from Wordnet
def get_vegetable_list():
	vegetable = wn.synset('vegetable.n.01')
	vegetable_list = list(set([w for s in vegetable.closure(lambda s:s.hyponyms()) for w in s.lemma_names()]))
	return vegetable_list

# importing company data from json file companies.json,
# and save to Company model and database
def import_company_data_from_file():
	datas = None
	with open('./json_files/companies.json', encoding='utf-8') as data_file:
		    datas = json.loads(data_file.read())
	if datas:
		for data in datas:
			company = Company()
			company.index = data['index']
			company.name = data['company']
			company.save()
			print("save company %s" % company.index)


# importing people data from json file people.json
# and save to People model and database
def import_people_data_from_file():
	datas = None
	with open('./json_files/people.json', encoding='utf-8') as data_file:
		    datas = json.loads(data_file.read())
	if datas:
		fruit_list = get_fruit_list()
		vegetable_list = get_vegetable_list()
		for data in datas:
			people = People()
			people._id = data['_id']
			people.guid = data['guid']
			people.index = data['index']
			people.name = data['name']
			people.age = data['age']
			people.has_died = False if data['has_died'] == "false" or data['has_died'] == False else True
			people.balance = Decimal(data['balance'].strip('$').replace(',',''))
			people.picture = data['picture']
			people.eye_color = data['eyeColor']
			people.gender = data['gender']
			people.company = Company.objects.filter(index=data['company_id']).first()
			people.email = data['email']
			people.phone = data['phone']
			people.address = data['address']
			people.about = data['about']
			try:
				people.registered = parser.parse(data['registered'])
			except Exception as e:
				pass
			people.add_tags(data['tags'])
			people.add_favourite_food(data['favouriteFood'])
			for food in data['favouriteFood']:
				if food in fruit_list:
					if people.favourite_fruit:
						people.favourite_fruit = "%s,%s" % (people.favourite_fruit, food)
					else:
						people.favourite_fruit = food

				if food in vegetable_list:
					if people.favourite_vegetable:
						people.favourite_vegetable = "%s,%s" % (people.favourite_vegetable, food)
					else:
						people.favourite_vegetable = food
			people.greeting = data['greeting']
			people.save()
			print("save people %s" % people.index)

		for data in datas:
			people = People.objects.get(index=data['index'])
			people.add_friends(data['friends'])
			print('save friends %s' % data['friends'])
	

