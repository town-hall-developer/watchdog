from exception import DateTimeFormatException, InvalidFunctionException, InvalidDatasourceException
from ply.lex import lex

# --- Tokenizer
from ply.yacc import yacc
from utils import str_to_datetime

tokens = (
    'VARIABLE',
    'HYPHEN',
    'COLON',
    'COMMA',
    'QUOTE',
    'LPAREN',
    'RPAREN',
    'LBRACKET',
    'RBRACKET',
    'L_SQUARE_BRACKET',
    'R_SQUARE_BRACKET',
    'EQUAL',

    'DATETIME_SEPERATOR',
)

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

t_VARIABLE = r'[a-zA-Z0-9_]+'
t_HYPHEN = r'-'
t_COLON = r':'
t_COMMA = r','
t_QUOTE = r'\"'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\{'
t_RBRACKET = r'\}'
t_L_SQUARE_BRACKET = r'\['
t_R_SQUARE_BRACKET = r'\]'
t_EQUAL = r'='
t_DATETIME_SEPERATOR = r'@'

lexer = lex()


def print_tokens(data):
    # Give the lexer some input
    lexer.input(data)

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        print(tok)


# --- Parser
def p_function(p):
    '''
    function : VARIABLE LPAREN condition COMMA VARIABLE RPAREN
    '''
    if p[1] not in ('find', ):
        raise InvalidFunctionException(f'InvalidFunctionException: Unknown function: {p[1]}')

    if p[5] not in ('nginx', 'alb', ):
        raise InvalidDatasourceException(f'InvalidDatasourceException: Unknown datasource: {p[5]}')

    p[0] = {
        'function': p[1],
        'condition': p[3],
        'datasource': p[5],
    }


def p_condition(p):
    '''
    condition : field_condition date_condition
    '''
    p[0] = {
        'field': p[1],
        'date': p[2],
    }


def p_field_condition(p):
    '''
    field_condition : LBRACKET key_value_pair key_value_pair_tail RBRACKET
    '''
    if p[3] == None:
        p[0] = [p[2]]
    else:
        p[0] = [p[2], *p[3]]


def p_empty(p):
    'empty :'
    pass


def p_key_value_pair_tail_empty(p):
    '''
    key_value_pair_tail : empty
    '''
    p[0] = p[0]


def p_key_value_pair_tail(p):
    '''
    key_value_pair_tail : COMMA key_value_pair
    '''
    p[0] = p[1]


def p_key_value_pair_tail_tail(p):
    '''
    key_value_pair_tail : COMMA key_value_pair key_value_pair_tail
    '''
    if p[3] == None:
        p[0] = [p[2]]
    else:
        p[0] = [p[2], *p[3]]


def p_key_value_pair(p):
    '''
    key_value_pair : VARIABLE EQUAL VARIABLE
    '''
    p[0] = {
        'key': p[1],
        'value': p[3],
    }


def p_date_condition(p):
    '''
    date_condition : L_SQUARE_BRACKET QUOTE datetime QUOTE COMMA QUOTE datetime QUOTE R_SQUARE_BRACKET
    '''
    p[0] = {
        'start': p[3],
        'end': p[7],
    }


def p_datetime(p):
    '''
    datetime : VARIABLE HYPHEN VARIABLE HYPHEN VARIABLE VARIABLE COLON VARIABLE COLON VARIABLE
    '''
    try:
        dt = str_to_datetime(f"{p[1]}-{p[3]}-{p[5]} {p[6]}:{p[8]}:{p[10]}")
    except ValueError:
        raise DateTimeFormatException(
            f'DateTimeFormatException: Invalid datetime format. Expected format: "%Y-%m-%d %H:%M:%S". Actual input: {p[1]}-{p[3]}-{p[5]} {p[6]}:{p[8]}:{p[10]}')

    p[0] = {
        'year': p[1],
        'month': p[3],
        'day': p[5],
        'hour': p[6],
        'minute': p[8],
        'second': p[10],
    }


# Build the parser
parser = yacc()


def parse(str):
    errMessage = ""
    try:
        r = parser.parse(str)
        return r
    except Exception as e:
        return {
            "error": e.message
        }
