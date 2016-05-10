import ply.lex as lex
import sys
import ply.yacc as yacc

t_ignore = ' \t\v\r' 

precedence = (
        ('left', 'OROR'),
        ('left', 'ANDAND'),
        ('left', 'EQUALEQUAL'),
        ('left', 'LT', 'LE', 'GT', 'GE'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        ('right', 'NOT'),
)

tokens = (
        'OROR',
        'ANDAND',
        'EQUALEQUAL',
        'LT',
        'LE',
        'GT',
        'GE',
        'PLUS',
        'MINUS',
        'TIMES',
        'DIVIDE',
        'NOT',
        'OPENINGBRACKET',       
        'CLOSINGBRACKET',  
        'OPPLUSMINUS',
        'IDENTIFIER',
        'ASSIGNMENT1',  
        'ASSIGNMENT2',         
        'NUMBER',  
        'FOR',
        'OPENINGPARANTHESIS',
        'CLOSINGPARANTHESIS', 
        'SEMICOLON',
        'PRINTFMT',
        'PRINTLN',
        'PRINTSTRUCT',
        'PRINTSCANF',
        'DOT',
        'QUOTATION',
        'STRING',
        'SCANTYPE',
        'COMMA',
        'AND',
        'NOTEQUAL',
        'TYPE',
        'STRUCT',
        'DATATYPE',
        'COLON',
        'LANGLE',
        'RANGLE',
)

t_ANDAND =  r'&&'
t_DIVIDE =  r'/'
t_EQUALEQUAL = r'=='
t_GE =  r'>='
t_GT =   r'>'
t_LE =  r'<='
t_LT = r'<'
t_MINUS = r'-'
t_NOT = r'!'
t_OROR = r'\|\|'
t_PLUS = r'\+'
t_TIMES = r'\*'
t_NOTEQUAL = r'!='
t_COLON = r':'

def t_newline(t):
        r'\n'
        t.lexer.lineno += 1
        pass


def t_error(t):
        print "SYNTAX ERROR"

def t_OPENINGBRACKET(t):
        r'{'
        return t

def t_OPENINGPARANTHESIS(t):
        r'\('
        return t
def t_SEMICOLON(t):
        r';'
        return t

def t_CLOSINGPARANTHESIS(t):
        r'\)'
        return t        

def t_CLOSINGBRACKET(t):
        r'}'
        return t

def t_LANGLE(t):
        r'\['
        return t

def t_RANGLE(t):
        r'\]'
        return t

def t_OPPLUSMINUS(t):
        r'--|\+\+'
        return t

def t_NUMBER(token):
        r'-?[0-9]+(?:\.[0-9]*)?'
        token.value = float(token.value)
        return token

def t_FOR(t):
        r'for'
        return t

def t_TYPE(t): 
 r'type'
 return t

def t_STRUCT(t): 
 r'struct'
 return t

def t_DATATYPE(t): 
 r'int|string'
 return t

def t_ASSIGNMENT1(t):
        r':'
        return t

def t_ASSIGNMENT2(t):
        r'='
        return t

def t_PRINTFMT(t):
        r'fmt'
        return t
def t_DOT(t):
        r'\.'
        return t

def t_PRINTLN(t):
        r'Println'
        return t

def t_PRINTSTRUCT(t):
        r'PrintStruct'
        return t
def t_PRINTSCANF(t):
        r'Scanf'
        return t


def t_IDENTIFIER(t):
        r'[a-z0-9A-Z]+'
        return t

def t_STRING(t):
        r'\"(\s*\w)+\"'
        return t

def t_SCANTYPE(t):
        r'%d|%f|%s'
        return t
def t_COMMA(t):
        r','
        return t
def t_QUOTATION(t):
        r'"'
        return t
def t_AND(t):
        r'&'
        return t

def p_program(p):
 '''program :  OPENINGBRACKET  statements CLOSINGBRACKET
 | OPENINGBRACKET CLOSINGBRACKET
 | structs OPENINGBRACKET  statements CLOSINGBRACKET'''
 if len(p) == 4:
  p[0] = p[2]
 elif len(p) == 5:
  p[0] = p[1] + p[3]

def p_structs_empty(p):
 ''' structs :  '''
 p[0] = []

def p_structs_nested(p):
 ''' structs : struct structs '''
 p[0] = [p[1]] + p[2]

def p_struct(p):
 ''' struct : TYPE IDENTIFIER STRUCT OPENINGBRACKET structdeclarations CLOSINGBRACKET''' 
 p[0] = ("struct", p[2], p[5])

def p_structdeclarations_single(p):
 ''' structdeclarations :  '''
 p[0] = []

def p_structdeclarations_nested(p):
 ''' structdeclarations : structdeclaration structdeclarations'''
 p[0] = [p[1]] + p[2]

def p_structdeclaration(p):
 ''' structdeclaration : IDENTIFIER DATATYPE '''
 p[0] = ('declarestruct', p[1], p[2])
def p_statements_single(p):
 '''statements : statement '''
 p[0] = [p[1]]

def p_statements_nested(p):
 '''statements : statement statements'''
 p[0] = [p[1]] + p[2]

def p_statement(p):
 '''statement : assignment
 | for
 | print
 | printstruct
 | scan '''
 p[0] = p[1]


def p_print(p):
 ''' print : PRINTFMT DOT PRINTLN OPENINGPARANTHESIS expression CLOSINGPARANTHESIS
 | PRINTFMT DOT PRINTLN OPENINGPARANTHESIS STRING CLOSINGPARANTHESIS'''
 p[0] = ('print', p[5])

def p_printstruct(p):
 ''' printstruct : PRINTFMT DOT PRINTSTRUCT OPENINGPARANTHESIS IDENTIFIER CLOSINGPARANTHESIS'''
 p[0] = ('printstruct', p[5])


def p_scan_normal(p):
 ''' scan : PRINTFMT DOT PRINTSCANF OPENINGPARANTHESIS QUOTATION SCANTYPE QUOTATION COMMA AND IDENTIFIER CLOSINGPARANTHESIS'''
 p[0] = ('scan', p[6], p[10])

def p_scan_struct(p):
 '''scan : PRINTFMT DOT PRINTSCANF OPENINGPARANTHESIS QUOTATION SCANTYPE QUOTATION COMMA AND IDENTIFIER DOT IDENTIFIER CLOSINGPARANTHESIS  '''
 p[0] = ('scanstruct', p[6], p[10], p[12])

def p_for(p):
 '''for : FOR assignment SEMICOLON expression SEMICOLON assignment OPENINGBRACKET statements CLOSINGBRACKET'''
 p[0] = ("for", p[2], p[4], p[6], p[8])


def p_assignment_normal(p):
 '''assignment : IDENTIFIER ASSIGNMENT1 ASSIGNMENT2 expression'''
 p[0] = ("assignment", p[1], p[4]) 

def p_assignment_bonus(p):
 '''assignment : IDENTIFIER LANGLE expression RANGLE ASSIGNMENT1 ASSIGNMENT2 expression'''
 p[0] = ("assignmentbonus", p[1],p[3],p[7])

def p_assignment_structattr(p):
 ''' assignment : IDENTIFIER DOT IDENTIFIER ASSIGNMENT1 ASSIGNMENT2 expression '''
 p[0] = ("structattr", p[1], p[3], p[6])

def p_assignment_struct(p):
 '''assignment : IDENTIFIER ASSIGNMENT1 ASSIGNMENT2 IDENTIFIER OPENINGBRACKET structdefinations CLOSINGBRACKET'''
 p[0] = ("structassignment", p[1], p[4], p[6])

def p_assignment_struct2(p):
 '''assignment : IDENTIFIER LANGLE expression RANGLE ASSIGNMENT1 ASSIGNMENT2 IDENTIFIER OPENINGBRACKET structdefinations CLOSINGBRACKET'''
 p[0] = ("structassignment2", p[1], p[3], p[7], p[9])

def p_structdefinations_empty(p):
 ''' structdefinations : '''
 p[0] = []

def p_structdefinations_single(p):
 ''' structdefinations : structdefination '''
 p[0] = [p[1]]
 
def p_structdefinations_nested(p):
 ''' structdefinations : structdefination COMMA structdefinations '''
 p[0] = [p[1]] + p[3]

def p_structdefination(p):
 ''' structdefination : IDENTIFIER SEMICOLON expression
 | IDENTIFIER SEMICOLON STRING '''
 p[0] = ("setstruct",p[1],p[3])

def p_assignment_opplus(p):
 '''assignment : IDENTIFIER OPPLUSMINUS'''
 p[0] = ("assignment" , p[1], p[2])


def p_expression_variable(p):
 '''expression : IDENTIFIER'''
 p[0] = ("variable", p[1])

def p_expression_number(p):
 ''' expression : NUMBER'''
 p[0] = ("number",p[1])

def p_operator(p):
 ''' operator : PLUS
 | NOTEQUAL
 | EQUALEQUAL
 | MINUS
 | TIMES
 | DIVIDE
 | GT
 | LT
 | GE
 | LE'''
 p[0] = p[1]

def p_expression_struct(p):
 ''' expression : IDENTIFIER DOT IDENTIFIER '''
 p[0] = ('expstruct', p[1], p[3])
def p_expression_equation(p):
 ''' expression : expression operator expression '''
 p[0] = ("expression3", p[1], p[2],p[3])


def p_error(t):
        print "invalid syntax"

class Env(dict):
    # Env is a subclass of dict.
    # An environment is a dictionary of {'var': val} pairs with an outer Env.
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))
        self.outer = outer

