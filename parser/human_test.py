"""Thorough tests of the human-readable string parser.

Unlike parse.py, which does more general tests for the common cases, these
testcases are intended to cover the edge cases more fully.

Test classes:
BinaryOp
SumOp
DifferenceOp
ProductOp 
QuotientOp
PowerOp

"""

import nose
from nose import tools
import human

class Test_HumanLex(object):
    """Test the lexer part of the human module.
    
    Ensure the following works as expected:
        Tokenization of valid input
        Handling of token errors

    """
    @classmethod
    def setUpClass(cls):
        cls.lexer = human.Tokenizer()

    def test_tokenize(self):
        # Ensure correct tokenization.
         
        # Must ensure:
        #     A single token of any type is parsed correctly.
        #     Whitespace is ignored.
        #     Groups of tokens are parsed correcty.

        # Tuple of tuples.  Each tuple has an input string, and a tuple of the
        # expected output as strings.  The last expected output should always be
        # "None".
        values = (
            # single tokens
            ("5",      ("LexToken(CONSTANT,Constant(5.0),1,0)",
                        "None")),
            ("7.0",    ("LexToken(CONSTANT,Constant(7.0),1,0)",
                        "None")),
            ("412",    ("LexToken(CONSTANT,Constant(412.0),1,0)",
                        "None")),
            ("x",      ("LexToken(VARIABLE,Variable('x'),1,0)",
                        "None")),
            ("cat",    ("LexToken(VARIABLE,Variable('cat'),1,0)",
                        "None")),
            ("+",      ("LexToken(SUMOP,'+',1,0)",
                        "None")),
            ("-",      ("LexToken(DIFFOP,'-',1,0)",
                        "None")),
            ("*",      ("LexToken(PRODOP,'*',1,0)",
                        "None")),
            ("/",      ("LexToken(QUOTOP,'/',1,0)",
                        "None")),
            ("^",      ("LexToken(POWOP,'^',1,0)",
                        "None")),
            ("(",      ("LexToken(OPPAR,'(',1,0)",
                        "None")),
            (")",      ("LexToken(CLPAR,')',1,0)",
                        "None")),
            # unary operations
            ("+7",     ("LexToken(SUMOP,'+',1,0)",
                        "LexToken(CONSTANT,Constant(7.0),1,1)",
                        "None")),
            ("- z",    ("LexToken(DIFFOP,'-',1,0)",
                        "LexToken(VARIABLE,Variable('z'),1,2)",
                        "None")),
            # simple binary operations
            ("5+6.0",  ("LexToken(CONSTANT,Constant(5.0),1,0)", 
                        "LexToken(SUMOP,'+',1,1)",
                        "LexToken(CONSTANT,Constant(6.0),1,2)",
                        "None")),
            ("a - z",  ("LexToken(VARIABLE,Variable('a'),1,0)",
                        "LexToken(DIFFOP,'-',1,2)",
                        "LexToken(VARIABLE,Variable('z'),1,4)",
                        "None")),
            # multiple binary operations
            ("5-3*x  ",("LexToken(CONSTANT,Constant(5.0),1,0)",
                        "LexToken(DIFFOP,'-',1,1)",
                        "LexToken(CONSTANT,Constant(3.0),1,2)",
                        "LexToken(PRODOP,'*',1,3)",
                        "LexToken(VARIABLE,Variable('x'),1,4)",
                        "None")),
            ("0/x ^3", ("LexToken(CONSTANT,Constant(0.0),1,0)",
                        "LexToken(QUOTOP,'/',1,1)",
                        "LexToken(VARIABLE,Variable('x'),1,2)",
                        "LexToken(POWOP,'^',1,4)",
                        "LexToken(CONSTANT,Constant(3.0),1,5)",
                        "None")),
            # miscellaneous silliness
            ("(  )\t", ("LexToken(OPPAR,'(',1,0)",
                        "LexToken(CLPAR,')',1,3)",
                        "None")),
            (" +\n- ", ("LexToken(SUMOP,'+',1,1)",
                        "LexToken(DIFFOP,'-',1,3)",
                        "None")),
            ("^- -^",  ("LexToken(POWOP,'^',1,0)",
                        "LexToken(DIFFOP,'-',1,1)",
                        "LexToken(DIFFOP,'-',1,3)",
                        "LexToken(POWOP,'^',1,4)",
                        "None"))
        )

        def run_logic(inval, outvals):
            """Provide the tokenizer with input, and check output.
            
            inval    - input string
            outvals  - tuple of expected outputs as strings (ending with none)

            This is the function that does the actual testing.
            
            """
            self.lexer.input(inval)
            for o in outvals:
                tools.eq_(str(self.lexer.token()), o)

        # This part yields the actual test.
        for i, o in values:
            yield run_logic, i, o


    def test_tokenize_error(self):
        # Ensure correct exception is raised.

        # Tuple of tuples, where the first element is the input and the second is
        # a tuple of the type and string representation of the exception to be
        # thrown.
        values = (
            ("_", (Exception, "Unknown symbol `_'.")),
            ("5 + $", (Exception, "Unknown symbol `$'.")),
            ("5 + $3 - 7", (Exception, "Unknown symbol `$3'.")),
            ("x = 5", (NotImplementedError,
                "Sorry, operator `=' is not yet implemented.")),
            ("0 < x", (NotImplementedError,
                "Sorry, operator `<' is not yet implemented.")),
            ("0 > x", (NotImplementedError,
                "Sorry, operator `>' is not yet implemented.")),
            ("0 >= x", (NotImplementedError,
                "Sorry, operator `>=' is not yet implemented.")),
            ("0 <= x", (NotImplementedError,
                "Sorry, operator `<=' is not yet implemented.")),
            ("0,5", (Exception,
                "Unknown symbol `,'.  The decimal point is a `.'.")),
            ("x, 3", (Exception,
                "Unknown symbol `,'.")),
            ("**", (Exception, "Power operator is `^', not `**'.")),
            ("5**6", (Exception, "Power operator is `^', not `**'.")),
            ("x^3* *6", (Exception, "Power operator is `^', not `**'.")),
        )

        def run_logic(inval, expect):
            """Provide the tokenizer with input, and expect exc.
            
            inval   - input string
            expect  - tuple with exception type and string representation

            This is the function that does the actual testing.
            
            """
            self.lexer.input(inval)
            try:
                while self.lexer.token() is not None:
                    pass  # Output is tested elsewhere
            except expect[0] as exc:
                # Check that this is not a derived class.
                tools.assert_is_instance(exc, expect[0])
                tools.eq_(str(exc), expect[1])
            except Exception as exc:
                assert False, ("Unexpected exception type ({0} vs {1}).".format(
                    expect[0], type(exc)))

        # This part yields the actual test.
        for i, e in values:
            yield run_logic, i, e

