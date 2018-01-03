import datetime
import unittest
from faker                 import Faker
from fake_logs.fake_tokens import FakeTokens
from .util_patch           import patch_rng, patch_random


class TestFakeTokens(unittest.TestCase):

	# Create FakeTokens instance
	def setUp(self):
		date = datetime.datetime(2017, 12, 25, 1, 2, 3)
		faker = Faker()
		faker.seed_instance(1337)
		fake_tokens = FakeTokens(faker=faker, date=date, sleep=1)
		self.fake_tokens = fake_tokens

		# Reset faker
		self.fake_tokens.faker.seed_instance(1337)

	def test_date(self):
		self.assertEqual(self.fake_tokens.run_token("d"), "25/Dec/2017:01:02:04")
		self.assertEqual(self.fake_tokens.run_token("d"), "25/Dec/2017:01:02:05")

	def test_host(self):
		self.assertEqual(self.fake_tokens.run_token("h"), "211.10.40.110")
		self.assertEqual(self.fake_tokens.run_token("h"), "202.36.16.253")

	@patch_rng(1)
	def test_method(self):
		self.assertEqual(self.fake_tokens.run_token("m"), "PUT")
		self.assertEqual(self.fake_tokens.run_token("m"), "PUT")

	def test_protocol(self):
		self.assertEqual(self.fake_tokens.run_token("H"), "HTTP/1.0")
		self.assertEqual(self.fake_tokens.run_token("H"), "HTTP/1.0")

	def test_referrer(self):
		self.assertEqual(self.fake_tokens.run_token("R"), "https://www.willis.biz/tag/category/categories/terms.htm")
		self.assertEqual(self.fake_tokens.run_token("R"), "http://www.hoover-ross.com/login.php")

	@patch_random("choice", "example1")
	def test_server_name(self):
		self.assertEqual(self.fake_tokens.run_token("v"), "example1")
		self.assertEqual(self.fake_tokens.run_token("v"), "example1")

	@patch_random("gauss", 100)
	def test_size_object(self):
		self.assertEqual(self.fake_tokens.run_token("b"), 100)
		self.assertEqual(self.fake_tokens.run_token("b"), 100)

	@patch_rng(1)
	def test_status_code(self):
		self.assertEqual(self.fake_tokens.run_token("s"), "301")
		self.assertEqual(self.fake_tokens.run_token("s"), "301")

	def test_timezone(self):
		self.assertRegex(self.fake_tokens.run_token("Z"), r"(-|\+)[0-9]+")
		self.assertRegex(self.fake_tokens.run_token("Z"), r"(-|\+)[0-9]+")

	@patch_random("choice", "file")
	def test_url_request(self):
		self.assertEqual(self.fake_tokens.run_token("U"), "file")
		self.assertEqual(self.fake_tokens.run_token("U"), "file")

	@patch_rng(1)
	def test_user_agent(self):
		self.assertIn("Opera/", self.fake_tokens.run_token("u"))
		self.assertIn("Opera/", self.fake_tokens.run_token("u"))
