from PyQt5 import QtCore, QtGui, QtWidgets, uic
from src.gestor import FliesGestor
from src.validators import *
from src import link
import sys, time

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("./design/main.ui", self)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.overlay = QtWidgets.QWidget(self.centralWidget())
        self.config_menu_transitions()

        self.av = AcceptPanel()
        self.cv = ConfirmPanel()

        self.oe = dict()

        self.stackedWidget.setCurrentIndex(0)
        FliesGestor.clean_links()
        self.load()
    
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

    def loadTable(self, c: int):
        match c:
            case 0:
                self.listTableI.setRowCount(0)
                self.stackedList.setCurrentIndex(1)
                for i, fly in enumerate(FliesGestor.get_internationals()):
                    self.listTableI.insertRow(i)
                    self.listTableI.setItem(i, 0, QtWidgets.QTableWidgetItem(fly.code))
                    self.listTableI.setItem(i, 1, QtWidgets.QTableWidgetItem(str(fly.inner)))
                    self.listTableI.setItem(i, 2, QtWidgets.QTableWidgetItem(fly.airline))
                    self.listTableI.setItem(i, 3, QtWidgets.QTableWidgetItem(fly.init_city))
                    self.listTableI.setItem(i, 4, QtWidgets.QTableWidgetItem(fly.end_city))
                    self.listTableI.setItem(i, 5, QtWidgets.QTableWidgetItem(str(fly.datetime)))
                    self.listTableI.setItem(i, 6, QtWidgets.QTableWidgetItem(fly.plane.mark))
                    self.listTableI.setItem(i, 7, QtWidgets.QTableWidgetItem(fly.plane.model))
                    self.listTableI.setItem(i, 8, QtWidgets.QTableWidgetItem(fly.plane.matricule))
                    self.listTableI.setItem(i, 9, QtWidgets.QTableWidgetItem(str(fly.plane.capacity)))
                    self.listTableI.setItem(i, 10, QtWidgets.QTableWidgetItem(fly.destiny))
                    self.listTableI.setItem(i, 11, QtWidgets.QTableWidgetItem(str(fly.scale)))
                    self.listTableI.setItem(i, 12, QtWidgets.QTableWidgetItem(str(fly.scale_number)))         
            case 1:
                self.listTableN.setRowCount(0)
                self.stackedList.setCurrentIndex(0)
                for i, fly in enumerate(FliesGestor.get_nationals()):
                    self.listTableN.insertRow(i)
                    self.listTableN.setItem(i, 0, QtWidgets.QTableWidgetItem(fly.code))
                    self.listTableN.setItem(i, 1, QtWidgets.QTableWidgetItem(str(fly.inner)))
                    self.listTableN.setItem(i, 2, QtWidgets.QTableWidgetItem(fly.airline))
                    self.listTableN.setItem(i, 3, QtWidgets.QTableWidgetItem(fly.init_city))
                    self.listTableN.setItem(i, 4, QtWidgets.QTableWidgetItem(fly.end_city))
                    self.listTableN.setItem(i, 5, QtWidgets.QTableWidgetItem(str(fly.datetime)))
                    self.listTableN.setItem(i, 6, QtWidgets.QTableWidgetItem(fly.plane.mark))
                    self.listTableN.setItem(i, 7, QtWidgets.QTableWidgetItem(fly.plane.model))
                    self.listTableN.setItem(i, 8, QtWidgets.QTableWidgetItem(fly.plane.matricule))
                    self.listTableN.setItem(i, 9, QtWidgets.QTableWidgetItem(str(fly.plane.capacity)))

    def getListPanel(self):
        self.loadTable(self.listOptions.currentIndex())
        self.stackedWidget.setCurrentIndex(0)
        self.changeAsidePanel()

    def getListNPanel(self):
        self.stackedWidget.setCurrentIndex(1)
        self.changeAsidePanel()

    def addFlyPanel(self):
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
        
        if not FliesGestor.get_airlines():
            self.get_acept_panel("Agregue primero aerolineas para continuar", False)
        else:
            self.airlineAddInput.clear()
            l = list(map(lambda f : f.name, FliesGestor.get_airlines()))
            self.airlineAddInput.addItems(l)
            self.stackedWidget.setCurrentIndex(2)

    def addAirlinePanel(self):
        self.stackedWidget.setCurrentIndex(3)
        self.changeAsidePanel()

    def delFlyPanel(self):
        self.stackedWidget.setCurrentIndex(4)

    def delAirlinePanel(self):
        if not FliesGestor.get_airlines():
            self.get_acept_panel("Agregue primero aerolineas para continuar", False)
        else:
            self.stackedWidget.setCurrentIndex(5)
            self.changeAsidePanel()

    def getAirlinePanel(self):
        if not (FliesGestor.get_internationals() + FliesGestor.get_nationals()):
            self.get_acept_panel("Agregue primero vuelos para continuar", False)
        else:
            self.stackedWidget.setCurrentIndex(6)
            self.changeAsidePanel()

    def getPorcentPanel(self):
        if not FliesGestor.get_internationals():
            self.get_acept_panel("Agregue primero vuelos internacionales para continuar", False)
        else:
            self.airlinePorcentInput.clear()
            airs = set()
            for i in FliesGestor.get_internationals():
                airs.add(i.airline)
            self.airlinePorcentInput.addItems(airs)
            
            self.markPorcentInput.clear()
            marks = set()
            for i in FliesGestor.get_internationals():
                marks.add(i.plane.mark)
            self.markPorcentInput.addItems(marks)

            self.stackedWidget.setCurrentIndex(7)
            self.changeAsidePanel()

    def getAvgPanel(self):
        if not FliesGestor.get_internationals():
            self.get_acept_panel("Agregue primero vuelos internacionales para continuar", False)
        else:
            self.destinyAvgInput.clear()
            destinies = set(map(lambda f : f.destiny, filter(lambda f : not f.inner, FliesGestor.get_internationals())))
            self.destinyAvgInput.addItems(destinies)
            self.stackedWidget.setCurrentIndex(8)
            self.changeAsidePanel()

    def getScalestPanel(self):
        if not FliesGestor.get_internationals():
            self.get_acept_panel("Agregue primero vuelos internacionales para continuar", False)
        else:
            self.stackedWidget.setCurrentIndex(9)
            self.changeAsidePanel()
    
    def get_acept_panel(self, txt : str, positive : bool):
        self.av.acceptLabel.setText(txt)
        if positive:
            self.av.acceptIcon.setPixmap(QtGui.QPixmap(":/icons/info.svg"))
            self.av.acceptButton.setStyleSheet("background: #3a9")
        else:
            self.av.acceptIcon.setPixmap(QtGui.QPixmap(":/icons/error.svg"))
            self.av.acceptButton.setStyleSheet("background: #a66")
        self.av.show()

    def get_confirm_panel(self, txt : str):
        self.cv.confirmLabel.setText(txt)
        self.cv.show()

    def getList(self):
        self.loadTable(self.listOptions.currentIndex())

    def getListN(self):
        date = self.dateListNInput.date().toPyDate()
        flies = FliesGestor.get_outers_nflies(date)
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

    def addFly(self):
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

        acode = FliesGestor.get_airline_code(airline)
        
        if not is_name_valid(init, end, mark):
            self.get_acept_panel("Los campos de ciudades y de la marca del avion no pueden estar vacios ni contener numeros", False)
        elif not is_fcode_valid(code, acode):
            self.get_acept_panel("El codigo de vuelo debe comenzar con el codigo de aerolinea y contener luego de 3 - 4 digitos", False)
        elif not is_fcode_exist(code):
            self.get_acept_panel("El codigo de vuelo ya esta en uso", False)
        elif not is_mm_valid(model, matr):
            self.get_acept_panel("Los campos de modelo y matricula del avion no pueden estar vacios ni contener espacios", False)
        elif self.listOptions.currentIndex() == 0:
            destiny = self.destinyAddInput.text().strip()
            if not (is_text_valid(destiny) and is_name_valid(destiny)):
                self.get_acept_panel("El campo de destino no puede estar vacio ni contener numeros", False)
            scale = self.scaleAddCheck.isChecked()
            number = self.numberAddInput.value()
            FliesGestor.add_ifly(code, inner, airline, init, end, datetime, mark, model, matr, capacity, destiny, scale, number)
            self.get_acept_panel("Agregado correctamente", True)
        else: 
            FliesGestor.add_nfly(code, inner, airline, init, end, datetime, mark, model, matr, capacity)
            self.get_acept_panel("Agregado correctamente", True)

    def checkScale(self):
        if not self.scaleAddCheck.isChecked():
            self.numberAddInput.setValue(0)
            self.numberAddInput.setEnabled(False)
        else:
            self.numberAddInput.setEnabled(True)
            self.numberAddInput.setValue(1)

    def scale_zero(self):
        number = self.numberAddInput.value()
        if number == 0:
            self.scaleAddCheck.setChecked(False)

    def airlinesChange(self):
        a_name = self.airlineAddInput.currentText()
        if a_name:
            a_code = FliesGestor.get_airline_code(a_name)
            self.codeAddInput.setText(a_code)

    def addAirline(self):
        code = self.codeAddAInput.text().strip().upper()
        name = self.nameAddAInput.text().strip().title()
        nation = self.nationAddAInput.text().strip()
        planes = self.planesAddAInput.value()

        if not is_name_valid(nation, name):
            self.get_acept_panel("La nacionalidad y el nombre de la aerolinea no debe contener numeros ni estar vacio", False)
        elif not is_acode_valid(code):
            self.get_acept_panel("El codigo de aerolinea debe contener exactamente 2 caracteres", False)
        elif not is_acode_exist(code):
            self.get_acept_panel("El codigo de aerolinea ya esta en uso", False)
        elif not is_aname_valid(name):
            self.get_acept_panel("El nombre de aerolinea ya esta en uso", False)
        else:
            FliesGestor.add_airline(code, name, nation, planes)
            self.get_acept_panel("Agregado correctamente", True)

    def delFly(self):
        code = self.codeDelInput.text().strip()
        FliesGestor.del_fly(code)

    def delAirline(self):
        self.get_confirm_panel("Esta accion eliminara ademas todos los vuelos asociados. Desea continuar?")
        self.cv.connect_del = True

    def getAirline(self):
        code = self.codeGetAirInput.text().strip()
        airline = FliesGestor.get_airline(code)
        if not airline:
            self.nameDataGetAir.setText("N/A")
            self.codeDataGetAir.setText("N/A")
            self.nationDataGetAir.setText("N/A")
            self.numberDataGetAir.setText("N/A")
        else:
            self.nameDataGetAir.setText(airline.name)
            self.codeDataGetAir.setText(airline.code)
            self.nationDataGetAir.setText(airline.nationality)
            self.numberDataGetAir.setText(str(airline.planes_number))

    def getPorcent(self):
        mark = self.markPorcentInput.currentText()
        airline = self.airlinePorcentInput.currentText()
        result = FliesGestor.get_internationals_porcent(mark, airline)
        self.countPorcentLabel.setText(str(result[0]))
        self.totalPorcentLabel.setText(str(result[1]))
        self.porcentBar.setValue(result[2])

    def getAvg(self):
        destiny = self.destinyAvgInput.currentText()
        result = FliesGestor.get_passagers_avg(destiny)
        self.resultAvgLabel.setText(str(result[0]))
        self.resultAvgTable.setRowCount(0)
        for i, fly in enumerate(result[1]):
            self.resultAvgTable.insertRow(i)
            self.resultAvgTable.setItem(i, 0, QtWidgets.QTableWidgetItem(fly.code))
            self.resultAvgTable.setItem(i, 1, QtWidgets.QTableWidgetItem(str(fly.plane.capacity)))

    def getScalest(self):
        date = self.dateScalestInput.date().toPyDate()
        fly = FliesGestor.get_scalest_fly(date)
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
            for widget, effect in self.oe.items():
                widget.setGraphicsEffect(effect)
        else:
            self.overlay.setGeometry(self.frame.geometry())
            self.overlay.show()
            self.overlay.raise_()
            
            self.oe[self.frame] = self.frame.graphicsEffect()
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
    
    def mouse_clicked(self, a0 : QtGui.QMouseEvent | None):
        self.changeAsidePanel()

    def accept(self):
        self.av.close()

    def confirm(self):
        self.cv.close()
        if self.cv.connect_del:
            code = self.codeADelInput.text().strip().upper()
            FliesGestor.del_airline(code)
        else:
            exit()

    def cancel(self):
        self.cv.close()

    def exit(self):
        if FliesGestor.close():
            exit()
        else:
            self.get_confirm_panel("Ha habido un error al guardar los datos, de continuar probablemente hayan perdidas. Cerrar de todos modos?")
            self.cv.connect_del = False


    def evts(self):
        self.listAsideButton.clicked.connect(self.getListPanel)
        self.listNAsideButton.clicked.connect(self.getListNPanel)
        self.addListButton.clicked.connect(self.addFlyPanel)
        self.addAirAsideButton.clicked.connect(self.addAirlinePanel)
        self.delListButton.clicked.connect(self.delFlyPanel)
        self.delAirAsideButton.clicked.connect(self.delAirlinePanel)
        self.getAirAsideButton.clicked.connect(self.getAirlinePanel)
        self.porcentAsideButton.clicked.connect(self.getPorcentPanel)
        self.avgAsideButton.clicked.connect(self.getAvgPanel)
        self.scalestAsideButton.clicked.connect(self.getScalestPanel)

        self.listOptions.currentIndexChanged.connect(self.getList)
        self.listNButton.clicked.connect(self.getListN)
        self.addButton.clicked.connect(self.addFly)
        self.scaleAddCheck.stateChanged.connect(self.checkScale)
        self.numberAddInput.valueChanged.connect(self.scale_zero)
        self.airlineAddInput.currentTextChanged.connect(self.airlinesChange)
        self.addAButton.clicked.connect(self.addAirline)
        self.delButton.clicked.connect(self.delFly)
        self.delAButton.clicked.connect(self.delAirline)
        self.findGetAirButton.clicked.connect(self.getAirline)
        self.calcPorcentButton.clicked.connect(self.getPorcent)
        self.calcAvgButton.clicked.connect(self.getAvg)
        self.findScalestButton.clicked.connect(self.getScalest)

        self.menuBttn.clicked.connect(self.changeAsidePanel)
        self.overlay.mousePressEvent = self.mouse_clicked
        self.exitBttn.clicked.connect(self.exit)
        self.cv.confirmButton.clicked.connect(self.confirm)
        self.cv.cancelButton.clicked.connect(self.cancel)
        self.av.acceptButton.clicked.connect(self.accept)

    def load(self):
        self.evts()
        self.loadTable(0)

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

class ConfirmPanel(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("./design/confirm.ui", self)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.confirmIcon.setPixmap(QtGui.QPixmap(":/icons/quest.svg"))
        self.connect_del = False
    
    def get_shadow(self, x, y, blur) -> QtWidgets.QGraphicsDropShadowEffect:
        shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(blur)
        shadow.setXOffset(x)
        shadow.setYOffset(y)
        shadow.setColor(QtCore.Qt.GlobalColor.lightGray)
        return shadow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())