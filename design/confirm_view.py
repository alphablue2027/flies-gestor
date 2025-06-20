from PyQt5 import QtWidgets, QtCore, QtGui, uic
from ..src.gestor import FliesGestor

class ConfirmPanel(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent, QtCore.Qt.WindowType.WindowSystemMenuHint)
        uic.loadUi("./confirm.ui", self)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.confirmIcon.setPixmap(QtGui.QPixmap(":/icons/quest.svg"))
    
    def get_shadow(self, x, y, blur) -> QtWidgets.QGraphicsDropShadowEffect:
        shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(blur)
        shadow.setXOffset(x)
        shadow.setYOffset(y)
        shadow.setColor(QtCore.Qt.GlobalColor.lightGray)
        return shadow
    
    def get_confirm_panel(self, txt : str):
        self.confirmLabel.setText(txt)
        return self.exec_() == QtWidgets.QDialog.accepted