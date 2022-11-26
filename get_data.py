from parser import parse

datetime = 'find({status!=200}["2022-11-01 11:18:21", "2021-12-31 01:45:11"], all'
# print_tokens(datetime)
print(parse(datetime))


def query(str):
    r = parse(datetime)

    where = f""

    condition = r.get('condition')
    date_condition = condition.get('date')
    start_date_condition = date_condition.get('start')
    start = f"{start_date_condition.get('year')}-{start_date_condition.get('month')}-{start_date_condition.get('day')} {start_date_condition.get('hour')}:{start_date_condition.get('minute')}:{start_date_condition.get('second')}"

    end_date_condition = date_condition.get('start')
    end = f"{end_date_condition.get('year')}-{end_date_condition.get('month')}-{end_date_condition.get('day')} {end_date_condition.get('hour')}:{end_date_condition.get('minute')}:{end_date_condition.get('second')}"

    print(end)

    datasource = r.get("datasource")
    if datasource != 'all':
        where += f" AND datasource='{datasource}'"


query(datetime)
