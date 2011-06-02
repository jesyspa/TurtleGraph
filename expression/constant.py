"""Provide classes for storing constants.

Classes:
Constant        Class for constants

"""

import expression

class Constant(expression.Expression):
    """Represent a constant expression.

    The constant always has a float value, even if it was originally an int or
    string.

    Methods:
        __init__(self, value)
            Initialise the attributes.

        evaluate(self) 
            Evaluate this expression.

        __str__(self)
            Return a human-readable string representing this expression.
            
        __repr__(self)
            Return a technical string representing this expression.

    Attributes:
        _value  The value of the constant.

    """
    def __init__(self, value):
        """Initialise the attributes."""
        self._value = float(value)

    def evaluate(self, variables):
        """Return the value of the constant."""
        return self._value

    def __str__(self):
        """Return a human-readable string representing of this expression.

        This representation should simply be the constant itself.

        """
        return str(self._value)

    def __repr__(self):
        """Return a technical string representing this expression."""
        return "Constant({0})".format(self._value)

