"""Provide a class to represent a single option."""

class Option(object):
    """Represent a single option.

    Options come in three parts:  a label, a current value, and a default value.

    Note:  This docstring should be expanded to have a brief description of
    member variables.

    """
    def __init__(self, label = "", default = None):
        """Set member variables."""
        self._label = label
        self._current = None
        self._default = default

    def set(self, value):
        """Set the current value of the option."""
        self._current = value

    def get(self):
        """Return the current value of the option.

        If the option is currently unset, the default will be returned.

        """
        if self._current is not None:
            return self._current
        else:
            return self._default

    def unset(self):
        """Restore the default value."""
        self._current = None

    def label(self):
        """Return the label."""
        return self._label

