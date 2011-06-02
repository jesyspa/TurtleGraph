"""Parser for human-readable strings.

Grammar:
sum      : sum SUMOP product
         | product
         ;
product  : product PRODOP power
         | power
         ;
power    : value POWOP power
         | SUMOP value
         | value
         ;
value    : OPPAR sum CLPAR
         | constant
         | variable
         ;
constant : CONSTANT ;
variable : VARIABLE ;
OPPAR    | '(' ;
CLPAR    | ')' ;
SUMOP    : '+' | '-' ;
PRODOP   : '*' | '/' ;
POWEROP  : '^' ;
CONSTANT : '0' .. '9'+
         | '0' .. '9'+ '.' '0' .. '9'+
         ;
VARIABLE : ('a' .. 'z' | 'A' .. 'Z')+ ;

"""

########################################
####   Defining lexer rules here    ####
########################################

from ply import lex

tokens = (
    "OPPAR",
    "CLPAR",
    "SUMOP",
    "PRODOP",
    "POWOP",
    "VARIABLE",
    "CONSTANT"
)

t_OPPAR = r"\("
t_CLPAR = r"\)"
t_SUMOP = r"\+|-"
t_PRODOP = r"\*|/"
t_POWOP = r"\^"
t_VARIABLE = "[a-zA-Z]+"

def t_CONSTANT(t):
    r"[0-9]+(\.[0-9]+)?"
    t.value = float(t.value)
    return t


def t_error(t):
    raise Exception("Unknown symbol `{0}'.".format(t.value))

t_ignore = " \t\n"

########################################
####       End of lexer rules       ####
########################################
########################################
####      Defining parser rules     ####
########################################

from ply import yacc
import expression.binaryop
import expression.constant
import expression.variable

def p_sum(p):
    """
    sum :  sum SUMOP product
    sum :  product
    """
    if len(p) == 4:
        if p[2] == '+':
            p[0] = expression.binaryop.SumOp(p[1], p[3])
        else:
            p[0] = expression.binaryop.DifferenceOp(p[1], p[3])
    else:
        p[0] = p[1]

def p_product(p):
    """
    product :  product PRODOP power
    product :  power
    """
    if len(p) == 4:
        if p[2] == '*':
            p[0] = expression.binaryop.ProductOp(p[1], p[3])
        else:
            p[0] = expression.binaryop.QuotientOp(p[1], p[3])
    else:
        p[0] = p[1]

def p_power(p):
    """
    power :  value POWOP power
    power :  SUMOP value
    power :  value
    """
    if len(p) == 4:
        p[0] = expression.binaryop.PowerOp(p[1], p[3])
    elif len(p) == 3:
        if p[2] == '+':
            p[0] = p[2]
        else:
            p[0] = expression.binaryop.DifferenceOp(0, p[2])
    else:
        p[0] = p[1]

def p_value(p):
    """
    value :  OPPAR sum CLPAR
    value :  variable
    value :  constant
    """
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_variable(p):
    "variable :  VARIABLE"
    p[0] = expression.variable.Variable(p[1])

def p_constant(p):
    "constant :  CONSTANT"
    p[0] = expression.constant.Constant(p[1])

#  It'd be nice if this error message was more informative.
def p_error(p):
    raise Exception("Syntax error at `{0}'.".format(p.value))

########################################
####       End of parser rules      ####
########################################

def get_parser():
    """Retrieve an instance of the parser.

    Relying on yacc to optimise away parser creation if it is unnecessary.
    
    """
    lex.lex()
    return yacc.yacc()


