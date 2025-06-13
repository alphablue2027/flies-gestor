from PyQt5 import QtCore, QtWidgets, uic
from gestor import FliesGestor
from validators import *
import sys

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)

        self.config_menu_transitions()

        self.stackedWidget.setCurrentIndex(0)
        FliesGestor.clean_links()
        self.load()
    
    def config_menu_transitions(self):
        # self.overlay = QtWidgets.QWidget(self.frame)
        # self.overlay.setStyleSheet("background: transparent;")
        # self.overlay.hide()

        # olayout = QtWidgets.QHBoxLayout(self.overlay)
        # olayout.setContentsMargins(0, 0, 0, 0)


        self.transition = QtCore.QPropertyAnimation(self.asidePanel, b"maximumWidth")
        self.transition.setDuration(500)
        self.asidePanel.setMaximumWidth(0)
        self.asidePanel.raise_()

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

    def getListNPanel(self):
        self.stackedWidget.setCurrentIndex(1)

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
            print('Error')
        else:
            self.airlineAddInput.clear()
            for i in FliesGestor.get_airlines():
                self.airlineAddInput.addItem(i.name)
            self.stackedWidget.setCurrentIndex(2)

    def addAirlinePanel(self):
        self.stackedWidget.setCurrentIndex(3)

    def delFlyPanel(self):
        self.stackedWidget.setCurrentIndex(4)

    def delAirlinePanel(self):
        self.stackedWidget.setCurrentIndex(5)

    def getAirlinePanel(self):
        self.stackedWidget.setCurrentIndex(6)

    def getPorcentPanel(self):
        if not FliesGestor.get_internationals():
            pass
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

    def getAvgPanel(self):
        if not FliesGestor.get_internationals():
            pass
        else:
            self.destinyAvgInput.clear()
            destinies = set()
            for i in FliesGestor.get_internationals():
                destinies.add(i.destiny)
            self.destinyAvgInput.addItems(destinies)
            self.stackedWidget.setCurrentIndex(8)

    def getScalestPanel(self):
        self.stackedWidget.setCurrentIndex(9)
    
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
            print("Invalid names")
        elif not is_fcode_valid(code, acode):
            print("Invalid code")
        elif not is_mm_valid(model, matr):
            print("Invalid matr and model")
        elif self.listOptions.currentIndex() == 0:
            destiny = self.destinyAddInput.text().strip()
            if not (is_text_valid(destiny) and is_name_valid(destiny)):
                pass
            scale = self.scaleAddCheck.isChecked()
            number = self.numberAddInput.value()
            FliesGestor.add_ifly(code, inner, airline, init, end, datetime, mark, model, matr, capacity, destiny, scale, number)
        else: 
            FliesGestor.add_nfly(code, inner, airline, init, end, datetime, mark, model, matr, capacity)

    def checkScale(self):
        if not self.scaleAddCheck.isChecked():
            self.numberAddInput.setValue(0)
            self.numberAddInput.setEnabled(False)
        else:
            self.numberAddInput.setEnabled(True)

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

        if not is_name_valid(nation):
            pass
        elif not is_acode_valid(code):
            pass
        elif not is_aname_valid(name):
            pass
        else:
            FliesGestor.add_airline(code, name, nation, planes)

    def delFly(self):
        code = self.codeDelInput.text().strip()
        FliesGestor.del_fly(code)

    def delAirline(self):
        code = self.codeADelInput.text().strip().upper()
        FliesGestor.del_airline(code)

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
        else:
            self.asidePanel.raise_()
            self.transition.setStartValue(0)
            self.transition.setEndValue(w)

        self.transition.start()
        self.update()
        
    def closeEvent(self, a0):
        FliesGestor.close()
        if a0 != None:
            a0.accept()

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
        self.airlineAddInput.currentTextChanged.connect(self.airlinesChange)
        self.addAButton.clicked.connect(self.addAirline)
        self.delButton.clicked.connect(self.delFly)
        self.delAButton.clicked.connect(self.delAirline)
        self.findGetAirButton.clicked.connect(self.getAirline)
        self.calcPorcentButton.clicked.connect(self.getPorcent)
        self.calcAvgButton.clicked.connect(self.getAvg)
        self.findScalestButton.clicked.connect(self.getScalest)

        self.menuBttn.clicked.connect(self.changeAsidePanel)

    def load(self):
        self.evts()
        self.loadTable(0)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())