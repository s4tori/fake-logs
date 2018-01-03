# pylint: disable=C0103
import argparse
from fake_logs.fake_logs    import FakeLogs
from fake_logs.line_pattern import LinePattern


parser = argparse.ArgumentParser(description="Fake logs")
parser.add_argument("--output"      , "-o", dest="output"      , help="output destination (.gz extension supported, STDOUT if not provided)" , type=str)
parser.add_argument("--num"         , "-n", dest="num_lines"   , help="Number of lines to generate (0 for infinite)", type=int, default=10)
parser.add_argument("--sleep"       , "-s", dest="sleep"       , help="Sleep this long between lines (in seconds)"  , type=float, default=None)
parser.add_argument("--format"      , "-f", dest="format"      , help="Line format", choices=["apache", "nginx", "lighttpd", "elf", "clf", "ncsa"], type=str, default="elf")
parser.add_argument("--pattern"     , "-p", dest="pattern"     , help="Custom pattern", type=str, default=None)
parser.add_argument("--date-pattern", "-d", dest="date_pattern", help="Date pattern", type=str, default=None)
args = parser.parse_args()

def run_from_cli(fake_tokens=None):
	"""Parse command-line options and run 'Fake Logs'."""
	line_pattern = LinePattern(args.pattern, date_pattern=args.date_pattern, file_format=args.format, fake_tokens=fake_tokens)
	FakeLogs(
		filename=args.output,
		num_lines=args.num_lines,
		sleep=args.sleep,
		line_pattern=line_pattern,
		file_format=args.format
	).run()
