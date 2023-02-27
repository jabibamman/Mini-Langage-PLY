from genereTreeGraphviz2 import printTreeGraph

# Functions
reserved = {
    'print' : 'PRINT',
    'if' : 'IF',
    'else' : 'ELSE',
    'elif' : 'ELIF',
    'while' : 'WHILE',
    'for' : 'FOR'
}

# List of token names
tokens = [
    'NAME','NUMBER',
    'PLUS','MINUS','TIMES','DIVIDE',
    'LPAREN','RPAREN','LCURLY','RCURLY',
    'SEMICOLON',
    'AND','OR','LOWER','HIGHER','LOWER_EQUAL','HIGHER_EQUAL',
    'EQUAL','EQUALS','INEQUAL'
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
t_LOWER  = r'\<'
t_HIGHER  = r'\>'
t_LOWER_EQUAL = r'\<='
t_HIGHER_EQUAL = r'\>='
t_EQUAL = r'='
t_EQUALS  = r'=='
t_INEQUAL  = r'!='

# Parsing rules
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'LOWER', 'HIGHER', 'EQUAL'),
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','UMINUS'),
)

# Variables
names = {}

# Ignored characters
t_ignore = " \t"



def eval(t):
    if type(t)!=tuple : return t
    print('eval de ', t)
    if t[0]=='+' : return eval(t[1]) + eval(t[2])
    if t[0]=='*' : return eval(t[1]) * eval(t[2])
    if t[0]=='-' : return eval(t[1]) - eval(t[2])
    if t[0]=='/' : return eval(t[1]) / eval(t[2])
    if t[0]=='&&': return eval(t[1]) and eval(t[2])
    if t[0]=='||': return eval(t[1]) or eval(t[2])
    if t[0]=='==': return eval(t[1]) == eval(t[2])
    if t[0]=='!=': return eval(t[1]) != eval(t[2])
    if t[0]=='<' : return eval(t[1]) < eval(t[2])
    if t[0]=='>' : return eval(t[1]) > eval(t[2])
    if t[0]=='<=': return eval(t[1]) <= eval(t[2])
    if t[0]=='>=': return eval(t[1]) >= eval(t[2])
    if t[0]=='bloc' :
        eval(t[1])
        eval(t[2])
    if t[0]=='print' : print(eval(t[1]))
    if t[0]=='assign' : names[t[1]] = eval(t[2])
    if t[0]=='name' : return names[t[1]]
    if t[0]=='if' :
        if eval(t[1]) :
            eval(t[2])
        else :
            eval(t[3])
    if t[0]=='while' :
        while eval(t[1]) :
            eval(t[2])
    if t[0]=='for' :
        eval(t[1])
        while eval(t[2]) :
            eval(t[4])
            eval(t[3])

def fibo_it(i):
    a,b,c,cpt=0,1,0,0
    while cpt <= i:
        if cpt < 2 :
            c = cpt
        else :
            c=a+b
            a=b
            b=c
        cpt+=1
    return c



def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'NAME')
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
    print(p[0])
    printTreeGraph(p[0])
    eval(p[1])

def p_line(p):
    '''linst : linst inst
            | inst'''
    if len(p)==3:
        p[0] = ('bloc',p[1],p[2])
    else:
        p[0] = ('bloc',p[1],'empty')

def p_statement_if(p):
    '''inst : IF LPAREN expression RPAREN LCURLY linst RCURLY
            | IF LPAREN expression RPAREN LCURLY linst RCURLY ELSE LCURLY linst RCURLY
            | IF LPAREN expression RPAREN LCURLY linst RCURLY instelif'''
    if len(p)==8 :
        p[0] = ('if',p[3],p[6],'empty')
    elif len(p)==12 :
        p[0] = ('if', p[3], p[6], p[10])
    else :
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
    if len(p)==10 :
        p[0] = ('elif',p[4],p[7],p[9])
    else :
        p[0] = ('elif',p[4],p[7],'empty')

def p_statement_while(p):
    'inst : WHILE LPAREN expression RPAREN LCURLY linst RCURLY'
    p[0] = ('while',p[3],p[6])

def p_statement_for(p):
    'inst : FOR LPAREN inst inst inst RPAREN LCURLY linst RCURLY'
    p[0] = ('for',p[3],p[4],p[5],p[8])

def p_statement_assign(p):
    'inst : NAME EQUAL expression SEMICOLON'
    p[0] = ('assign',p[1],p[3])

def p_statement_print(p):
    'inst : PRINT LPAREN expression RPAREN SEMICOLON'
    p[0] = ('print',p[3])

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
    p[0] = (p[2],p[1],p[3])

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
    p[0] = ('name',p[1])

def p_error(p):
    print("Syntax error at '%s'" % p.value)



# Parsing the input
import ply.yacc as yacc
yacc.yacc()
#s='1+2;x=4;if(x==4){x=x+1;}print(x);'
#s='x=4;if(x>4){x=x+1;}print(x);'
#s='print(1+2);x=4;x=x+1;print(x);'
#s='x=4;while(x!=0){x=x-1;}print(x);'
#s=';;;;;;;;;;;;;;;;;;;'
s='for(i=0;i<=10;i=i+1;) {print(i);}'
#s='for(;;;){}'
#s='x=4; if(x==4){x=5;} else{x=0;} print(x);'
#s='i=6; a=0;b=1;c=0;cpt=0; while(cpt<=i) {if(cpt<2) {c=cpt;} else {c=a+b;a=b;b=c;} cpt=cpt+1;} print(c);'
yacc.parse(s)

# while True :
#     s = input("calc > ")
#     yacc.parse(s)
