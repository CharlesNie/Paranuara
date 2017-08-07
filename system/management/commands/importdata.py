from django.core.management.base import BaseCommand, CommandError
from system.utils import import_company_data_from_file,import_people_data_from_file


class Command(BaseCommand):
	help = 'Import company/people data from json file'

	def add_arguments(self, parser):
		parser.add_argument('category', nargs='+', type=str)

	def handle(self, *args, **options):
		for c in options['category']:
			if c == 'company':
				import_company_data_from_file()
			elif c == 'people':
				import_people_data_from_file()
			else:
				 raise CommandError("Please provide either 'company' or 'people' argument!")

			self.stdout.write(self.style.SUCCESS('Successfully import %s data' % c))
