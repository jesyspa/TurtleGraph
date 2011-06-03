"""Parser for human-readable strings.

Due to PLY using function docstrings for special purposes, all of the functions
in this module that start with a t_ or a p_ do not have standard docstrings.
Please consult the comments instead.

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
         | CONSTANT
         | VARIABLE
         ;
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

###############################################################################
###########                 Defining lexer rules                   ############
###############################################################################

from ply import lex
import expression.constant
import expression.variable

# List of token names.  These are required by both the lexer and parser, so
# they must be imported by the parser module if it is ever split.
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

# Let's handle the variables and constants here for simplicity.
# Formally, this is part of the parser, but there's no need to delay it.
def t_VARIABLE(t):
    "[a-zA-Z]+"
    t.value = expression.variable.Variable(t.value)
    return t

def t_CONSTANT(t):
    r"[0-9]+(\.[0-9]+)?"
    t.value = expression.constant.Constant(t.value)
    return t

# Getting the column number would be nice, too.
def t_error(t):
    raise Exception("Unknown symbol `{0}'.".format(t.value))

# Currently ignoring newlines -- may want to change that at some point.
t_ignore = " \t\n"

###############################################################################
###########                  End of lexer rules                    ############
###############################################################################
###############################################################################
###############################################################################
###########                Defining parser rules                   ############
###############################################################################

from ply import yacc
import expression.binaryop

# There's a way to rewrite this to be neater using operator precedence.  As
# things are, this way works equally well.

def p_sum(p):
    "sum :  sum SUMOP product"
    if p[2] == '+':
        p[0] = expression.binaryop.SumOp(p[1], p[3])
    else:
        p[0] = expression.binaryop.DifferenceOp(p[1], p[3])

def p_promote_sum(p):
    "sum :  product"
    p[0] = p[1]

def p_product(p):
    "product :  product PRODOP power"
    if p[2] == '*':
        p[0] = expression.binaryop.ProductOp(p[1], p[3])
    else:
        p[0] = expression.binaryop.QuotientOp(p[1], p[3])

def p_promote_product(p):
    "product :  power"
    p[0] = p[1]

def p_power(p):
    "power :  value POWOP power"
    p[0] = expression.binaryop.PowerOp(p[1], p[3])

def p_promote_power(p):
    """
    power :  SUMOP value
          |  value
    """
    if len(p) == 3:
        if p[2] == '+':
            p[0] = p[2]
        else:
            p[0] = expression.binaryop.DifferenceOp(0, p[2])
    else:
        p[0] = p[1]

def p_value(p):
    """
    value :  OPPAR sum CLPAR
          |  VARIABLE
          |  CONSTANT
    """
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]

#  It'd be nice if this error message was more informative.
def p_error(p):
    raise Exception("Syntax error at `{0}'.".format(p.value))

###############################################################################
###########                  End of parser rules                   ############
###############################################################################

def get_lexer():
    """Retrieve an instance of the lexer.

    Relying on PLY to optimise away lexer creation if it is already done.

    """
    import os.path
    tgdir = os.path.expanduser("~/.turtlegraph/")
    return lex.lex(outputdir=tgdir)

def get_parser():
    """Retrieve an instance of the parser.

    Relying on PLY to optimise away parser creation if it is already done.
    
    """
    get_lexer() # ensure that the lexer exists
    import os.path
    tgdir = os.path.expanduser("~/.turtlegraph/")
    return yacc.yacc(outputdir=tgdir)


