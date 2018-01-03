from unittest.mock import patch


# Decorator returning a @patch decorator
# Or use @patch directly
# @mock.patch("fake_logs.weighted_choice.random.uniform", return_value=10)
# def test_my_test(self, _):
def patch_rng(return_value):
	"""Decorator returning a @patch decorator for 'fake_logs.weighted_choice'."""
	def decorator(fn):
		def decorated(self):
			with patch("fake_logs.weighted_choice.random.uniform", return_value=return_value):
				return fn(self)
		return decorated
	return decorator

# Decorator returning a @patch decorator for "random.<method> (choice, gauss, etc)"
# Or use @patch directly
# @patch("random.<method>", return_value="<value>")
# def test_my_test(self, _):
def patch_random(method, return_value):
	"""Decorator returning a @patch decorator for 'random.<method>'."""
	def decorator(fn):
		def decorated(self):
			with patch("random." + method, return_value=return_value):
				return fn(self)
		return decorated
	return decorator