env = Env()


def eval_statements(statements):
        for statement in statements: 
                eval_statement(statement)

def eval_statement(tree):
        nodetype = tree[0]
        if nodetype == "structattr":
                env[tree[1]][tree[2]] = eval_exp(tree[3])
        if nodetype == "struct":
                constructStruct(tree[1], tree[2])
        elif nodetype == "structassignment":
                assignStruct(tree[1], tree[2], tree[3])
        elif nodetype == "structassignment2":
                var = tree[1] + str(eval_exp(tree[2]))
                assignStruct(var, tree[3], tree[4])
        elif nodetype == "expression":
                return eval_exp(tree[1])
        elif nodetype == "assignment":
                return assign(tree[1], tree[2])
        elif nodetype == "assignmentbonus":
                var = tree[1] + str(eval_exp(tree[2]))
                return assign(var, tree[3])
        elif nodetype == "for":
                return forloop(tree[1], tree[2], tree[3], tree[4])
        elif nodetype == "print":
                if isinstance(tree[1], basestring): 
                        print tree[1][1:-1]
                else:
                        print eval_exp(tree[1])
        elif nodetype == "printstruct":
                print env[tree[1]]
        elif nodetype == "scan":
             if tree[1] == "%d":
                env[tree[2]] = int(raw_input())
             elif tree[1] == "%s": 
                env[tree[2]] = raw_input()
        elif nodetype == "scanstruct":
             if tree[1] == "%d":
                env[tree[2]][tree[3]] = int(raw_input())
             elif tree[1] == "%s":
                env[tree[2]][tree[3]] = raw_input()

