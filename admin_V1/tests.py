# from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase

from .views import algo_v1
from django.contrib.auth import get_user_model
from institute_V1.models import *

from django.core.management import call_command
import pytest

# Standard imports 
import requests
import sqlite3

# Third party imports
import pytest

@pytest.fixture
def setup_database():
    """ Fixture to set up the in-memory database with test data """
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute('''
	    CREATE TABLE stocks
        (date text, trans text, symbol text, qty real, price real)''')
    sample_data = [
        ('2020-01-01', 'BUY', 'IBM', 1000, 45.0),
        ('2020-01-01', 'SELL', 'GOOG', 40, 123.0),
    ]
    cursor.executemany('INSERT INTO stocks VALUES(?, ?, ?, ?, ?)', sample_data)
    yield conn





pytestmark = pytest.mark.django_db

@pytest.mark.django_db
class TestUsers:
	pytestmark = pytest.mark.django_db
	def test_details(self):
		# Create an instance of a GET request.
		# request = self.factory.get('Admin/table/5/algo/')
		# call_command('loaddata', 'asd.json', verbosity=0)
		print(Division.objects.all())
		me = get_user_model().objects.get(email='Dev@root.com')
		assert me.is_superuser
# class SimpleTest(TestCase):
	
# 	def setUp(self):
# 		# Every test needs access to the request factory.
# 		self.factory = RequestFactory()
# 		# self.user = User.objects.create_user(
# 		#     username='jacob', email='jacob@…', password='top_secret')

# 	@pytest.mark.django_db
# 	def test_details(self):
# 		# Create an instance of a GET request.
# 		request = self.factory.get('Admin/table/5/algo/')
# 		# call_command('loaddata', 'asd.json', verbosity=0)
# 		print(Division.objects.all())
# 		# Recall that middleware are not supported. You can simulate a
# 		# logged-in user by setting request.user manually.
# 		# request.user = get_user_model().objects.all().filter(email="Dev@root.com")

# 		# Test my_view() as if it were deployed at /customer/details
# 		# response = algo_v1(None,5)

# 		# self.assertEqual(response.status_code, 500)