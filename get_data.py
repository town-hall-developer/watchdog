from parser import parse

datetime = 'find({status!=200}["2022-11-01 11:18:21", "2021-12-31 01:45:11"], all)'
# print_tokens(datetime)
print(parse(datetime))

def query(str):
    r = parse(datetime)

    where = f""
    datasource = r.get("datasource")


query(datetime)