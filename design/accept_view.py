from PyQt5 import QtWidgets, QtGui, QtCore, uic

class AcceptPanel(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("./design/accept.ui", self)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
    
    def get_shadow(self, x, y, blur) -> QtWidgets.QGraphicsDropShadowEffect:
        shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(blur)
        shadow.setXOffset(x)
        shadow.setYOffset(y)
        shadow.setColor(QtCore.Qt.GlobalColor.lightGray)
        return shadow

    def get_acept_panel(self, txt : str, positive : bool):
        self.av.acceptLabel.setText(txt)
        if positive:
            self.av.acceptIcon.setPixmap(QtGui.QPixmap(":/icons/info.svg"))
            self.av.acceptButton.setStyleSheet("background: #3a9")
        else:
            self.av.acceptIcon.setPixmap(QtGui.QPixmap(":/icons/error.svg"))
            self.av.acceptButton.setStyleSheet("background: #a66")
        self.av.show()