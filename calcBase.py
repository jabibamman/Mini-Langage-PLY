from genereTreeGraphviz2 import printTreeGraph

# Functions
reserved = {
    'print': 'PRINT',
    'if': 'IF',
    'else': 'ELSE',
    'elif': 'ELIF',
    'while': 'WHILE',
    'for': 'FOR',
    'function': 'FUNCTION',
    'return': 'RETURN'
}

# List of token names
tokens = [
             'NAME', 'NUMBER',
             'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
             'LPAREN', 'RPAREN', 'LCURLY', 'RCURLY',
             'SEMICOLON',
             'AND', 'OR', 'LOWER', 'HIGHER', 'LOWER_EQUAL', 'HIGHER_EQUAL',
             'EQUAL', 'EQUALS', 'INEQUAL',
             'DOUBLEQUOTE', 'STRING', 'COMMA'
         ] + list(reserved.values())

# Characters for tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LCURLY = r'\{'
t_RCURLY = r'\}'
t_SEMICOLON = r';'
t_AND = r'&&'
t_OR = r'\|\|'
t_LOWER = r'\<'
t_HIGHER = r'\>'
t_LOWER_EQUAL = r'\<='
t_HIGHER_EQUAL = r'\>='
t_EQUAL = r'='
t_EQUALS = r'=='
t_INEQUAL = r'!='
t_DOUBLEQUOTE = r'"'
t_COMMA = r','

# Parsing rules
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'LOWER', 'HIGHER', 'EQUAL'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),
)

# Variables
names = {}

# Functions
functions = {}

# Ignored characters
t_ignore = " \t"


def evalInst(p):
    print("evalInst de ", p)
    if p == "empty":
        return

    if type(p) != tuple:
        print("inst non tuple")
        return

    if p[0] == 'bloc':
        evalInst(p[1])
        evalInst(p[2])
        return

    if p[0] == 'function':
        # p[1][0] = function name, p[1][1] = args, p[1][2] = body
        function = dict()

        # si il y a des parametre
        if p[2][1] != 'empty':
            args = list()
            t = p[2][1]
            while t is tuple and len(t) == 2:
                args.append(t[0])
                t = t[1]
            if t is not tuple():
                args.append(t)
            function['args'] = args
        function['body'] = p[3]
        functions[p[1]] = function

    if p[0] == 'call':
        function = functions[p[1]]
        if len(p) == 3:
            call_args = list()
            arg = p[2]
            while arg is tuple() and len(arg) == 2:
                call_args.append(arg[1])
                arg = arg[0]

            if arg is not tuple():
                call_args.append(arg[1])
            if dict(function).get('args', []) is None \
                    or len(function.get('args', [])) > len(call_args) \
                    or len(function.get('args', [])) < len(call_args):
                raise Exception(p[1] + " takes " + str(len(function.get('args', []))) + " arguments but " + str(
                    len(call_args)) + " were given")

            for k in range(len(call_args)):
                names[function['args'][k]] = evalExpr(call_args[k])

        evalInst(function['body'])

        # delete args in names
        if len(p) == 3:
            for arg in function['args']:
                del names[arg]


    if p[0] == 'assign':
        names[p[1]] = evalExpr(p[2])

    if p[0] == 'print':
        print(">", evalExpr(p[1]))

    if p[0] == 'for':
        evalInst(p[1])  # initialisation
        while evalExpr(p[2]):
            evalInst(p[3])  # corps de la boucle
            evalInst(p[4])  # incrémentation

    if p[0] == 'while':
        while evalExpr(p[1]):
            evalInst(p[2])

    if p[0] == 'if':
        if evalExpr(p[1]):
            evalInst(p[2])
        else:
            evalInst(p[3])

    return 'UNK'


def evalExpr(p):
    print("evalExpr de ", p)
    if type(p) is int: return p
    if type(p) is str:
        if p.startswith('"'):
            return p[1:-1]
        else:
            if names.get(('arg', p)) is not None:
                return names[('arg', p)]

            if p not in names:
                raise NameError(f"'{p}' is not defined")

            return names[p]

    if type(p) is tuple:
        if p[0] == 'arg':
            return p[1]
        op, left, right = p  # décomposition de la paire

        if op == '+': return evalExpr(left) + evalExpr(right)
        if op == '-': return evalExpr(left) - evalExpr(right)
        if op == '*': return evalExpr(left) * evalExpr(right)
        if op == '/': return evalExpr(left) / evalExpr(right)
        if op == '<': return int(evalExpr(left)) < int(evalExpr(right))
        if op == '>': return int(evalExpr(left)) > int(evalExpr(right))
        if op == '<=': return int(evalExpr(left)) <= int(evalExpr(right))
        if op == '>=': return int(evalExpr(left)) >= int(evalExpr(right))
        if op == '!=': return int(evalExpr(left)) != int(evalExpr(right))
        if op == '==': return int(evalExpr(left)) == int(evalExpr(right))
        if op == '&':  return evalExpr(left) and evalExpr(right)
        if op == '|':  return evalExpr(left) or evalExpr(right)
    return "UNK"


def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'NAME')
    return t


def t_STRING(t):
    r'\".*?\"'
    t.value = str(t.value)
    t.type = reserved.get(t.value, 'STRING')
    return t


def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
import ply.lex as lex

lex.lex()


def p_start(p):
    '''start : linst'''
    p[0] = ('start', p[1])
    # print(p[0])
    # printTreeGraph(p[0])
    evalInst(p[1])


def p_bloc(p):
    '''linst : linst inst
            | inst'''
    if len(p) == 3:
        p[0] = ('bloc', p[1], p[2])
    else:
        p[0] = ('bloc', p[1], 'empty')


