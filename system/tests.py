from django.test import TestCase, Client
from system.utils import import_company_data_from_file,import_people_data_from_file

class ParanuaraViewTestBase(TestCase):
	def setUp(self):
		pass

	def test_import_company_data(self):
		import_company_data_from_file()

	def test_import_people_data(self):
		import_people_data_from_file()

	def test_lookup_employee(self):
		c = Client()
		res = c.post('/', {'args':"{'company':'NETBOOK'}"})
		print(res.content)
		self.assertEqual(res.status_code, 200)

	def test_lookup_common_friends(self):
		import_people_data_from_file()
		c = Client()
		res = c.post('/', {'args':"{'people':'Decker Mckenzie,Mindy Beasley'}"})
		print(res.content)
		self.assertEqual(res.status_code, 200)
	
	def test_lookup_favorite_fruit_vegetable(self):
		import_people_data_from_file()
		c = Client()
		res = c.post('/', {'args':"{'people':'Grace Kelly'}"})
		print(res.content)
		self.assertEqual(res.status_code, 200)
