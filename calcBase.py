from genereTreeGraphviz2 import printTreeGraph

# -----------------------------------------------------------------------------
# calc.py
#
# Expressions arithmétiques sans variables
# -----------------------------------------------------------------------------
import ply.yacc

reserved = {
    'print': 'PRINT',
    'for': 'FOR',
    'while': 'WHILE',
    'if': 'IF',
    'else': 'ELSE',
}

tokens = [
         'NUMBER', 'MINUS',
         'PLUS', 'TIMES', 'DIVIDE',
         'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'AND', 'OR', 'SEMICOLON', 'NAME', 'EQUAL', 'EQUALEQUAL',
         'INFERIOR', 'SUPERIOR', 'INFERIOR_EQUAL', 'SUPERIOR_EQUAL', 'DIFFERENT', "DOUBLEQUOTE", "STRING",
         'COMMENT'
         ] + list(reserved.values())

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'EQUALEQUAL', 'INFERIOR', 'SUPERIOR', 'INFERIOR_EQUAL', 'SUPERIOR_EQUAL', 'DIFFERENT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

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
t_DOUBLEQUOTE = r'\"'
t_LBRACE  = r'\{'
t_RBRACE  = r'\}'

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9_]*'
    t.type = reserved.get(t.value, 'NAME')
    return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_STRING(t):
    r'\".*?\"'
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


def t_COMMENT(t):
    r'//.*|/\*.*?\*/'
    t.lexer.lineno += t.value.count('\n')
    t.type = reserved.get(t.value, 'COMMENT')
    pass

# Build the lexer
import ply.lex as lex

lex.lex()

def evalInst(p):
    print("evaInst de ", p)
    if p == 'empty': return
    if type(p) != tuple:
        print("inst non tuple")
        return

    if p[0] == 'bloc':
        evalInst(p[1])
        evalInst(p[2])
        return

    if p[0] == 'assign':
        names[p[1]] = evalExpr(p[2])


    if p[0] == 'print':
        print("CALC>", evalExpr(p[1]))


    if p[0] == 'for':
        evalInst(p[1]) # initialisation
        while bool(evalExpr(p[2])):
            evalInst(p[3])  # corps de la boucle
            evalInst(p[4])  # incrémentation

    if p[0] == 'while':
        while bool(evalExpr(p[1])):
            evalInst(p[2])


    if p[0] == 'ifElse':
        if(evalExpr(p[1])):
            evalInst(p[2])
        else:
            evalInst(p[3])

    if p[0] == 'if':
        if(evalExpr(p[1])):
            evalInst(p[2])

    return 'UNK'


names = {}

def evalExpr(p):
    print("evalExpr de ", p)
    if type(p) is int: return p
    if type(p) is str:
        if p.startswith('"'):
            return p[1:-1]
        else:
            return names[p]
    if type(p) is tuple:
        if p[0] == '+': return evalExpr(p[1]) + evalExpr(p[2])
        if p[0] == '-': return evalExpr(p[1]) - evalExpr(p[2])
        if p[0] == '*': return evalExpr(p[1]) * evalExpr(p[2])
        if p[0] == '/': return evalExpr(p[1]) / evalExpr(p[2])
        if p[0] == '<': return int(evalExpr(p[1])) < int(evalExpr(p[2]))
        if p[0] == '>': return int(evalExpr(p[1])) > int(evalExpr(p[2]))
        if p[0] == '<=': return int(evalExpr(p[1])) <= int(evalExpr(p[2]))
        if p[0] == '>=': return int(evalExpr(p[1])) >= int(evalExpr(p[2]))
        if p[0] == '!=': return int(evalExpr(p[1])) != int(evalExpr(p[2]))
        if p[0] == '==': return int(evalExpr(p[1])) == int(evalExpr(p[2]))
        if p[0] == '&':  return evalExpr(p[1]) and evalExpr(p[2])
        if p[0] == '|':  return evalExpr(p[1]) or evalExpr(p[2])

    return "UNK"


