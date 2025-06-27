# SPDX-License-Identifier: AGPL-3.0-with-Commons-Clause
# Copyright (C) 2025 Ordnay Perez Hernandez - ¡Uso comercial prohibido sin permiso!
from views.accept_view import AcceptPanel

class AcceptControllers:
    def __init__(self) -> None:
        self.av = AcceptPanel()
        self.evts()
    
    def accept(self):
        self.av.close()

    def show_accept_panel(self, txt : str, positive : bool):
        self.av.get_acept_panel(txt, positive)

    def evts(self):
        self.av.acceptButton.clicked.connect(self.accept)