# SPDX-License-Identifier: AGPL-3.0-with-Commons-Clause
# Copyright (C) 2025 Ordnay Perez Hernandez - ¡Uso comercial prohibido sin permiso!
from views.confirm_view import ConfirmPanel

class ConfirmControllers:
    def __init__(self):
        self.cv = ConfirmPanel()
        self.evts()

    def show_confirm_panel(self, txt : str) -> bool:
        return self.cv.get_confirm_panel(txt)
    
    def evts(self):
        self.cv.confirmButton.clicked.connect(self.cv.accept)
        self.cv.cancelButton.clicked.connect(self.cv.reject)