class Test_HumanParse(object):
    """Test the parser part of the human module.
    
    Ensure the following works as expected:
        Precedence of operators in built expressions
        Correct creation of nodes
        Reporting common syntax errors in detail
        Reporting of miscellaneous syntax errors

    These tests assume that the lexer is functioning correctly.

    """
    @classmethod
    def setUpClass(cls):
        cls.parser = human.Parser()

    def test_operator_precedence(self):
        # Ensure that correct operator precedence is used.

        # Tuple of tuples.  Each tuple is an input-output pair, with both the
        # input and the output being a string.  The output should be what is
        # expected from str(), not from repr().
        values = (
            # This is about precedence, so no single-token expressions.
            # First make sure that all the operators are grouped correctly
            # individiually.
            ("5+x", "(5.0 + x)"),
            ("x-7", "(x - 7.0)"),
            ("z*y", "(z*y)"),
            ("6/3", "(6.0/3.0)"),
            ("x^2", "(x^2.0)"),
            # Two operators of equal precedence
            ("x+2.5+3", "((x + 2.5) + 3.0)"),
            ("0+0-0", "((0.0 + 0.0) - 0.0)"),
            ("5-2+7.3", "((5.0 - 2.0) + 7.3)"),
            ("9-x-3", "((9.0 - x) - 3.0)"),
            ("9*z*1.1", "((9.0*z)*1.1)"),
            ("y*z/x", "((y*z)/x)"),
            ("8/0.5*2", "((8.0/0.5)*2.0)"),
            ("3.3/1.1/0.1", "((3.3/1.1)/0.1)"),
            ("y^2^0.5", "(y^(2.0^0.5))"),
            # Two operators of different precedence
            ("5*x+0.5", "((5.0*x) + 0.5)"),
            ("5-x*0.5", "(5.0 - (x*0.5))"),
            ("3*x^2", "(3.0*(x^2.0))"),
            ("y^2/x", "((y^2.0)/x)"),
            # Three operators of different precedence
            ("0.3^x+5/2", "((0.3^x) + (5.0/2.0))"),
            ("3-0.3*x^2", "(3.0 - (0.3*(x^2.0)))"),
            # With unary operators
            ("3+-5", "(3.0 + (0.0 - 5.0))"),
            ("-2*x", "((0.0 - 2.0)*x)"),
            ("x^-2", "(x^(0.0 - 2.0))"),
            ("-2^4", "(0.0 - (2.0^4.0))"),
            # With parentheses
            ("(x+3)*(x-7)", "((x + 3.0)*(x - 7.0))"),
            ("0.5^(3*x)", "(0.5^(3.0*x))"),
            ("5*(x+3)", "(5.0*(x + 3.0))"),
            ("2*3+(5-3)", "((2.0*3.0) + (5.0 - 3.0))"),
        )
        def run_logic(inval, outval):
            """Provide the parser with input, and expect a certain output.

            Both input and output should be strings.

            """
            tools.eq_(str(self.parser.parse(inval)), outval)
        for i, o in values:
            yield run_logic, i, o

    def test_expr_tree_creation(self):
        # Ensure that the expression tree is correct.
        # 
        # Seeing as operator precedence is tested elsewhere, these tests simply
        # ensure that all rules are applied correctly individually.
        
        # Tuple of tuples.  Each tuple is an input-output pair, with both the
        # input and the output being a string.  The output should be what is
        # expected from repr(), not from str().
        values = (
            # Single-token expressions
            ("0", "Constant(0.0)"),
            ("3.5", "Constant(3.5)"),
            ("x", "Variable('x')"),
            # Some simple expressions
            ("-3", "DifferenceOp(Constant(0.0), Constant(3.0))"),
            ("+3", "Constant(3.0)"),
            ("5+x", "SumOp(Constant(5.0), Variable('x'))"),
            ("3-2", "DifferenceOp(Constant(3.0), Constant(2.0))"),
            ("0*x", "ProductOp(Constant(0.0), Variable('x'))"),
            ("z/2", "QuotientOp(Variable('z'), Constant(2.0))"),
            ("x^2", "PowerOp(Variable('x'), Constant(2.0))"),
            # With parentheses
            ("x^(2+3)", "PowerOp(Variable('x'), SumOp(Constant(2.0),"
            " Constant(3.0)))"),
            # More tests are necessary!
        )
        def run_logic(inval, outval):
            """Provide the parser with input, and expect a certain output.

            Both input and output should be strings.

            """
            tools.eq_(repr(self.parser.parse(inval)), outval)

        for i, o in values:
            yield run_logic, i, o

    def test_errors(self):
        # Ensure correct exception is raised.
        #
        # Common errors to check for:
        #     Empty string
        #     Usage of functions
        #     Usage of implicit multiplication of brackets, such as 3(x+5)
        # 
        # Also check that miscellaneous errors raise an Exception

        # Tuple of tuples.  Each tuple is an input-output pair, the input being
        # a string, and the output being a tuple of exception type and exception
        # string representation.
        values = (
            ("", (Exception, "Nothing to parse.")),
            # functions
            ("sin(x)", (Exception, "Functions are currently not supported.  "
                "Offending piece: ``sin(x)''.")),
            ("tan(y+3)", (Exception, "Functions are currently not supported.  "
                "Offending piece: ``tan((y + 3.0))''.")),
            ("6*ln(x+3)", (Exception, "Functions are currently not supported.  "
                "Offending piece: ``ln((x + 3.0))''.")),
            # implicit multiplication
            ("5(6+x)", (Exception, "Implicit multiplication is currently not "
            "supported.  Offending piece: ``5.0((6.0 + x))''.")),
            ("2(x+3)+7", (Exception, "Implicit multiplication is currently not "
            "supported.  Offending piece: ``2.0((x + 3.0))''.")),
            ("(x+3)(6+x)", (Exception, "Implicit multiplication is currently not "
            "supported.  Offending piece: ``((x + 3.0))((6.0 + x))''.")),
            # other
            ("5+++3", (Exception, "Syntax error at `+'.")),
            ("6.0 7", (Exception, "Syntax error at `7.0'.")),
        )
        def run_logic(inval, expect):
            """Provide the parser with input, and expect exc.
            
            inval   - input string
            expect  - tuple with exception type and string representation

            This is the function that does the actual testing.
            
            """
            try:
                self.parser.parse(inval)
            except expect[0] as exc:
                # Check that this is not a derived class.
                tools.assert_is_instance(exc, expect[0])
                tools.eq_(str(exc), expect[1])
            except Exception as exc:
                assert False, ("Unexpected exception type ({0} vs {1}).".format(
                    expect[0], type(exc)))

        for i, o in values:
            yield run_logic, i, o


