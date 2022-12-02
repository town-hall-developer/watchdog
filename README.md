# Parser

## How to run

```bash
uvicorn main:app --reload --port 8000
```

## Endpoint

- /parse
- /query

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
operator : BANG TILDE EQUAL
date_condition : L_SQUARE_BRACKET QUOTE datetime QUOTE COMMA QUOTE datetime QUOTE R_SQUARE_BRACKET 
datetime : VARIABLE HYPHEN VARIABLE HYPHEN VARIABLE VARIABLE COLON VARIABLE COLON VARIABLE
```

### Examples

find({status=200}["2022-11-01 11:00:00", "2022-11-01 11:05:00"], nginx)

find({status!~=200}["2022-11-01 11:00:00", "2022-11-01 11:05:00"], alb)


## Environments

- WATCHDOG_DATABASE_HOST
- WATCHDOG_DATABASE_USER
- WATCHDOG_DATABASE_PASSWORD
- WATCHDOG_DATABASE_NAME
- WATCHDOG_DATABASE_PORT

# Cron

## How to run

```bash
python main_cron.py
```

## Environments

- WATCHDOG_DATABASE_HOST
- WATCHDOG_DATABASE_USER
- WATCHDOG_DATABASE_PASSWORD
- WATCHDOG_DATABASE_NAME
- WATCHDOG_DATABASE_PORT
- AWS_DEFAULT_REGION
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_ACCOUNT_ID