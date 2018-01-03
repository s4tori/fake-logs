import unittest
from fake_logs.weighted_choice import WeightedChoice
from .util_patch               import patch_rng


class TestWeightedChoice(unittest.TestCase):

	@unittest.skip
	def test_default(self):
		els = [1, 3, 5]
		choices = WeightedChoice(els)
		self.assertIn(choices.run(), els)

	@unittest.skip
	def test_no_choices(self):
		choices = WeightedChoice(["a", "b", "c"], [0, 0, 0])
		self.assertEqual(choices.run(), "a")

	@unittest.skip
	def test_one_choice(self):
		choices = WeightedChoice([1, 3, 5], [0, 1, 0])
		self.assertEqual(choices.run(), 3)

	@unittest.skip
	def test_two_choices(self):
		choices = WeightedChoice(["a", "b", "c"], [0, 1, 1])
		self.assertIn(choices.run(), ["b", "c"])
		self.assertNotEqual(choices.run(), "d")

	@unittest.skip
	def test_three_choices(self):
		choices = WeightedChoice(["α", "Δ", "Ω"], [1, 1, 1])
		self.assertIn(choices.run(), ["α", "Δ", "Ω"])
		self.assertNotEqual(choices.run(), "π")

	@patch_rng(10)
	def test_force_first_choice(self):
		choices = WeightedChoice([1, 2, 3], [10, 20, 30])
		self.assertEqual(choices.run(), 1)

	@patch_rng(11)
	def test_force_second_choice(self):
		choices = WeightedChoice([1, 2, 3], [10, 20, 30])
		self.assertEqual(choices.run(), 2)

	@patch_rng(30)
	def test_force_second_choice_again(self):
		choices = WeightedChoice([1, 2, 3], [10, 20, 30])
		self.assertEqual(choices.run(), 2)

	@patch_rng(31)
	def test_force_third_choice(self):
		choices = WeightedChoice([1, 2, 3], [10, 20, 30])
		self.assertEqual(choices.run(), 3)

	@patch_rng(1000)
	def test_force_error(self):
		with self.assertRaises(AssertionError):
			choices = WeightedChoice([1, 2, 3], [10, 20, 30])
			self.assertEqual(choices.run(), 1)
