## Grammars

```
function : datasource_function
         | numeric_datasource_function
         | operator_function

datasource_function : find(condition, DATASOURCE)

numeric_datasource_function : count(condition, DATASOURCE)
operator_function : sum(numeric_datasource_function, numeric_datasource_function)
                  | max(numeric_datasource_function, numeric_datasource_function)
                  | min(numeric_datasource_function, numeric_datasource_function)

condition : { key_value_pair key_value_pair_tail }[datetime, datetime]
key_value_pair : KEY condition_operator VALUE
key_value_pair_tail : , KEY condition_operator VALUE key_value_pair_tail
                    : , KEY condition_operator VALUE
                    : <empty>
                    
datetime : date time
date : YEAR-MONTH-DAY
time : HOUR:MINUTE:SECOND

condition_operator : =                  
                   | =!
                   | =~

```

### Examples

find({statusCode="200"}["2022-11-01 11:00:00", "2022-11-01 11:05:00"], nginx)

find({statusCode=~"200"}["2022-11-01 11:00:00", "2022-11-01 11:05:00"], alb)

count({statusCode="200"}["2022-11-01 11:00:00", "2022-11-01 11:05:00"])

sum(find({statusCode="200"}["2022-11-01 11:00:00", "2022-11-01 11:05:00"], nginx), find({statusCode=~"200"}["2022-11-01 11:00:00", "2022-11-01 11:05:00"], alb))

