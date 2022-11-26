## Grammars

```
function : VARIABLE LPAREN condition COMMA VARIABLE RPAREN
condition : field_condition date_condition
field_condition : LBRACKET key_value_pair key_value_pair_tail RBRACKET
field_condition : empty
key_value_pair_tail : COMMA key_value_pair key_value_pair_tail
key_value_pair_tail : empty
key_value_pair : VARIABLE operator VARIABLE
operator : EQUAL
operator : BANG EQUAL
operator : TILDE EQUAL
date_condition : L_SQUARE_BRACKET QUOTE datetime QUOTE COMMA QUOTE datetime QUOTE R_SQUARE_BRACKET 
datetime : VARIABLE HYPHEN VARIABLE HYPHEN VARIABLE VARIABLE COLON VARIABLE COLON VARIABLE
```

### Examples

find({statusCode="200"}["2022-11-01T11:00:00", "2022-11-01T11:05:00"], nginx)

find({statusCode=~"200"}["2022-11-01T11:00:00", "2022-11-01T11:05:00"], alb)



TODO:

- 없는 필드 처리