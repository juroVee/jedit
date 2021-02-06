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

from ..settings import settings


class Tab:
    """
    Rodičovská trieda Tab, ktorá združuje základné parametre jedného tabu pracovnej plochy
    """

    def __init__(self, name=None, main_window=None, sidebar=None, footer=None):
        self.name = name if name else 'Untitled Tab'
        self.main_window = main_window if main_window else []
        self.sidebar = sidebar if sidebar else []
        self.footer = footer if footer else []
        self.board_grid_rows = settings['default_sizes']['board_grid_rows']
        self.board_grid_cols = settings['default_sizes']['board_grid_cols']
        self.height = settings['default_sizes']['board_grid_height']
        self.main_window_rows = settings['default_sizes']['main_window_rows']
        self.main_window_cols = settings['default_sizes']['main_window_cols']


class AnalysisTab(Tab):
    """
    Tab Analýza a jeho vlastnosti
    """

    def __init__(self, board=None):
        function_manager = board.get_object('function_manager')
        menu = board.get_object('main_menu')
        logger = board.get_object('logger')
        logger_mini_tab = w.Tab(children=[logger.get_widget(t='mini')], layout=w.Layout(height='100%'))
        logger_mini_tab.set_title(0, 'Posledná zmena')
        super().__init__(name='Analýza',
                         main_window=[function_manager.get_plot_widget()],
                         sidebar=[menu.get_widget()],
                         footer=[logger_mini_tab] if settings['editor']['footer_log'] == 'yes' else []
                         )

    def get_widget(self) -> w.GridspecLayout:
        grid = w.GridspecLayout(self.board_grid_rows, self.board_grid_cols, height=self.height)
        grid[:self.main_window_rows, :self.main_window_cols] = w.VBox(children=self.main_window)
        grid[:self.main_window_rows, self.main_window_cols:] = w.VBox(children=self.sidebar)
        grid[self.main_window_rows:, :self.board_grid_cols] = w.VBox(children=self.footer)
        return grid


class LogTab(Tab):
    """
    Tab Výstupy a jeho vlastnosti
    """

    def __init__(self, board=None):
        logger = board.get_object('logger')
        super().__init__(name='Výstupy', main_window=[logger.get_widget(t='main')])

    def get_widget(self) -> w.GridspecLayout:
        grid = w.GridspecLayout(self.board_grid_rows, self.board_grid_cols, height=self.height)
        grid[:self.board_grid_rows, :self.board_grid_cols] = w.VBox(children=self.main_window)
        return grid


class WarningTab(Tab):
    """
    Tab Upozornenia a jeho vlastnosti
    """

    def __init__(self, board=None):
        logger = board.get_object('logger')
        super().__init__(name='Upozornenia', main_window=[logger.get_widget(t='warnings')])

    def get_widget(self) -> w.GridspecLayout:
        grid = w.GridspecLayout(self.board_grid_rows, self.board_grid_cols, height=self.height)
        grid[:self.board_grid_rows, :self.board_grid_cols] = w.VBox(children=self.main_window)
        return grid
