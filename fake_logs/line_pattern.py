import re
from .fake_tokens import FakeTokens


class LinePattern:
	"""Parse a pattern to generate a line inside the logs."""

	patterns = {
		"elf"      : '%h - - [%d %Z] "%m %U %H" %s %b "%R" "%u"',
		"clf"      : '%h - - [%d %Z] "%m %U %H" %s %b',
		"elf-vhost": '%v:%h - - [%d %Z] "%m %U %H" %s %b "%R" "%u"',
		"clf-vhost": '%v:%h - - [%d %Z] "%m %U %H" %s %b'
	}

	def __init__(self, pattern=None, date_pattern=None, file_format="elf", fake_tokens=None):
		self.pattern = self.get_default_format(pattern, file_format)
		self.date_pattern = "%d/%b/%Y:%H:%M:%S" if date_pattern is None else date_pattern
		self._sleep = None
		self.fake_tokens = FakeTokens() if fake_tokens is None else fake_tokens
		self.dispatcher = self.fake_tokens.get_tokens(self.date_pattern)
		self.tokens = []

		tokens_regex = re.compile("%([a-zA-Z]{1})")
		self.line = tokens_regex.sub(self.match_token, self.pattern)

	def get_default_format(self, pattern=None, file_format="elf"):
		"""Return a correct pattern (custom or relative a standard file format)."""
		if pattern is not None:
			return pattern

		if any(file_format in s for s in ["apache", "elf", "lighttpd", "ncsa", "nginx"]):
			file_format = "elf"
		elif any(file_format in s for s in ["clf"]):
			file_format = "clf"

		return self.patterns[file_format]

	@property
	def sleep(self):
		"""Getter to retrieve 'sleep' attribute."""
		return self._sleep

	@sleep.setter
	def sleep(self, sleep):
		"""Setter to update fake_tokens configuration."""
		self._sleep = sleep
		self.fake_tokens.sleep = sleep

	def match_token(self, match):
		"""Register token."""
		key = match.group(1)

		if key not in self.dispatcher:
			raise KeyError("Unsupported key '%{}'".format(key))

		self.tokens.append(self.dispatcher[key])
		return "{}"

	def __iter__(self):
		return iter(self.tokens)

	def create_line(self):
		"""Format a line according to the pattern."""
		values = []
		for get_token in self:
			values.append(get_token())

		return self.line.format(*values)
