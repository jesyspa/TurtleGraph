"""Parser for human-readable strings.

Due to PLY using function docstrings for special purposes, all of the functions
in this module that start with a t_ or a p_ do not have standard docstrings.
Please consult the comments instead.

Grammar:
expr     : expr SUMOP expr
         | expr DIFFOP expr
         | expr PRODOP expr
         | expr QUOTOP expr
         | expr POWOP expr
         | OPPAR QUOTOP CLPAR
         | DIFFOP expr (UMINUS precedence)
         | SUMOP expr  (UPLUS precedence)
         | value
         ;
value    : CONSTANT
         | VARIABLE
         ;
OPPAR    | '(' ;
CLPAR    | ')' ;
SUMOP    : '+' ;
DIFFOP   : '-' ;
PRODOP   : '*' ;
QUOTOP   : '/' ;
POWEROP  : '^' ;
CONSTANT : '0' .. '9'+
         | '0' .. '9'+ '.' '0' .. '9'+
         ;
VARIABLE : ('a' .. 'z' | 'A' .. 'Z')+ ;

"""

# It may be a good idea to rewrite this to be in classes...

###############################################################################
###########                 Defining lexer rules                   ############
###############################################################################

from ply import lex
import expression.constant
import expression.variable

# List of token names.  These are required by both the lexer and parser, so
# they must be imported by the parser module if it is ever split.
tokens = (
    "NOTIMPLEMENTED",
    "BADCOMMA",
    "BADPOWOP",
    "OPPAR",
    "CLPAR",
    "SUMOP",
    "DIFFOP",
    "PRODOP",
    "QUOTOP",
    "POWOP",
    "VARIABLE",
    "CONSTANT",
    "UPLUS", # only for precedence
    "UMINUS", # only for precedence
)

class Tokenizer(object):
    """Tokenizer of mathematical expressions.

    Written with PLY.  An object of this class behaves like an instance returned
    by lex.lex().  __init__ accepts the same arguments as lex.lex().

    Methods starting with t_ are internal, do not use them separately.

    Methods:
        __init__(**kwargs)
            Arguments to lex.lex()

        token

    """
    def __init__(self, **kwargs):
        """Build the lexer.

        This constructs this into an instance of the lexer.

        """
        self.tokens = tokens
        self.lexer = lex.lex(module=self, **kwargs)
        self.token = self.lexer.token
        self.input = self.lexer.input

    ######################################################
    ## Functions past this point are only needed by lex ##
    ######################################################

    # Handles errors of not-implemented operators and tokens.
    def t_NOTIMPLEMENTED(self, t):
        "[<>=]=?"
        raise NotImplementedError(
            "Sorry, operator `{0}' is not yet implemented.".format(t.value))

    # Handles the usage of , as a decimal point.
    def t_BADCOMMA(self, t):
        "[0-9]+,[0-9]+"
        raise Exception("Unknown symbol `,'.  The decimal point is a `.'.")

    def t_BADPOWOP(self, t):
        r"\*\*"
        raise Exception("Power operator is `^', not `**'.")

    t_OPPAR = r"\("
    t_CLPAR = r"\)"
    t_SUMOP = r"\+"
    t_DIFFOP = r"-"
    t_PRODOP = r"\*"
    t_QUOTOP = r"/"
    t_POWOP = r"\^"

    # Let's handle the variables and constants here for simplicity.
    # Formally, this is part of the parser, but there's no need to delay it.
    def t_VARIABLE(self, t):
        "[a-zA-Z]+"
        t.value = expression.variable.Variable(t.value)
        return t

    def t_CONSTANT(self, t):
        r"[0-9]+(\.[0-9]+)?"
        t.value = expression.constant.Constant(t.value)
        return t

    # If we encounter an error, we want to grab anything until we reach whitespace.
    def t_error(self, t):
        import re
        pattern = re.compile("[^ \t\n]+")
        raise Exception("Unknown symbol `{0}'.".format(
            pattern.match(t.value).group(0)))

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

class Parser(object):
    """Parser of mathematical expressions.

    Written with PLY.  An object of this class behaves like an object returned
    by yacc.yacc().  __init__ accepts the same parameters as yacc.yacc(), plus a
    lexer parameter.  See the docstring of __init__ for details.

    Methods starting with p_ are internal, do not use them separately.
    
    """
    def __init__(self, lexer=None, **kwargs):
        """Initialise the parser.

        lexer - lexer to use
        kwargs - args to pass to yacc.yacc

        If no lexer is passed, a default one is used.

        """
        if lexer is None:
            self.lexer = Tokenizer()
        else:
            self.lexer = lexer
        self.parser = yacc.yacc(**kwargs)
        
    def parse(self, instring, lexer=None):
        if lexer is None:
            return self.parser.parse(instring, lexer=self.lexer)
        else:
            return self.parser.parse(instring, lexer=lexer)


precedence = (
    ('left', 'SUMOP', 'DIFFOP'),
    ('left', 'PRODOP', 'QUOTOP'),
    ('right', 'UPLUS', 'UMINUS'),
    ('right', 'POWOP'),
    ('left', 'CLPAR')
)

def p_error_empty(p):
    "expr : "
    raise Exception("Nothing to parse.")

def p_error_function(p):
    "expr : VARIABLE OPPAR expr CLPAR"
    raise Exception("Functions are currently not supported.  "
        "Offending piece: ``{0}({1})''.".format(p[1], p[3]))

def p_error_implicit_multiplication(p):
    "expr : CONSTANT OPPAR expr CLPAR"
    raise Exception("Implicit multiplication is currently not supported.  "
        "Offending piece: ``{0}({1})''.".format(p[1], p[3]))

def p_error_implicit_bracket_multiplication(p):
    "expr : OPPAR expr CLPAR OPPAR expr CLPAR"
    raise Exception("Implicit multiplication is currently not supported.  "
        "Offending piece: ``({0})({1})''.".format(p[2], p[5]))

def p_error_wrong_power_op(p):
    "expr : PRODOP PRODOP"
    raise Exception("Power operator is `^', not `**'.")

def p_expr_sum(p):
    "expr : expr SUMOP expr"
    p[0] = expression.binaryop.SumOp(p[1], p[3])

def p_expr_difference(p):
    "expr : expr DIFFOP expr"
    p[0] = expression.binaryop.DifferenceOp(p[1], p[3])

def p_expr_product(p):
    "expr : expr PRODOP expr"
    p[0] = expression.binaryop.ProductOp(p[1], p[3])

def p_expr_quotient(p):
    "expr : expr QUOTOP expr"
    p[0] = expression.binaryop.QuotientOp(p[1], p[3])

def p_expr_power(p):
    "expr : expr POWOP expr"
    p[0] = expression.binaryop.PowerOp(p[1], p[3])

def p_expr_parens(p):
    "expr :  OPPAR expr CLPAR"
    p[0] = p[2]

def p_expr_uplus(p):
    "expr : SUMOP expr %prec UPLUS"
    p[0] = p[2]

def p_expr_uminus(p):
    "expr : DIFFOP expr %prec UMINUS"
    p[0] = expression.binaryop.DifferenceOp(
        expression.constant.Constant(0), p[2])

def p_expr_value(p):
    "expr : value"
    p[0] = p[1]

def p_value(p):
    """
    value :  VARIABLE
          |  CONSTANT
    """
    p[0] = p[1]

#  It'd be nice if this error message was more informative.
def p_error(p):
    raise Exception("Syntax error at `{0}'.".format(p.value))

###############################################################################
###########                  End of parser rules                   ############
###############################################################################

