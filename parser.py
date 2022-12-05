from exception import DateTimeFormatException, InvalidFunctionException, InvalidDatasourceException, SyntaxError, \
    TokenizeError
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
    'BANG',
    'TILDE',
)

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

t_VARIABLE = r'[a-zA-Z0-9_./]+'
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
t_BANG = r'!'
t_TILDE = r'~'


def t_error(t):
    raise TokenizeError(f"TokenizeError: Illegal character '{t.value[0]}'")


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


def p_field_condition_empty(p):
    '''
    field_condition : empty
    '''
    p[0] = []


def p_key_value_pair_tail_tail(p):
    '''
    key_value_pair_tail : COMMA key_value_pair key_value_pair_tail
    '''
    if p[3] == None:
        p[0] = [p[2]]
    else:
        p[0] = [p[2], *p[3]]


def p_key_value_pair_tail_empty(p):
    '''
    key_value_pair_tail : empty
    '''
    p[0] = p[0]


def p_key_value_pair(p):
    '''
    key_value_pair : VARIABLE operator VARIABLE
    '''
    p[0] = {
        'key': p[1],
        'operator': p[2],
        'value': p[3],
    }


def p_operator_equal(p):
    '''
    operator : EQUAL
    '''
    p[0] = p[1]


def p_operator_not_equal(p):
    '''
    operator : BANG EQUAL
    '''
    p[0] = f"{p[1]}{p[2]}"


def p_operator_contains(p):
    '''
    operator : TILDE EQUAL
    '''
    p[0] = f"{p[1]}{p[2]}"


def p_operator_not_contains(p):
    '''
    operator : BANG TILDE EQUAL
    '''
    p[0] = f"{p[1]}{p[2]}{p[3]}"


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

    p[0] = {
        'year': p[1],
        'month': p[3],
        'day': p[5],
        'hour': p[6],
        'minute': p[8],
        'second': p[10],
    }


def p_empty(p):
    'empty :'
    pass


def p_error(p):
    raise SyntaxError(f'SyntaxException: Syntax error at {p.value!r}')


# Build the parser
parser = yacc()


def parse(str):
    try:
        r = parser.parse(str)
    except (SyntaxError, TokenizeError,) as e:
        return {
            "status": "fail",
            "errors": [{
                "error": e.message
            }]
        }
    except Exception as e:
        return {
            "status": "fail",
            "errors": [{
                "error": f"SyntaxError: Your input: {str}"}]
        }

    errs = errors(r)
    if len(errs) == 0:
        r["status"] = "success"
        return r
    else:
        return {
            "status": "fail",
            "errors": errs
        }


def errors(parseTree):
    errors = []

    function = parseTree.get("function")

    if function not in ('find', 'count'):
        errors.append({
            "error": f"InvalidFunctionException: Unknown function: {function}"
        })

    datasource = parseTree.get("datasource")
    if datasource not in ('nginx', 'alb', 'all',):
        errors.append({
            "error": f"InvalidDatasourceException: Unknown datasource: {datasource}"
        })

    start = parseTree.get("condition").get("date").get("start")

    isStart = False
    isEnd = False
    try:
        startDt = str_to_datetime(
            f"{start.get('year')}-{start.get('month')}-{start.get('day')} {start.get('hour')}:{start.get('minute')}:{start.get('second')}")
        isStart = True
    except Exception as e:
        errors.append({
            "error": f"DateTimeFormatException: Invalid start datetime format. Your input: {start.get('year')}-{start.get('month')}-{start.get('day')} {start.get('hour')}:{start.get('minute')}:{start.get('second')}"
        })

    end = parseTree.get("condition").get("date").get("end")
    try:
        endDt = str_to_datetime(
            f"{end.get('year')}-{end.get('month')}-{end.get('day')} {end.get('hour')}:{end.get('minute')}:{end.get('second')}")
        isEnd = True
    except Exception as e:
        errors.append({
            "error": f"DateTimeFormatException: Invalid end datetime format. Your input: {end.get('year')}-{end.get('month')}-{end.get('day')} {end.get('hour')}:{end.get('minute')}:{end.get('second')}"
        })

    if (isStart and isEnd):
        if endDt < startDt:
            errors.append({
                "error": f"DateTimeException: start datetime should be faster than the end datetime."
            })

    return errors
