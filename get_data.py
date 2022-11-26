from parser import parse

datetime = 'find({statusCode=200}["2022-11-01 11:98:21", "2021-12-31 01:45:67"], nginx)'
# print_tokens(datetime)
parse(datetime)