from db import fetchall
from parser import parse


def query(str):
    r = parse(str)

    where = f"WHERE "

    condition = r.get('condition')

    # -- Date condition
    date_condition = condition.get('date')
    start_date_condition = date_condition.get('start')
    start = f"{start_date_condition.get('year')}-{start_date_condition.get('month')}-{start_date_condition.get('day')} {start_date_condition.get('hour')}:{start_date_condition.get('minute')}:{start_date_condition.get('second')}"

    end_date_condition = date_condition.get('end')
    end = f"{end_date_condition.get('year')}-{end_date_condition.get('month')}-{end_date_condition.get('day')} {end_date_condition.get('hour')}:{end_date_condition.get('minute')}:{end_date_condition.get('second')}"

    where += f"`timestamp` >= '{start}' AND `timestamp` <= '{end}'"

    # -- Field condition
    field_condition = condition.get('field')
    for f in field_condition:
        field = f.get('key')
        operator = f.get('operator')
        value = f.get('value')

        if operator == "~=":
            where += f" AND `{field}` LIKE '%{value}%'"
        else:
            where += f" AND `{field}` {operator} '{value}'"

    datasource = r.get("datasource")
    if datasource != 'all':
        where += f" AND datasource='{datasource}'"

    sql = f"SELECT * FROM `log_tb` {where}"

    print(sql)

    result = fetchall(sql)
    return result
