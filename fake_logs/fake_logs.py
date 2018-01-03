#!/usr/bin/python
import gzip
import os
import signal
import sys
import time
from .line_pattern import LinePattern


class FakeLogs:
	"""Entrypoint to generate fake logs (into file or stdout)."""

	def __init__(self, filename=None, num_lines=10, file_format="elf", line_pattern=None, sleep=None):
		self.filename = filename
		self.num_lines = num_lines
		self.sleep = sleep
		self.line_pattern = LinePattern(file_format=file_format) if line_pattern is None else line_pattern
		self.line_pattern.sleep = sleep

		if self.num_lines < 0:
			sys.exit("The number of lines cannot be negative '^_^")

		if self.sleep == 0 and self.num_lines == 0:
			sys.exit("Do not use --sleep=0 and --num=0 in the same time '^_^")

		self._init_file()

	def _init_file(self):
		self.file = sys.stdout
		if self.filename is not None:
			dirname = os.path.dirname(self.filename)
			if dirname != "":
				os.makedirs(dirname, exist_ok=True)

			_open = gzip.open if self.filename.lower().endswith(".gz") else open
			self.file = _open(self.filename, "wt")

	def _close_file(self):
		if self.filename is not None:
			self.file.close()

	def run(self):
		"""Main method to generate fake logs."""
		if self.sleep is not None:
			self._write_line_and_sleep()
			return

		for _ in range(0, self.num_lines):
			self._write_line()

		self._close_file()

	def _write_line_and_sleep(self):
		def signal_handler(*_):
			print("Goodbye!")
			self._close_file()
			sys.exit(0)

		signal.signal(signal.SIGINT, signal_handler)
		num_lines = self.num_lines
		infinite  = self.num_lines == 0

		while infinite or num_lines > 0:
			self._write_line(flush=True)
			time.sleep(self.sleep)
			num_lines -= 1

	def _write_line(self, flush=False):
		line = self.line_pattern.create_line()
		print(line, file=self.file, flush=flush)
