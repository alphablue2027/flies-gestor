from PyQt5 import QtWidgets, QtGui
from .confirm_controllers import ConfirmControllers
from .accept_controlers import AcceptControllers
from .validators import *
from models.gestor import FliesGestor
from views.main_view import MainWindow
import sys

class MainController:
    def __init__(self) -> None:
        app = QtWidgets.QApplication(sys.argv)
        self.mp = MainWindow()
        self.ap = AcceptControllers()
        self.cp = ConfirmControllers()
        self.evts()
        self.getListPanel()
        self.mp.show()
        sys.exit(app.exec_())

    def getListPanel(self):
        if self.mp.listOptions.currentIndex() == 0:
            self.mp.getListPanel(0, FliesGestor.get_internationals())
        else:
            self.mp.getListPanel(1, FliesGestor.get_nationals())
    
    def getListNPanel(self):
        self.mp.getListNPanel()
    
    def addFlyPanel(self):
        if not FliesGestor.get_airlines():
            self.ap.show_accept_panel("Agregue primero aerolineas para continuar", False)
        else:
            self.mp.addFlyPanel(FliesGestor.get_airlines())
    
    def addAirlinePanel(self):
        self.mp.addAirlinePanel()

    def delFlyPanel(self):
        flies = FliesGestor.get_internationals() + FliesGestor.get_nationals()
        if not flies:
            self.ap.show_accept_panel("Agregue primero vuelos para continuar", False)
        else:
            self.mp.delFlyPanel(flies)
    
    def delAirlinePanel(self):
        if not FliesGestor.get_airlines():
            self.ap.show_accept_panel("Agregue primero aerolineas para continuar", False)
        else:
            self.mp.delAirlinePanel(FliesGestor.get_airlines())
    
    def getAirlinePanel(self):
        flies = FliesGestor.get_internationals() + FliesGestor.get_nationals()
        if not flies:
            self.ap.show_accept_panel("Agregue primero vuelos para continuar", False)
        else:
            self.mp.getAirlinePanel(flies)
    
    def getPorcentPanel(self):
        if not FliesGestor.get_internationals():
            self.ap.show_accept_panel("Agregue primero vuelos internacionales para continuar", False)
        else:
            self.mp.getPorcentPanel(FliesGestor.get_internationals())
    
    def getAvgPanel(self):
        if not FliesGestor.get_internationals():
            self.ap.show_accept_panel("Agregue primero vuelos internacionales para continuar", False)
        else:
            self.mp.getAvgPanel(FliesGestor.get_internationals())
    
    def getScalestPanel(self):
        if not FliesGestor.get_internationals():
            self.ap.show_accept_panel("Agregue primero vuelos internacionales para continuar", False)
        else:
            self.mp.getScalestPanel()
    
    def getListN(self):
        date = self.mp.getListN()
        flies = FliesGestor.get_outers_nflies(date)
        self.mp.setListN(flies)
    
    def addFly(self):
        code, inner, airline, init, end, datetime, mark, model, matr, capacity, *iattr = self.mp.addFly()
        acode = FliesGestor.get_airline_code(airline)
        if not is_name_valid(init, end, mark):
            self.ap.show_accept_panel("Los campos de ciudades y de la marca del avion no pueden estar vacios ni contener numeros", False)
        elif not is_fcode_valid(code, acode):
            self.ap.show_accept_panel("El codigo de vuelo debe comenzar con el codigo de aerolinea y contener luego de 3 - 4 digitos", False)
        elif not is_fcode_exist(code):
            self.ap.show_accept_panel("El codigo de vuelo ya esta en uso", False)
        elif not is_mm_valid(model, matr):
            self.ap.show_accept_panel("Los campos de modelo y matricula del avion no pueden estar vacios ni contener espacios", False)
        elif self.mp.listOptions.currentIndex() == 0:
            if not is_name_valid(iattr[0]):
                self.ap.show_accept_panel("El campo de destino no puede estar vacio ni contener numeros", False)
            FliesGestor.add_ifly(code, inner, airline, init, end, datetime, mark, model, matr, capacity, iattr[0], iattr[1], iattr[2])
            self.ap.show_accept_panel("Agregado correctamente", True)
        else:
            FliesGestor.add_nfly(code, inner, airline, init, end, datetime, mark, model, matr, capacity)
            self.ap.show_accept_panel("Agregado correctamente", True)
    
    def checkScale(self):
        self.mp.checkScale()
    
    def scaleZero(self):
        self.mp.scaleZero()
    
    def airlinesChange(self):
        a_name = self.mp.airlineAddInput.currentText()
        if a_name:
            a_code = FliesGestor.get_airline_code(a_name)
            self.mp.airlinesChange(a_code)
    
    def addAirline(self):
        code, name, nation, planes = self.mp.addAirline()
        if not is_name_valid(nation, name):
            self.ap.show_accept_panel("La nacionalidad y el nombre de la aerolinea no debe contener numeros ni estar vacio", False)
        elif not is_acode_valid(code):
            self.ap.show_accept_panel("El codigo de aerolinea debe contener exactamente 2 caracteres", False)
        elif not is_acode_exist(code):
            self.ap.show_accept_panel("El codigo de aerolinea ya esta en uso", False)
        elif not is_name_exist(name):
            self.ap.show_accept_panel("El nombre de aerolinea ya esta en uso", False)
        else:
            FliesGestor.add_airline(code, name, nation, planes)
            self.ap.show_accept_panel("Agregado correctamente", True)
    
    def delFly(self):
        code = self.mp.delFly()
        FliesGestor.del_fly(code)
        self.ap.show_accept_panel("Eliminado correctamente", True)
        self.delFlyPanel()
    
    def delAirline(self):
        if self.cp.show_confirm_panel("Esta accion eliminara ademas todos los vuelos asociados. Desea continuar?"):
            code = self.mp.delAirline()
            FliesGestor.del_airline(code)
            self.ap.show_accept_panel("Eliminada correctamente", True)
            self.delAirlinePanel()

    def getAirline(self):
        code = self.mp.codeGetAirInput.currentText()
        airline = FliesGestor.get_airline(code)
        if not airline:
            self.mp.getAirline(('N/A', 'N/A', 'N/A', 'N/A'))
        else:
            self.mp.getAirline((airline.name, airline.code, airline.nationality, str(airline.planes_number)))
    
    def getPorcent(self):
        mark = self.mp.markPorcentInput.currentText()
        airline = self.mp.airlinePorcentInput.currentText()
        result = FliesGestor.get_internationals_porcent(mark, airline)
        self.mp.getPorcent(result)

    def getScalest(self):
        date = self.mp.dateScalestInput.date().toPyDate()
        fly = FliesGestor.get_scalest_fly(date)
        self.mp.getScalest(fly)
    
    def getAvg(self):
        destiny = self.mp.destinyAvgInput.currentText()
        result = FliesGestor.get_passagers_avg(destiny)
        self.mp.getAvg(result)
    
    def changeAsidePanel(self):
        self.mp.changeAsidePanel()

    def mouseClicked(self, a0 : QtGui.QMouseEvent | None):
        self.mp.mouseClicked(a0)

    def minimize(self):
        self.mp.minimize()

    def maximize(self):
        self.mp.maximize()

    def exit(self):
        if FliesGestor.close():
            exit()
        elif self.cp.show_confirm_panel("Ha habido un error al guardar los datos, de continuar probablemente hayan perdidas. Cerrar de todos modos?"):
            exit()

    def evts(self):
        self.mp.listAsideButton.clicked.connect(self.getListPanel)
        self.mp.listOptions.currentIndexChanged.connect(self.getListPanel)
        self.mp.listNAsideButton.clicked.connect(self.getListNPanel)
        self.mp.addListButton.clicked.connect(self.addFlyPanel)
        self.mp.addAirAsideButton.clicked.connect(self.addAirlinePanel)
        self.mp.delListButton.clicked.connect(self.delFlyPanel)
        self.mp.delAirAsideButton.clicked.connect(self.delAirlinePanel)
        self.mp.getAirAsideButton.clicked.connect(self.getAirlinePanel)
        self.mp.porcentAsideButton.clicked.connect(self.getPorcentPanel)
        self.mp.avgAsideButton.clicked.connect(self.getAvgPanel)
        self.mp.scalestAsideButton.clicked.connect(self.getScalestPanel)

        self.mp.listNButton.clicked.connect(self.getListN)
        self.mp.addButton.clicked.connect(self.addFly)
        self.mp.scaleAddCheck.stateChanged.connect(self.checkScale)
        self.mp.numberAddInput.valueChanged.connect(self.scaleZero)
        self.mp.airlineAddInput.currentTextChanged.connect(self.airlinesChange)
        self.mp.addAButton.clicked.connect(self.addAirline)
        self.mp.delButton.clicked.connect(self.delFly)
        self.mp.delAButton.clicked.connect(self.delAirline)
        self.mp.findGetAirButton.clicked.connect(self.getAirline)
        self.mp.calcPorcentButton.clicked.connect(self.getPorcent)
        self.mp.calcAvgButton.clicked.connect(self.getAvg)
        self.mp.findScalestButton.clicked.connect(self.getScalest)

        self.mp.menuBttn.clicked.connect(self.changeAsidePanel)
        self.mp.overlay.mousePressEvent = self.mouseClicked
        self.mp.minBttn.clicked.connect(self.minimize)
        self.mp.maxBttn.clicked.connect(self.maximize)
        self.mp.exitBttn.clicked.connect(self.exit)