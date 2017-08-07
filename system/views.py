import json
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from system.models import Company,People
from system.forms import ParanuaraForm
from django.db.models import Q


class ParanuaraView(TemplateView):
	'''
	This paranuara view will handle given company/people arguments,
	than process with specific request and return json result to user.
	'''

	template_name = 'paranuara.html'

	# this function will return a form instance including attributes for 
	# user to input arguments such as company name and people name
	def get_paranuara_form(self):
		if self.request.method == 'POST':
			return ParanuaraForm(self.request.POST)
		else:
			return ParanuaraForm()

	# this function is for searching all employees with given company name
	def get_all_employees(self, company_list):
		companies = Company.objects.filter(name__in=company_list)
		employee_list = People.objects.filter(company__in=companies)
		if len(employee_list) > 0:
			all_employees = []
			for company in companies:
				company_employee = {}
				company_employee['company'] = company.name
				employees = []
				for employee in employee_list.filter(company=company):
					employees.append({'index':employee.index, 'name':employee.name})
				company_employee['employees'] = employees
				all_employees.append(company_employee)
			return all_employees
		else:
			return [{'company':'', 'employees':[{}]}]

	# this function is for searching fruits and vegetables people like
	def get_fruits_and_vegetables(self, given_people_name):
		people = People.objects.filter(name=given_people_name).first()
		if people:
			return {"username":people.name, "age":people.age, "fruits":people.get_favourite_fruit(),
					"vegetables":people.get_favourite_vegetables()}
		return {"username":"", "age":"", "fruits":[], "vegetables":[]}

	# this function is for searching common friends of people
	def get_common_friends(self, given_people_list):
		people_list = People.objects.filter(name__in = given_people_list)
		results = []
		for people in people_list:
			people_info = {'name':people.name, 'age':people.age, 'address':people.address,
					'phone':people.phone, 'friends':[]}
			all_friends = people.get_all_friends().values('friend_index').distinct()
			for other_people in people_list:
				if other_people.index in [value['friend_index'] for value in all_friends]:
					common_friends = []
					other_people_s_friends = other_people.friends.filter(friend_index__has_died=False,
							friend_index__eye_color="brown").values('friend_index').distinct()
					for friend in all_friends.filter(friend_index__in=other_people_s_friends):
						common_friends.append({'index':friend['friend_index']})
					people_info['friends'].append({'index':other_people.index, 'common_friends':common_friends})
			results.append(people_info)
		return results

	# this function is for updating the form and pass on to GET request
	def get_context_data(self, **kwargs):
		ctx = super(ParanuaraView, self).get_context_data(**kwargs)
		ctx.update({'form':self.get_paranuara_form()})
		return ctx

	# this function is for getting POST data and processing data, then
	# return a set of json data
	def post(self, *args, **kwargs):
		try:
			form = self.get_paranuara_form()
			if form.is_valid():
				# get the option to determine if it is company
				# name argument or people argument
				args = form.cleaned_data['args']
				if len(args) > 0:
					# convert arg string to dictionary
					from ast import literal_eval
					args_dict = literal_eval(args)

					# processing given company name scenario
					if 'company' in args_dict.keys():
						values = args_dict['company'].split(',')
						if len(values) > 0:
							employees = self.get_all_employees(values)
							if employees:
								return JsonResponse(employees, safe=False)
							else:
								return JsonResponse({"result":"No records"})

					# processing given people name scenario
					if 'people' in args_dict.keys():
						values = args_dict['people'].split(',')
						if len(values) == 0:
							return JsonResponse({'Error':'Please provide valid argument.'})
						
						# if given 1 people name, then return favorite fruits and vegetables
						elif len(values) == 1:
							fv_list = self.get_fruits_and_vegetables(values[0])
							if fv_list:
								return JsonResponse(fv_list, safe=False)
							else:
								return JsonResponse({"result":"No records"})
						
						# if given more than 1 people name, then return their common friends
						else:
							common_friends = self.get_common_friends(values)
							if common_friends:
								return JsonResponse(common_friends, safe=False)
							else:
								return JsonResponse({"result":"No records"})

			return JsonResponse({'Error':'Please provide valid argument.'})

		except Exception as e:
			return JsonResponse({'Error':str(e)})
