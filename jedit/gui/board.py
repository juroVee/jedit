"""
JEDIT, editor which allows interactive exploration of the properties of elementary
functions in the computing environment IPython/Jupyter
Copyright (C) 2020 Juraj Vetrák

This file is part of JEDIT, editor which allows interactive
exploration of the properties of elementary functions in the computing environment IPython/Jupyter.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program (license.txt).  If not, see https://www.gnu.org/licenses/agpl-3.0.html.
"""

import ipywidgets as w

from .menu import MainMenu
from .observer import Observer
from .tabs import AnalysisTab, LogTab, WarningTab
from ..analysis import FunctionManager


class Board:
    """
    Trieda reprezentujúca základný grafický objekt - pracovnú plochu v podobe troch objektov Tab:
        - Analýza
        - Výstupy
        - Upozornenia
    """

    def __init__(self, user_params, logger):
        self.logger = logger
        self.function_manager = FunctionManager(user_params, logger)
        self.main_menu = MainMenu()
        tabs = [AnalysisTab(board=self),
                LogTab(board=self),
                WarningTab(board=self)]
        self.tab_parent = w.Tab(children=[tab.get_widget() for tab in tabs])
        for i, tab in enumerate(tabs):
            self.tab_parent.set_title(i, tab.name)
        self.observer = Observer(self)
        self.observer.start()

    def get_object(self, object_name):
        if hasattr(self, object_name):
            return getattr(self, object_name)

    def get_widget(self) -> w.VBox:
        return w.VBox(children=[self.tab_parent])
