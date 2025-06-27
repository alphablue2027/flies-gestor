# SPDX-License-Identifier: AGPL-3.0-with-Commons-Clause
# Copyright (C) 2025 Ordnay Perez Hernandez - ¡Uso comercial prohibido sin permiso!
from PyQt5 import QtWidgets, QtGui, QtCore, uic
from models import link

class AcceptPanel(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("./views/ui/accept.ui", self)
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
        self.acceptLabel.setText(txt)
        if positive:
            self.acceptIcon.setPixmap(QtGui.QPixmap(":/icons/info.svg"))
            self.acceptButton.setStyleSheet("background: #3a9")
        else:
            self.acceptIcon.setPixmap(QtGui.QPixmap(":/icons/error.svg"))
            self.acceptButton.setStyleSheet("background: #a66")
        self.show()