def p_start(p):
    ''' start : bloc '''
    p[0] = ('start', p[1])
    #print(p[0])
    printTreeGraph(p[0])
    evalInst(p[1])


def p_bloc(p):
    '''bloc : bloc statement SEMICOLON
            | statement SEMICOLON'''
    if len(p) == 4:
        p[0] = ('bloc', p[1], p[2])
    else:
        p[0] = ('bloc', p[1], 'empty')


def p_statement_assign(p):
    'statement : NAME EQUAL expression'
    p[0] = ('assign', p[1], p[3])


def p_statement_print(p):
    """statement : PRINT LPAREN expression RPAREN"""
    p[0] = ('print', p[3])


def p_statement_for(p):
    'statement : FOR LPAREN statement SEMICOLON expression SEMICOLON statement RPAREN LBRACE bloc RBRACE'
    p[0] = ('for', p[3], p[5], p[7], p[10])


def p_statement_while(p):
    'statement : WHILE LPAREN expression RPAREN LBRACE bloc RBRACE'
    p[0] = ('while', p[3], p[6])


def p_statement_if_else(p):
    '''statement : IF LPAREN expression RPAREN LBRACE bloc RBRACE ELSE LBRACE bloc RBRACE
    | IF LPAREN expression RPAREN LBRACE bloc RBRACE'''
    if len(p) == 12:
        p[0] = ('ifElse', p[3], p[6], p[10])
    else:
        p[0] = ('if', p[3], p[6])




def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression INFERIOR expression
                  | expression AND expression
                  | expression OR expression
                  | expression SUPERIOR expression
                  | expression INFERIOR_EQUAL expression
                  | expression SUPERIOR_EQUAL expression
                  | expression DIFFERENT expression
                  | expression EQUALEQUAL expression'''
    p[0] = (p[2], p[1], p[3])


def p_expression_uminus(p):
    'expression : MINUS expression'
    p[0] = -p[2]


def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]


def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]


def p_expression_name(p):
    'expression : NAME'
    p[0] = p[1]


def p_statement_comment(p):
    'statement : COMMENT'
    pass


def p_expression_string(p):
    'expression : STRING'
    p[0] = p[1]


def p_error(p):
    print("Syntax error at '%s'" % p.value)


import ply.yacc as yacc

yacc.yacc()

# ! PRINT!
s = 'print(1+2);x=4;x=x+1;print("hello world");'
#s='print(1+2);x=4;x=x+1;'
#s = 'print("hello world!");'
#s = 'x=0; print(x);'
#s='print(1<2 | 2>1);'
#s = 'print(1<2 & 2<1);'

# ! BOUCLES !
#s =  'for(x=0;x<10;x=x+1) { print(x); };'
#s = 'for (i=0; i<=10; i=i+1){print(i);};'
#s = 'x=0; while(x<10) { print(x); x=x+1; };'
# Fibonacci - 10 premiers termes / Doesn't work with the current grammar
#s = 'a=0; b=1; cpt=0; while(cpt <= 10){if(cpt < 1){c=cpt}else{c=a+b;a=b;b=c;};'

# ! IF ELSE !
#s = 'if (1<2){ print("1 est bien inférieur à 2"); };'
#s = 'if (1>2){ print("1 est bien inférieur à 2"); } else { print("1 n\'est pas supérieur à 2"); };'
#s = 'x=1;y=2; if (1<2){ print(x); } else { print(y); };'
#s='if(1<2){print("1<2");}else{print("1>=2"); };'
# s = 'x=1; y=1;if (x==y){ print("x est égal à y"); };'
# doesn't work with the current grammar
#s = 'for(i=0;i<10;i+=1) { }'
#s = "for (x=0;x<10;x++){print(x);};"

# while True:
#     try:
#         #s = input('calc > ')
#         # s = 'x=1;x+3+1;'
#         # s = 'print(1<2 & 2<1);'
#
#     except EOFError:
#         break
yacc.parse(s)
