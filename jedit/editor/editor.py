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

from IPython.display import display
from matplotlib import get_backend

from .exceptions import NotSupportedException, ParameterError
from .util import hide_interactive_toolbars, check_parameters
from ..gui import Board, Logger
from ..settings import settings


class Editor:
    """
    Trieda, ktorá načíta všetky potrebné inštancie objektov a spustí prvý výpočet hodnôt.
    """

    def __init__(self):
        self.board = None
        self.logger = Logger()

    def run_instance(self, **params) -> None:
        if not settings['editor']['interactive_elements'] == 'yes':
            hide_interactive_toolbars()
        if 'inline' in get_backend():
            raise NotSupportedException('Clause %matplotlib inline is not supported. Please use %matplotlib notebook.')
        for t in 'main', 'mini', 'warnings':
            self.logger.get_widget(t).clear_output()
        error_message, parameters = check_parameters(params)
        if error_message is not None:
            raise ParameterError(error_message)
        self.board = Board(parameters, self.logger)
        function_manager = self.board.get_object('function_manager')
        display(self.board.get_widget())
        function_manager.update_plot(main_function=True, main_derivatives=True, zero_points=True,
                                     extremes=True, inflex_points=True, monotonic=True, concave=True)
