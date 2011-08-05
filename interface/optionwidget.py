"""Provide a class for the option display.

This class should make it easy to query for whether an option is set or not.

"""

from PyQt4 import QtGui
from PyQt4 import QtCore
from option import Option

class OptionWidget(QtGui.QWidget):
    """Display option dialogs and provide an easy way to get options.

    """
    def __init__(self, parent=None):
        """Draw the options interface, and set some defaults.
        
        """
        QtGui.QWidget.__init__(self, parent)
        self.grid_l = QtGui.QGridLayout(self)
        self.options = [ # Note -- this should not be hardcoded!  Move to
                         # metadata ASAP.
            ('function', Option('f(x) = ', '')),
            ('x_min', Option('x minimum: ', -10)),
            ('x_max', Option('x maximum: ', 10)),
            ('y_min', Option('y minimum: ', -10)),
            ('y_max', Option('y maximum: ', 10))
        ]
        i = 0 # counter for rows
        for k, v in self.options:
            option_label_w = QtGui.QLabel(self)
            option_label_w.setText(v.label())
            option_line_w = QtGui.QLineEdit(self)
            option_line_w.setText(str(v.get()))
            self.grid_l.addWidget(option_label_w, i, 0)
            self.grid_l.addWidget(option_line_w, i, 1)
            i += 1
        self.options = dict(self.options)
        self.setLayout(self.grid_l)
        self.show()


