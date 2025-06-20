from ..design.confirm_view import ConfirmPanel
from ..design.main_view import MainWindow
from ..src.gestor import FliesGestor

class ConfirmControllers:
    def __init__(self):
        self.cv = ConfirmPanel()
        self.evts()

    def show_confirm_panel(self, txt : str) -> bool:
        return self.cv.get_confirm_panel(txt)
    
    def evts(self):
        self.cv.confirmButton.clicked.connect(self.cv.accept)
        self.cv.cancelButton.clicked.connect(self.cv.reject)