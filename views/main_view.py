from PyQt5 import QtWidgets, QtGui, QtCore, uic
from datetime import date
from models import link

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("./views/ui/main.ui", self)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.maximized = False

        self.overlay = QtWidgets.QWidget(self.centralWidget())
        self.config_menu_transitions()

        self.oe = self.frame.graphicsEffect()

        self.stackedWidget.setCurrentIndex(0)

    def config_menu_transitions(self):
        self.overlay.setStyleSheet("background: transparent;\nborder-radius: 0;")
        self.overlay.hide()

        olayout = QtWidgets.QHBoxLayout(self.overlay)
        olayout.setContentsMargins(0, 0, 0, 0)
        olayout.setSpacing(0)

        self.asidePanel.setParent(self.overlay)

        self.spacer_lay = QtWidgets.QWidget()
        self.spacer_lay.setStyleSheet("background: rgba(0, 0, 0, 0.3);")

        self.topPanel.setGraphicsEffect(self.get_shadow(0, 10, 15))
        self.asidePanel.setGraphicsEffect(self.get_shadow(5, 0, 15))

        olayout.addWidget(self.asidePanel)
        olayout.addWidget(self.spacer_lay)

        self.transition = QtCore.QPropertyAnimation(self.asidePanel, b"maximumWidth")
        self.transition.setDuration(400)
        self.asidePanel.setMaximumWidth(0)

    def get_shadow(self, x, y, blur) -> QtWidgets.QGraphicsDropShadowEffect:
        shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(blur)
        shadow.setXOffset(x)
        shadow.setYOffset(y)
        shadow.setColor(QtCore.Qt.GlobalColor.lightGray)
        return shadow

    def loadTable(self, c: int, flies : list):
        match c:
            case 0:
                self.listTableI.setRowCount(0)
                self.stackedList.setCurrentIndex(1)
                for i, fly in enumerate(flies):
                    self.listTableI.insertRow(i)
                    self.listTableI.setItem(i, 0, QtWidgets.QTableWidgetItem(fly.code))
                    self.listTableI.setItem(i, 1, QtWidgets.QTableWidgetItem("Si" if fly.inner else "No"))
                    self.listTableI.setItem(i, 2, QtWidgets.QTableWidgetItem(fly.airline))
                    self.listTableI.setItem(i, 3, QtWidgets.QTableWidgetItem(fly.init_city))
                    self.listTableI.setItem(i, 4, QtWidgets.QTableWidgetItem(fly.end_city))
                    self.listTableI.setItem(i, 5, QtWidgets.QTableWidgetItem(str(fly.datetime)))
                    self.listTableI.setItem(i, 6, QtWidgets.QTableWidgetItem(fly.plane.mark))
                    self.listTableI.setItem(i, 7, QtWidgets.QTableWidgetItem(fly.plane.model))
                    self.listTableI.setItem(i, 8, QtWidgets.QTableWidgetItem(fly.plane.matricule))
                    self.listTableI.setItem(i, 9, QtWidgets.QTableWidgetItem(str(fly.plane.capacity)))
                    self.listTableI.setItem(i, 10, QtWidgets.QTableWidgetItem(fly.destiny))
                    self.listTableI.setItem(i, 11, QtWidgets.QTableWidgetItem("Si" if fly.scale else "No"))
                    self.listTableI.setItem(i, 12, QtWidgets.QTableWidgetItem(str(fly.scale_number)))
            case 1:
                self.listTableN.setRowCount(0)
                self.stackedList.setCurrentIndex(0)
                for i, fly in enumerate(flies):
                    self.listTableN.insertRow(i)
                    self.listTableN.setItem(i, 0, QtWidgets.QTableWidgetItem(fly.code))
                    self.listTableN.setItem(i, 1, QtWidgets.QTableWidgetItem("Si" if fly.inner else "No"))
                    self.listTableN.setItem(i, 2, QtWidgets.QTableWidgetItem(fly.airline))
                    self.listTableN.setItem(i, 3, QtWidgets.QTableWidgetItem(fly.init_city))
                    self.listTableN.setItem(i, 4, QtWidgets.QTableWidgetItem(fly.end_city))
                    self.listTableN.setItem(i, 5, QtWidgets.QTableWidgetItem(str(fly.datetime)))
                    self.listTableN.setItem(i, 6, QtWidgets.QTableWidgetItem(fly.plane.mark))
                    self.listTableN.setItem(i, 7, QtWidgets.QTableWidgetItem(fly.plane.model))
                    self.listTableN.setItem(i, 8, QtWidgets.QTableWidgetItem(fly.plane.matricule))
                    self.listTableN.setItem(i, 9, QtWidgets.QTableWidgetItem(str(fly.plane.capacity)))

    def getListPanel(self, t : int, flies : list):
        self.loadTable(t, flies)
        self.stackedWidget.setCurrentIndex(0)
        if self.overlay.isVisible():
            self.changeAsidePanel()

    def getListNPanel(self):
        self.stackedWidget.setCurrentIndex(1)
        if self.overlay.isVisible():
            self.changeAsidePanel()

    def addFlyPanel(self, airlines : list):
        if self.listOptions.currentIndex() == 1:
            self.destinyAddInput.setVisible(False)
            self.scaleAddCheck.setVisible(False)
            self.numberAddInput.setVisible(False)
            self.destinyAddLabel.setVisible(False)
            self.scaleAddLabel.setVisible(False)
            self.numberAddLabel.setVisible(False)
        else:
            self.destinyAddInput.setVisible(True)
            self.scaleAddCheck.setVisible(True)
            self.numberAddInput.setVisible(True)
            self.destinyAddLabel.setVisible(True)
            self.scaleAddLabel.setVisible(True)
            self.numberAddLabel.setVisible(True)

        self.airlineAddInput.clear()
        l = list(map(lambda f : f.name, airlines))
        self.airlineAddInput.addItems(l)
        self.stackedWidget.setCurrentIndex(2)

    def addAirlinePanel(self):
        self.stackedWidget.setCurrentIndex(3)
        if self.overlay.isVisible():
            self.changeAsidePanel()

    def delFlyPanel(self, flies : list):
        self.codeDelInput.clear()
        codes = list(map(lambda f : f.code, (flies)))
        self.codeDelInput.addItems(codes)
        self.stackedWidget.setCurrentIndex(4)

    def delAirlinePanel(self, airlines : list):
        self.codeADelInput.clear()
        codes = list(map(lambda a : a.code, airlines))
        self.codeADelInput.addItems(codes)
        self.stackedWidget.setCurrentIndex(5)
        if self.overlay.isVisible():
            self.changeAsidePanel()

    def getAirlinePanel(self, flies : list):
            self.codeGetAirInput.clear()
            codes = list(map(lambda f : f.code, flies))
            self.codeGetAirInput.addItems(codes)
            self.stackedWidget.setCurrentIndex(6)
            if self.overlay.isVisible():
                self.changeAsidePanel()

    def getPorcentPanel(self, flies : list):
        self.airlinePorcentInput.clear()
        airs = set(map(lambda f : f.airline, flies))
        self.airlinePorcentInput.addItems(airs)

        self.markPorcentInput.clear()
        marks = set(map(lambda f : f.plane.mark, flies))
        self.markPorcentInput.addItems(marks)

        self.stackedWidget.setCurrentIndex(7)
        if self.overlay.isVisible():
            self.changeAsidePanel()

    def getAvgPanel(self, flies : list):
        self.destinyAvgInput.clear()
        destinies = set(map(lambda f : f.destiny, filter(lambda f : not f.inner, flies)))
        self.destinyAvgInput.addItems(destinies)

        self.stackedWidget.setCurrentIndex(8)
        if self.overlay.isVisible():
            self.changeAsidePanel()

    def getScalestPanel(self):
        self.stackedWidget.setCurrentIndex(9)
        if self.overlay.isVisible():
            self.changeAsidePanel()

    def getListN(self) -> date:
        date = self.dateListNInput.date().toPyDate()
        return date

    def setListN(self, flies : list):
        self.listNTable.setRowCount(0)
        for i, fly in enumerate(flies):
            self.listNTable.insertRow(i)
            self.listNTable.setItem(i, 0, QtWidgets.QTableWidgetItem(fly.code))
            self.listNTable.setItem(i, 1, QtWidgets.QTableWidgetItem(str(fly.inner)))
            self.listNTable.setItem(i, 2, QtWidgets.QTableWidgetItem(fly.airline))
            self.listNTable.setItem(i, 3, QtWidgets.QTableWidgetItem(fly.init_city))
            self.listNTable.setItem(i, 4, QtWidgets.QTableWidgetItem(fly.end_city))
            self.listNTable.setItem(i, 5, QtWidgets.QTableWidgetItem(str(fly.datetime)))
            self.listNTable.setItem(i, 6, QtWidgets.QTableWidgetItem(fly.plane.mark))
            self.listNTable.setItem(i, 7, QtWidgets.QTableWidgetItem(fly.plane.model))
            self.listNTable.setItem(i, 8, QtWidgets.QTableWidgetItem(fly.plane.matricule))
            self.listNTable.setItem(i, 9, QtWidgets.QTableWidgetItem(str(fly.plane.capacity)))

    def addFly(self) -> tuple:
        code = self.codeAddInput.text().strip().upper()
        inner = self.inAddCheck.isChecked()
        airline = self.airlineAddInput.currentText()
        init = self.initAddInput.text().strip().title()
        end = self.endAddInput.text().strip().title()
        datetime = self.dateAddInput.dateTime().toPyDateTime()
        mark = self.markAddInput.text().strip().title()
        model = self.modelAddInput.text().strip().upper()
        matr = self.matrAddInput.text().strip().upper()
        capacity = self.capacityAddInput.value()
        if self.listOptions.currentIndex() == 0:
            destiny = self.destinyAddInput.text().strip()
            scale = self.scaleAddCheck.isChecked()
            number = self.numberAddInput.value()
            return (code, inner, airline, init, end, datetime, mark, model, matr, capacity, destiny, scale, number)
        else:
            return (code, inner, airline, init, end, datetime, mark, model, matr, capacity)

    def checkScale(self):
        if not self.scaleAddCheck.isChecked():
            self.numberAddInput.setValue(0)
            self.numberAddInput.setEnabled(False)
        else:
            self.numberAddInput.setEnabled(True)
            self.numberAddInput.setValue(1)

    def scaleZero(self):
        number = self.numberAddInput.value()
        if number == 0:
            self.scaleAddCheck.setChecked(False)

    def airlinesChange(self, a_code : str):
        self.codeAddInput.setText(a_code)

    def addAirline(self):
        code = self.codeAddAInput.text().strip().upper()
        name = self.nameAddAInput.text().strip().title()
        nation = self.nationAddAInput.text().strip()
        planes = self.planesAddAInput.value()
        return (code, name, nation, planes)

    def delFly(self) -> str:
        code = self.codeDelInput.currentText()
        return code

    def delAirline(self) -> str:
        code = self.codeADelInput.currentText()
        return code

    def getAirline(self, attr : tuple):
        self.nameDataGetAir.setText(attr[0])
        self.codeDataGetAir.setText(attr[1])
        self.nationDataGetAir.setText(attr[2])
        self.numberDataGetAir.setText(attr[3])

    def getPorcent(self, result : tuple):
        self.countPorcentLabel.setText(str(result[0]))
        self.totalPorcentLabel.setText(str(result[1]))
        self.porcentBar.setValue(result[2])

    def getAvg(self, result : tuple):
        self.resultAvgLabel.setText(str(result[0]))
        self.resultAvgTable.setRowCount(0)
        for i, fly in enumerate(result[1]):
            self.resultAvgTable.insertRow(i)
            self.resultAvgTable.setItem(i, 0, QtWidgets.QTableWidgetItem(fly.code))
            self.resultAvgTable.setItem(i, 1, QtWidgets.QTableWidgetItem(str(fly.plane.capacity)))

    def getScalest(self, fly):
        if not fly:
            self.codeScalestLabel.setText("N/A")
            self.innerScalestLabel.setText("N/A")
            self.airlineScalestLabel.setText("N/A")
            self.initScalestLabel.setText("N/A")
            self.endScalestLabel.setText("N/A")
            self.dateScalestLabel.setText("N/A")
            self.markScalestLabel.setText("N/A")
            self.modelScalestLabel.setText("N/A")
            self.matrScalestLabel.setText("N/A")
            self.capacityScalestLabel.setText("N/A")
            self.destinyScalestLabel.setText("N/A")
            self.scaleScalestLabel.setText("N/A")
            self.numberScalestLabel.setText("N/A")
        else:
            self.codeScalestLabel.setText(fly.code)
            self.innerScalestLabel.setText(str(fly.inner))
            self.airlineScalestLabel.setText(fly.airline)
            self.initScalestLabel.setText(fly.init_city)
            self.endScalestLabel.setText(fly.end_city)
            self.dateScalestLabel.setText(str(fly.datetime.date()))
            self.markScalestLabel.setText(fly.plane.mark)
            self.modelScalestLabel.setText(fly.plane.model)
            self.matrScalestLabel.setText(fly.plane.matricule)
            self.capacityScalestLabel.setText(str(fly.plane.capacity))
            self.destinyScalestLabel.setText(fly.destiny)
            self.scaleScalestLabel.setText(str(fly.scale))
            self.numberScalestLabel.setText(str(fly.scale_number))

    def changeAsidePanel(self):
        w = 300

        if self.asidePanel.maximumWidth() == 300:
            self.transition.setStartValue(w)
            self.transition.setEndValue(0)
            self.transition.finished.connect(self.overlay.hide)
            self.frame.setGraphicsEffect(self.oe)
        else:
            self.overlay.setGeometry(self.frame.geometry())
            self.overlay.show()
            self.overlay.raise_()

            blur = QtWidgets.QGraphicsBlurEffect()
            blur.setBlurRadius(4)
            self.frame.setGraphicsEffect(blur)

            self.transition.setStartValue(0)
            self.transition.setEndValue(w)
            try:
                self.transition.finished.disconnect(self.overlay.hide)
            except:
                pass

        self.transition.start()
        self.update()

    def mouseClicked(self, a0 : QtGui.QMouseEvent | None):
        self.changeAsidePanel()

    def minimize(self):
        self.showMinimized()

    def maximize(self):
        if self.maximized:
            self.showNormal()
            self.maxBttn.setIcon(QtGui.QIcon(QtGui.QPixmap(":/icons/max")))
            self.maximized = False
        else:
            if self.overlay.isVisible():
                self.overlay.hide()
                self.frame.setGraphicsEffect(self.oe)
            self.showMaximized()
            self.maxBttn.setIcon(QtGui.QIcon(QtGui.QPixmap(":/icons/maxr")))
            self.maximized = True