def constructStruct(var, initList):
        env[var] = Env()
        for i in initList:
                if i[2] == 'int':
                        env[var][i[1]] = 0
                elif i[2] == 'string':
                        env[var][i[1]] = ""

def assignStruct(var, struct, initlist):
        env[var] = Env()
        for i in initlist:
                temp =  eval_exp(i[2])
                env[struct][i[1]] = temp
                env[var][i[1]] = temp

def forloop(varassign, cond, exp, statements):
        assign(varassign[1], varassign[2])
        while eval_exp(cond):
                eval_statements(statements)
                assign(exp[1], exp[2])

def assign(var, exp):
        if (exp == '++'):
            env[var] = env[var] + 1
        elif (exp == '--'):
            env[var] = env[var] - 1
        else:
            env[var] = eval_exp(exp)


def eval_exp(tree):
 
    nodetype = tree[0]
    if nodetype == "number":
        return int(tree[1])
    elif nodetype == "variable":
        return env[tree[1]]
    elif nodetype == "expstruct":
        return env[tree[1]][tree[2]]
    else:
        left_child = tree[1]
        operator = tree[2]
        right_child = tree[3]
        left_val = eval_exp(left_child)
        right_val = eval_exp(right_child)
        if operator == "+":
            return left_val + right_val
        elif operator == "-":
            return left_val - right_val
        elif operator == "*":
            return left_val * right_val
        elif operator == "/":
            return left_val / right_val
        elif operator == '>':
            return left_val > right_val
        elif operator == '<':
            return left_val < right_val
        elif operator == '>=':
            return left_val >= right_val
        elif operator == '<=':
            return left_val <= right_val

def getTree(test_string):
        lex.lex()
        parser = yacc.yacc()
        tree = parser.parse(test_string)             
        return tree


test_string = "type Person struct {n1 int \n n2 int}   type Color struct {r int \n g int \n b int } { \n  fmt.Println(\"Enter a number\") \n fmt.Scanf(\"%d\",&num) for i:=0 ; i<10;i := i + 2 { color[i] := Color{r ; i+2 , g ; num*3, b ; i+num} person[i] := Person{n1 ; i , n2 ; num}  \n num := num * 2} fmt.PrintStruct(person4) fmt.PrintStruct(color8) }"
a = getTree(test_string)
eval_statements(a)
