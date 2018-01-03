<div align="center">
	<h1>Python Fake Logs</h1>
</div>

This script generates fake logs in various formats ([ELF][elf], [CLF][clf]).
Some options are directly available to help you format log output (see [Options](#options) section below). You can also easily override the script and add your own tokens (see [Custom tokens](#custom-tokens) section).


## Requirement

* Python 3.3+


## Getting Started

```sh
# Install dependencies
pip install -r requirements.txt

# Run fake-logs (with python 3)
python fake-logs.py
```


## Usage

Generate 100 lines to STDOUT (Apache format):
```sh
python fake-logs.py -n 100 -f apache
# 192.30.253.112 - - [02/Jan/2018:20:59:51 +0100] "GET /dolorem/dicta.csv HTTP/1.0" 200 5039 "https://example1.com/" "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_9) AppleWebKit/5351 (KHTML, like Gecko) Chrome/14.0.850.0 Safari/5351"
# 192.30.253.113 - - [02/Jan/2018:21:00:21 +0100] "POST /cupiditate.txt HTTP/1.0" 200 5035 "http://example2.net/register/" "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_7_4; rv:1.9.3.20) Gecko/2013-04-14 01:22:21 Firefox/3.8
# ...
```

Generate 500 log lines (CLF format) into a log file at intervals of 2 seconds:
```sh
python fake-logs.py -n 500 -o myfile.log -s 2 -f clf
# See "myfile.log" file
```

Infinite log file generation with custom format (one line every 50ms to STDOUT):
```sh
python fake-logs.py -n 0 -s 0.5 -p "%m %d" --date-pattern="%H:%M:%S"
# GET 16:40:36
# GET 16:40:36
# POST 16:40:37
# GET 16:40:37
# ...
```

Generate 5 lines with custom format (one line every 1s into a gzip file):
```sh
python fake-logs.py -p "%m %d" -o logs/myfile.log.gz -n 5 -s 1
# See "logs/myfile.log.gz" file
```


## Options

You can use `python fake-logs.py -h` to get all available options.

| Specifier               | Description                                     |
| ----------------------: | :---------------------------------------------- |
| `--output` (`-o`)       | Log output destination (STDOUT if not provided) |
| `--num` (`-n`)          | Number of lines to generate (0 for infinite)    |
| `--sleep` (`-s`)        | Sleep this long between lines (in seconds)      |
| `--format` (`-f`)       | Preconfigured line format (see `-h` option)     |
| `--pattern` (`-p`)      | Custom log pattern                              |
| `--date-pattern` (`-d`) | Custom date pattern                             |
| `--help` (`-h`)         | List all available options                      |


### Custom patterns

The `pattern` option (`-p`) can be used to provide a customizable log format :

| Specifier  | Description                                   | Example             |
| ---------: | :-------------------------------------------- | :------------------ |
| `%b`       | The size of the object returned to the client | 4943                |
| `%d`       | The date (see `date-pattern` option)          | 1970/01/01 00:00:00 |
| `%h`       | The client IP address                         | 192.30.253.112      |
| `%m`       | The request method                            | GET                 |
| `%s`       | The HTTP status code                          | 200                 |
| `%u`       | The user-agent HTTP request header            | Mozilla/5.0 ...     |
| `%v`       | The server name                               | example1            |
| `%H`       | The request protocol                          | HTTP/1.0            |
| `%R`       | The referrer HTTP request header              | https://github.com  |
| `%U`       | The URL path requested                        | file.html           |
| `%Z`       | The current timezone                          | +0100               |

Use the `date-pattern` option to format the `%d` specifier.
See [python documentation](https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior) to specify a valid date pattern.

Examples :

```sh
python fake-logs.py -n 2 -p "%v - %m %s"
# example1 - POST 200
# example2 - GET 200

python fake-logs.py -n 2 -p "%v - %m %s [%d]" -d="%Y | %H:%M:%S"
# example1 - GET 200 [2018 | 17:29:38]
# example1 - POST 404 [2018 | 17:31:51]
```


### Custom tokens

You can override `fake_token` Python class to update an existing specifier or create your own tokens. Check the [examples/custom_tokens.py](./examples/custom_tokens.py) script:

```sh
# Custom method (%m) + new token (%Y)
python examples/custom_tokens.py -n 2 -p '"%m %Y" - %h'
# "PATCH custom1" - 192.30.253.112
# "PATCH custom2" - 192.30.253.113
```

## Resources

* Inspiration : [Fake-Apache-Log-Generator][falg]
* NCSA Common Log Format : [CLF][clf]
* W3C Extended Log Format : [ELF][elf]
* List of specifiers : [Apache][apache], [Nginx][nginx], [Lighttpd][lighttpd], [GoAccess][goaccess]


## License

Fake Logs is [MIT licensed](./LICENSE).


[//]: # (---------------------------------------------------------------------)

[//]: # (Resources)
[falg]:       https://github.com/kiritbasu/Fake-Apache-Log-Generator
[clf]:        https://www.w3.org/Daemon/User/Config/Logging.html#common_logfile_format
[elf]:        https://www.w3.org/TR/WD-logfile.html
[apache]:     https://httpd.apache.org/docs/current/en/mod/mod_log_config.html
[nginx]:     http://nginx.org/en/docs/http/ngx_http_log_module.html#log_format
[goaccess]:   https://goaccess.io/man#custom-log
[lighttpd]:   https://redmine.lighttpd.net/projects/1/wiki/Docs_ModAccesslog
