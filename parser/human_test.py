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
        cls.lexer = human.get_lexer()

    def test_tokenize(self):
        """Ensure correct tokenization.
        
        Must ensure:
            A single token of any type is parsed correctly.
            Whitespace is ignored.
            Groups of tokens are parsed correcty.
            
        """
        # A list of tuples.  Each tuple has an input string, and a tuple of the
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
            ("-",      ("LexToken(SUMOP,'-',1,0)",
                        "None")),
            ("*",      ("LexToken(PRODOP,'*',1,0)",
                        "None")),
            ("/",      ("LexToken(PRODOP,'/',1,0)",
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
            ("-z",     ("LexToken(SUMOP,'-',1,0)",
                        "LexToken(VARIABLE,Variable('z'),1,1)",
                        "None")),
            # simple binary operations
            ("5+6.0",  ("LexToken(CONSTANT,Constant(5.0),1,0)", 
                        "LexToken(SUMOP,'+',1,1)",
                        "LexToken(CONSTANT,Constant(6.0),1,2)",
                        "None")),
            ("a - z",  ("LexToken(VARIABLE,Variable('a'),1,0)",
                        "LexToken(SUMOP,'-',1,2)",
                        "LexToken(VARIABLE,Variable('z'),1,4)",
                        "None")),
            # multiple binary operations
            ("5-3*x",  ("LexToken(CONSTANT,Constant(5.0),1,0)",
                        "LexToken(SUMOP,'-',1,1)",
                        "LexToken(CONSTANT,Constant(3.0),1,2)",
                        "LexToken(PRODOP,'*',1,3)",
                        "LexToken(VARIABLE,Variable('x'),1,4)",
                        "None")),
            ("0/x^3",  ("LexToken(CONSTANT,Constant(0.0),1,0)",
                        "LexToken(PRODOP,'/',1,1)",
                        "LexToken(VARIABLE,Variable('x'),1,2)",
                        "LexToken(POWOP,'^',1,3)",
                        "LexToken(CONSTANT,Constant(3.0),1,4)",
                        "None")),
            # miscellaneous silliness
            ("()",     ("LexToken(OPPAR,'(',1,0)",
                        "LexToken(CLPAR,')',1,1)",
                        "None")),
            ("+-",     ("LexToken(SUMOP,'+',1,0)",
                        "LexToken(SUMOP,'-',1,1)",
                        "None")),
            ("^--^",   ("LexToken(POWOP,'^',1,0)",
                        "LexToken(SUMOP,'-',1,1)",
                        "LexToken(SUMOP,'-',1,2)",
                        "LexToken(POWOP,'^',1,3)",
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
        """Ensure correct exception is raised."""
        # List of tuples, where the first element is the input and the second is
        # a tuple of the type and string representation of the exception to be
        # thrown.
        values = (
            ("_", (Exception, "Unknown symbol `_'.")),
            ("5 + $", (Exception, "Unknown symbol `$'.")),
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
                tools.eq_(type(exc), expect[0])
                tools.eq_(str(exc), expect[1])
            except Exception as exc:
                assert False, ("Unexpected exception type ({0} vs {1}).".format(
                    expect[0], type(exc)))

        # This part yields the actual test.
        for i, e in values:
            yield run_logic, i, e

class HumanParseTest(object):
    """Test the parser part of the human module.
    
    Ensure the following works as expected:
        Building of expressions from tokens
        Reporting common syntax errors in detail
        Reporting of miscellaneous syntax errors

    """
    def setUp(self):
        self.parser = human.get_parser()

if __name__ == '__main__':
    unittest.main()

