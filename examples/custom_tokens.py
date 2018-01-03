# pylint: disable=C0103
import sys
import os
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from fake_logs.fake_logs_cli import run_from_cli
from fake_logs.fake_tokens   import FakeTokens


class CustomFakeTokens(FakeTokens):
	"""Override FakeTokens class to update or add custom tokens."""

	def __init__(self, *args):
		FakeTokens.__init__(self, *args)
		self.register_token("Y", self.init_custom())

	# Override existing "method" token
	def init_method(self):
		"""Return the request method (%m)."""
		return lambda: "PATCH"

	# Create a new token (don't forget to call "register_token" in the constructor)
	def init_custom(self):
		"""Return a custom token (%Y)."""
		choices = ["custom1", "custom2"]
		return lambda: random.choice(choices)


# python examples/new_tokens.py -p '"%m %Y" - %h'
run_from_cli(fake_tokens=CustomFakeTokens())
