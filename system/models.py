from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext as _


class Company(models.Model):
	'''
	This company model is for storing company data
	from Paranuara planet.
	'''

	index = models.PositiveIntegerField(primary_key=True, unique=True, blank=False, null=False, verbose_name=_("Company index"))
	name = models.CharField(max_length=128, blank=True, null=True, verbose_name=_("Company name"))


	def __unicode__(self):
		return "%s: %s" % (self.index, self.company)

	
class People(models.Model):
	'''
	This people model is for storing people data
	from Paranuara planet
	'''

	_id = models.CharField(max_length=128, unique=True, blank=False, verbose_name=_("People ID"))
	guid = models.CharField(max_length=128, unique=True, blank=False, verbose_name=_("GUID"))
	index = models.PositiveIntegerField(primary_key=True, unique=True, blank=False, null=False, verbose_name=_("People Index"))
	name = models.CharField(max_length=128, blank=True, null=True, verbose_name=_("Name"))
	age = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name=_("Age"))
	has_died = models.BooleanField(default=False, verbose_name="Has this person died")
	balance = models.DecimalField(default=0.0, decimal_places=2, max_digits=32, verbose_name=_("Balance"))
	picture = models.CharField(max_length=256, blank=True, null=True, verbose_name=_("Picture"))
	eye_color = models.CharField(max_length=32, blank=True, null=True, verbose_name=_("Eye Color"))
	gender = models.CharField(max_length=16, blank=True, null=True, verbose_name=_("Gender"))
	company = models.ForeignKey('Company', related_name="company_staffs", blank=True, null=True, verbose_name=_("Company ID"))
	email = models.CharField(max_length=32, blank=True, null=True, verbose_name=_("Email"))
	phone = models.CharField(max_length=32, blank=True, null=True, verbose_name=_("Phone"))
	address = models.CharField(max_length=256, blank=True, null=True, verbose_name=_("Address"))
	about = models.TextField(blank=True, null=True, verbose_name=_("About"))
	registered = models.DateTimeField(blank=True, null=True, verbose_name=_('Registered'))
	tags = models.TextField(blank=True, null=True, verbose_name=_("Tags"))
	favourite_food = models.TextField(blank=True, null=True, verbose_name=_("Favourite Food"))
	favourite_fruit = models.TextField(blank=True, null=True, verbose_name=_("Favourite Fruit"))
	favourite_vegetable = models.TextField(blank=True, null=True, verbose_name=_("Favourite Vegetable"))
	greeting = models.TextField(blank=True, null=True, verbose_name=_("Greeting"))

	def __unicode__(self):
		return "%s" % self._id

	# add a list of new tags to people
	def add_tags(self, new_tags=[]):
		if len(new_tags) > 0:
			for tag in new_tags:
				self.tags = '%s,%s' % (self.tags, tag)
			self.save()

	# return a list of tags
	def get_tags(self):
		if len(self.tags) > 0:
			return self.tags.split(',')
		else:
			return []

	# add a list of new favourite food to people
	def add_favourite_food(self, new_food=[]):
		if len(new_food) > 0:
			for food in new_food:
				self.favourite_food = '%s,%s' % (self.favourite_food, food)
			self.save()

	# return a list of favourite_food
	def get_favourite_food(self):
		if len(self.favourite_food) > 0:
			return self.favourite_food.split(',')
		else:
			return []

	# return a list of favourite fruit
	def get_favourite_fruit(self):
		if len(self.favourite_fruit):
			return self.favourite_fruit.split(',')
		else:
			return []

	# return a list of favourite vegetables
	def get_favourite_vegetables(self):
		if len(self.favourite_vegetable):
			return self.favourite_vegetable.split(',')
		else:
			return []

	# add a friend
	def add_friend(self, other_people_index):
		new_friend = Friend()
		new_friend.people_index = self
		new_friend.friend_index = other_people_index
		new_friend.save()

	# add a list of friends
	def add_friends(self, friend_list):
		if len(friend_list) > 0:
			for friend in friend_list:
				self.add_friend(People.objects.filter(index=friend['index']).first())

	# return a friend list
	def get_all_friends(self):
		return self.friends.all()

	
class Friend(models.Model):
	'''
	This friend model stores the friendship of people.
	Building this model is for easily expanding other
	attributes of friend relationship.
	'''

	people_index = models.ForeignKey('People', related_name='friends', verbose_name=_('People'))
	friend_index = models.ForeignKey('People', verbose_name=_('Friend'))
