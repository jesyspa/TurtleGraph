"""Provide classes for variables.

Classes:
Constant        Class for constants

"""

import expression

class Variable(expression.Expression):
    """Represent an expression that is a variable.

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
        _name  The name used to represent this variable (usually 'x').

    """
    def __init__(self, name):
        """Initialise the attributes."""
        self._name = name

    def evaluate(self, variables):
        """Return the value of this variable."""
        variables[self._name]

    def __str__(self):
        """Return a human-readable string representing of this expression.
        
        This should simply be the name of this variable.
        
        """
        return str(self._name)

    def __repr__(self):
        """Return a technical string representing this expression."""
        return "Variable('{0}')".format(self._name)