def p_args(p):
    '''args : NAME
            | NUMBER
            | args COMMA NAME
            | args COMMA NUMBER'''
    p[0] = ('args', p[1])
    if len(p) == 2:
        p[0] = ('arg', p[1])  # , 'empty')
    else:
        p[0] = ('arg', p[1], p[3])  # 'empty')


def p_statement_declare_function(p):
    '''inst : FUNCTION NAME LPAREN RPAREN LCURLY linst RCURLY
               |  FUNCTION NAME LPAREN args RPAREN LCURLY linst RCURLY'''
    if len(p) == 8:
        # p[6] c'est l'équivalent de body ('bloc, ('print', 'a'), 'empty')
        p[0] = ('function', p[2], ('args', 'empty'), p[6])  # , 'empty')
    elif len(p) == 9:
        # p[7] c'est l'équivalent de body ('bloc, ('print', 'a'), 'empty')
        p[0] = ('function', p[2], ('args', p[4]), p[7])  # , 'empty')


def p_statement_call_function(p):
    '''inst : NAME LPAREN RPAREN
                |  NAME LPAREN args RPAREN'''
    if len(p) == 4:
        p[0] = ('call', p[1])
    elif len(p) == 5:
        p[0] = ('call', p[1], ('args', p[3]))


def p_statement_if(p):
    '''inst : IF LPAREN expression RPAREN LCURLY linst RCURLY
            | IF LPAREN expression RPAREN LCURLY linst RCURLY ELSE LCURLY linst RCURLY
            | IF LPAREN expression RPAREN LCURLY linst RCURLY instelif'''
    if len(p) == 8:
        p[0] = ('if', p[3], p[6], 'empty')
    elif len(p) == 12:
        p[0] = ('if', p[3], p[6], p[10])
    else:
        p[0] = ('if', p[3], p[6], p[7])


# def p_statement_if_else(p):
#     'inst : IF LPAREN expression RPAREN LCURLY linst RCURLY ELSE LCURLY linst RCURLY'
#     p[0] = ('if',p[3],p[6],p[10])
#
# def p_statement_elif(p):
#     'inst : IF LPAREN expression RPAREN LCURLY linst RCURLY instelif'
#     p[0] = ('if',p[3],p[6],p[7])

def p_inst_elif(p):
    '''instelif : ELSE IF LPAREN expression RPAREN LCURLY linst RCURLY instelif
                | ELSE IF LPAREN expression RPAREN LCURLY linst RCURLY'''
    if len(p) == 10:
        p[0] = ('elif', p[4], p[7], p[9])
    else:
        p[0] = ('elif', p[4], p[7], 'empty')


def p_statement_while(p):
    'inst : WHILE LPAREN expression RPAREN LCURLY linst RCURLY'
    p[0] = ('while', p[3], p[6])


def p_statement_for(p):
    'inst : FOR LPAREN inst inst inst RPAREN LCURLY linst RCURLY'
    p[0] = ('for', p[3], p[4], p[5], p[8])


def p_statement_assign(p):
    'inst : NAME EQUAL expression SEMICOLON'
    p[0] = ('assign', p[1], p[3])


def p_statement_print(p):
    'inst : PRINT LPAREN expression RPAREN SEMICOLON'
    p[0] = ('print', p[3])


def p_statement_expr(p):
    'inst : expression SEMICOLON'
    p[0] = p[1]


def p_statement_semicolon(p):
    'inst : SEMICOLON'
    p[0] = ('empty')


def p_statement_nothing(p):
    'inst : '
    p[0] = ('empty')


def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression AND expression
                  | expression OR expression
                  | expression EQUALS expression
                  | expression INEQUAL expression
                  | expression LOWER expression
                  | expression HIGHER expression
                  | expression LOWER_EQUAL expression
                  | expression HIGHER_EQUAL expression'''
    p[0] = (p[2], p[1], p[3])


def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
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


def p_expression_string(p):
    'expression : STRING'
    p[0] = p[1]


def p_error(p):
    print("Syntax error at '%s'" % p.value)


# Parsing the input
import ply.yacc as yacc

yacc.yacc()
# s='print(1+2);x=4;x=x+1;'
# s = '1+2;x=4;if(x==4){x=x+1;}print(x);'
#s = 'print(1+2);x=4;x=x+1;print("hello world");'
# s = 'print("hello world");'
# s='x=4;if(x>4){x=x+1;}print(x);'
# s='print(1+2);x=4;x=x+1;print(x);'
# s='x=4;while(x!=0){x=x-1;}print(x);'
# s=';;;;;;;;;;;;;;;;;;;'
# s='for(i=0;i<=10;i=i+1;) {print(i);}'
# s='for(;;;){}'
# s='x=4; if(x==4){x=5;} else{x=0;} print(x);'
# s='i=6; a=0;b=1;c=0;cpt=0; while(cpt<=i) {if(cpt<2) {c=cpt;} else {c=a+b;a=b;b=c;} cpt=cpt+1;} print(c);'

# ! FONCTION ! /!\ WORKING, le parser  reconnait les fonctions sans args /!\
# s = '''
# function carre() {
#     print("on test");
# }
# carre();
# print("on test AUSSI");
# '''

# ! FONCTION ! /!\ WORKING, le parser  reconnait les fonctions avec 1 args /!\
s = '''
function carre(x) {
    print(x*x);
}
carre(2);
print("on test AUSSI");
'''

# ! FONCTION ! /!\ WORKING, le parser  reconnait les fonctions avec 2 args /!\
# s = '''
# function carre(x,y) {
#     print(x*y);
# }
# carre(2,3);
# print("on test AUSSI");
# '''

yacc.parse(s)

# while True :
#     s = input("calc > ")
#     yacc.parse(s)
