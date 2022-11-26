## Grammars

```
function : VARIABLE LPAREN condition COMMA VARIABLE RPAREN
condition : field_condition date_condition
field_condition : LBRACKET VARIABLE EQUAL VARIABLE RBRACKET
date_condition : L_SQUARE_BRACKET QUOTE datetime QUOTE COMMA QUOTE datetime QUOTE R_SQUARE_BRACKET 
datetime : VARIABLE HYPHEN VARIABLE HYPHEN VARIABLE VARIABLE COLON VARIABLE COLON VARIABLE
```

### Examples

find({statusCode="200"}["2022-11-01T11:00:00", "2022-11-01T11:05:00"], nginx)

find({statusCode=~"200"}["2022-11-01T11:00:00", "2022-11-01T11:05:00"], alb)

count({statusCode="200"}["2022-11-01T11:00:00", "2022-11-01T11:05:00"])

todo:
sum(find({statusCode="200"}["2022-11-01T11:00:00", "2022-11-01T11:05:00"], nginx), find({statusCode=~"200"
}["2022-11-01 11:00:00", "2022-11-01 11:05:00"], alb))

