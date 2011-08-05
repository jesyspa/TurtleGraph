"""Provide a class for the main window.

"""

from PyQt4 import QtGui

class Window(QtGui.QWidget):
    """Represent the main window of TurtleGraph.

    """
    def __init__(self, parent=None):
        """Create the window."""
        import optionwidget
        QtGui.QWidget.__init__(self, parent)
        self.vertical_l = QtGui.QVBoxLayout(self)
        self.options_w = optionwidget.OptionWidget(self)
        self.button_w = QtGui.QPushButton('Plot', self)
        self.vertical_l.addWidget(self.options_w)
        self.vertical_l.addWidget(self.button_w)
        self.setLayout(self.vertical_l)
        self.show()

