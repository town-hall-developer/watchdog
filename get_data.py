from parser import parse

datetime = 'find({statusCode=200}["2022-11-01 11:18:21", "2021-12-31 01:45:11"], db)'
# print_tokens(datetime)
print(parse(datetime))