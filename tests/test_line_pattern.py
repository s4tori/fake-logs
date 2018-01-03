import datetime
import unittest
from faker                  import Faker
from fake_logs.fake_tokens  import FakeTokens
from fake_logs.line_pattern import LinePattern
from .util_patch            import patch_rng, patch_random


class TestLinePattern(unittest.TestCase):

	# Create FakeTokens instance
	def setUp(self):
		date = datetime.datetime(2017, 12, 25, 1, 2, 3)
		faker = Faker()
		faker.seed_instance(1337)
		fake_tokens = FakeTokens(faker=faker, date=date, sleep=1)
		self.fake_tokens = fake_tokens

		# Reset faker
		self.fake_tokens.faker.seed_instance(1337)

	@patch_rng(1)
	@patch_random("gauss", 100)
	def test_pattern(self):
		line_pattern = LinePattern("%h [%d] %m %H %s %b", fake_tokens=self.fake_tokens)
		self.assertEqual(line_pattern.create_line(), "211.10.40.110 [25/Dec/2017:01:02:04] PUT HTTP/1.0 301 100")
		self.assertEqual(line_pattern.create_line(), "202.36.16.253 [25/Dec/2017:01:02:05] PUT HTTP/1.0 301 100")

	def test_date(self):
		line_pattern = LinePattern("%H [%d]", fake_tokens=self.fake_tokens, date_pattern="%H-%M-%S")
		self.assertEqual(line_pattern.create_line(), "HTTP/1.0 [01-02-04]")
		self.assertEqual(line_pattern.create_line(), "HTTP/1.0 [01-02-05]")
