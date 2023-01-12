# -----------------------------------------------------------------------------
# calc.py
#
# Expressions arithmétiques sans variables
# -----------------------------------------------------------------------------
reserved = {
    'print': 'PRINT'
}

tokens = [
             'NUMBER', 'MINUS',
             'PLUS', 'TIMES', 'DIVIDE',
             'LPAREN', 'RPAREN', 'AND', 'OR', 'SEMICOLON', 'NAME', 'EQUAL', 'EQUALEQUAL',
             'INFERIOR', 'SUPERIOR', 'INFERIOR_EQUAL', 'SUPERIOR_EQUAL', 'DIFFERENT', "DOUBLEQUOTE", "STRING"
         ] + list(reserved.values())

# Tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_AND = r'\&'
t_OR = r'\|'
t_SEMICOLON = r';'
t_EQUAL = r'='
t_INFERIOR = r'<'
t_SUPERIOR = r'>'
t_INFERIOR_EQUAL = r'<='
t_SUPERIOR_EQUAL = r'>='
t_DIFFERENT = r'!='
t_EQUALEQUAL = r'=='
t_PRINT = r'print'
t_DOUBLEQUOTE = r'\"'

names = {}


def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9_]*'
    t.type = reserved.get(t.value, 'NAME')
    return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_STRING(t):
    r'\".*\"'
    t.value = str(t.value)
    t.type = reserved.get(t.value, 'STRING')
    return t


# Ignored characters
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
import ply.lex as lex

lex.lex()


def p_bloc(p):
    '''START : START statement SEMICOLON
            | statement SEMICOLON'''


def p_statement_expr(p):
    'statement : expression'
    # print(p[1]) # Just for debug


def p_expression_binop_plus(p):
    'expression : expression PLUS expression'
    p[0] = p[1] + p[3]


def p_expression_binop_times(p):
    'expression : expression TIMES expression'
    p[0] = p[1] * p[3]


def p_expression_binop_divide_and_minus(p):
    '''expression : expression MINUS expression
				| expression DIVIDE expression'''
    if p[2] == '-':
        p[0] = p[1] - p[3]
    else:
        p[0] = p[1] / p[3]


def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]


def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]


def p_expression_name(p):
    'expression : NAME'
    try:
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined name '%s'" % p[1])


def p_expression_string(p):
    'expression : STRING'
    p[0] = p[1]


def p_expression_binop_bool(p):
    '''expression : expression AND expression
                  | expression OR expression
                  | expression INFERIOR expression
                  | expression SUPERIOR expression
                  | expression INFERIOR_EQUAL expression
                  | expression SUPERIOR_EQUAL expression
                  | expression DIFFERENT expression
                  | expression EQUALEQUAL expression'''
    switcher = {
        '&': p[1] and p[3],
        '|': p[1] or p[3],
        '<': p[1] < p[3],
        '>': p[1] > p[3],
        '<=': p[1] <= p[3],
        '>=': p[1] >= p[3],
        '!=': p[1] != p[3],
        '==': p[1] == p[3]
    }

    p[0] = switcher.get(p[2])


def p_expression_assign(p):
    '''statement : NAME EQUAL expression
                 | NAME PLUS PLUS'''
    try:
        if p[2] == '=':
            names[p[1]] = p[3]
        elif p[2] == '+' and p[3] == '+':
            names[p[1]] = names[p[1]] + 1
    except LookupError:
        print("Undefined name '%s'" % p[1])


def p_error(p):
    print("Syntax error at '%s'" % p.value)


def p_print(p):
    """statement : PRINT LPAREN expression RPAREN
                 | PRINT LPAREN DOUBLEQUOTE STRING DOUBLEQUOTE RPAREN"""

    # TODO: faire en sorte de pouvoir untiliser des STRING
    if p[3] == '"':
        print(p[4])
    else:
        print(p[3])


import ply.yacc as yacc

yacc.yacc()

while True:
    try:
        s = input('calc > ')
    except EOFError:
        break
    yacc.parse(s)
