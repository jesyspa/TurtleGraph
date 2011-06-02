"""Provide the Expression class.

"""

class Expression(object):
    """Represent a mathematical expression.

    This class represents an interface that classes that can represent a full
    mathematical expression (such as BinaryOp, Variable and Constant) should
    follow.  By default, all methods except __repr__ raise a
    NotImplementedError exception, and must therefore be overriden in any subclasses.

    Methods:
        evaluate(self, variables)
            Evaluate the expression and return the result.  

        __str__(self)
            Return a human-readable representation of the expression.

        __repr__(self)
            Return a more detailed representation of the expression.

    """
    def evaluate(self, variables):
        """Evaluate the expression and return the result as a float.

        Parameters:
        variables   A dictionary of variable name and value pairs.

        """
        raise NotImplementedError()

    def __str__(self):
        """Return a human-readable representation of the expression."""
        raise NotImplementedError()

    def __repr__(self):
        """Return a more detailed representation of the expression.

        It is convenient if evaluating this string would create an identical
        instance of the expression, but this is not necessary.
        """
        return "Expression()"

