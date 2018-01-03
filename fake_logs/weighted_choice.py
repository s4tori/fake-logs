import random


class WeightedChoice:
	"""Weighted version of random.choice."""

	def __init__(self, values, weights=None):
		if weights is None:
			weights = [1] * len(values)

		self.choices = [[x, y] for x, y in zip(values, weights)]
		self.total = sum(w for c, w in self.choices)

	def run(self):
		"""Get a random value."""
		rnd = random.uniform(0, self.total)
		upto = 0
		for choice, weight in self.choices:
			if upto + weight >= rnd:
				return choice
			upto += weight
		assert False, "Shouldn't get here."
		return None
