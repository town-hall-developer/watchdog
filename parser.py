from ply.lex import lex

# --- Tokenizer
from ply.yacc import yacc

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
    function : VARIABLE LPAREN condition RPAREN
    '''
    p[0] = {
        'function': p[1],
        'condition': p[3],
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
    field_condition : LBRACKET VARIABLE EQUAL VARIABLE RBRACKET
    '''
    p[0] = {
        'key': p[2],
        'value': p[4],
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
    datetime : VARIABLE HYPHEN VARIABLE HYPHEN VARIABLE DATETIME_SEPERATOR VARIABLE COLON VARIABLE COLON VARIABLE
    '''
    p[0] = {
        'year': p[1],
        'month': p[3],
        'day': p[5],
        'hour': p[7],
        'minute': p[9],
        'second': p[11],
    }


# Build the parser
parser = yacc()


def parse(str):
    r = parser.parse(str)
    print(r)


datetime = 'find({statusCode=200}["2022-11-01@11:98:21", "2021-12-31@01:45:67"])'
# print_tokens(datetime)
parse(datetime)
