"""Provide classes for binary operatons.

Classes:
BinaryOp      Base class for binary operators
SumOp         Class for sum expressions
DifferenceOp  Class for difference expressions
ProductOp     Class for product expressions
QuotientOp    Class for quotient expressions
PowerOp       Class for power expressions

"""

import expression

class BinaryOp(expression.Expression):
    """Represent an expression with a binary operator.

    The two operands are contained within this expression.  This is a base
    class: evaluate(self, variables) should be overloaded.

    Methods:
        __init__(self, first, operator, second)
            Initialise the attributes.

        evaluate(self, variables) [inherited]
            Evaluate this expression.

        __str__(self)
            Return a human-readable string representing this expression.
            
        __repr__(self)
            Return a technical string representing this expression.

    Attributes:
        _first     The expression to the left of the operator.
        _operator  A string representation of the operator.
        _second    The expression to teh right of the operator.

    """
    def __init__(self, first, operator, second):
        """Initialise the attributes.

        Set the first and second subexpressions, and set the operator symbol.

        Parameters:
        first     first subexpression
        operator  string representation of the operator to use
        second    second subexpression

        """
        self._first = first
        self._second = second
        self._operator = operator

    def __str__(self):
        """Return a human-readable string representation of this expression.

        The expression should be surrounded by parentheses, and should be the
        two subexpressions linked with the operator.

        """
        return "".join(['(', str(self._first), self._operator,
        str(self._second), ')'])

    def __repr__(self):
        """Return a technical string representing this expression."""
        return "BinaryOp({0!r}, {1}, {2!r})".format(
            self._first,
            self._operator,
            self._second
        )


class SumOp(BinaryOp):
    """Represent an expression that is a sum of two expressions.

    For details, see the BinaryOp docstring.

    Important differences:

    Methods:
        __init__(self, first, second)
            Initialise the attributes; the operator is not necessary.

        evaluate(self, variables)
            Return the sum of first and second.

    """
    def __init__(self, first, second):
        """Initialise the attributes."""
        # Putting spaces around the + for readability.
        BinaryOp.__init__(self, first, " + ", second)

    def evaluate(self, variables):
        """Return the sum of first and second."""
        return (self._first.evaluate(variables) +
        self._second.evaluate(variables))

    def __repr__(self):
        return "SumOp({0!r}, {1!r})".format(self._first, self._second)


class DifferenceOp(BinaryOp):
    """Represent an expression that is a difference of two expressions.

    For details, see the BinaryOp docstring.

    Important differences:

    Methods:
        __init__(self, first, second)
            Initialise the attributes; the operator is not necessary.

        evaluate(self, variables)
            Return the difference of first and second.

    """
    def __init__(self, first, second):
        """Initialise the attributes."""
        # Putting spaces around the - for readability.
        BinaryOp.__init__(self, first, " - ", second)

    def evaluate(self, variables):
        """Return the difference of first and second."""
        return (self._first.evaluate(variables) -
        self._second.evaluate(variables))

    def __repr__(self):
        return "DifferenceOp({0!r}, {1!r})".format(self._first, self._second)


class ProductOp(BinaryOp):
    """Represent an expression that is a product of two expressions.

    For details, see the BinaryOp docstring.

    Important differences:

    Methods:
        __init__(self, first, second)
            Initialise the attributes; the operator is not necessary.

        evaluate(self, variables)
            Return the product of first and second.

    """
    def __init__(self, first, second):
        """Initialise the attributes."""
        BinaryOp.__init__(self, first, "*", second)

    def evaluate(self, variables):
        """Return the product of first and second."""
        return (self._first.evaluate(variables) *
        self._second.evaluate(variables))

    def __repr__(self):
        return "ProductOp({0!r}, {1!r})".format(self._first, self._second)


class QuotientOp(BinaryOp):
    """Represent an expression that is a quotient of two expressions.

    For details, see the BinaryOp docstring.

    Important differences:

    Methods:
        __init__(self, first, second)
            Initialise the attributes; the operator is not necessary.

        evaluate(self, variables)
            Return the quotient of first and second.

    """
    def __init__(self, first, second):
        """Initialise the attributes."""
        BinaryOp.__init__(self, first, "/", second)

    def evaluate(self, variables):
        """Return the product of first and second."""
        return (self._first.evaluate(variables) /
        self._second.evaluate(variables))

    def __repr__(self):
        return "QuotientOp({0!r}, {1!r})".format(self._first, self._second)


class PowerOp(BinaryOp):
    """Represent an expression that is one expression to the power of another.

    For details, see the BinaryOp docstring.

    Important differences:

    Methods:
        __init__(self, first, second)
            Initialise the attributes; the operator is not necessary.

        evaluate(self, variables)
            Return the first to the power of the second.

    """
    def __init__(self, first, second):
        """Initialise the attributes."""
        BinaryOp.__init__(self, first, "^", second)

    def evaluate(self, variables):
        """Return the first to the power of the second."""
        return (self._first.evaluate(variables) **
        self._second.evaluate(variables))

    def __repr__(self):
        return "PowerOp({0!r}, {1!r})".format(self._first, self._second)


