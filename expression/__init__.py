"""Provide classes that represent an expression tree.

Classes:
Expression  Represent a full expression
BinaryOp    Represent a binary operator
Constant    Represent an integer or real constant
Variable    Represent a variable in an expression

"""

# Expression is not in __all__, as it should not be used externally.
__all__ = ['constant', 'variable', 'binaryop']

