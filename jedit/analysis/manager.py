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

import warnings

import ipywidgets as w
import matplotlib.pyplot as plt
from IPython.display import clear_output, display

from .computations import ComputationsManager
from .function import Function
from .warn import WarningsManager
from ..settings import settings


class FunctionManager:
    """
    Trieda pre načítanie grafu zadanej funkcie a kontrolu jeho aktualizovania.
    """

    def __init__(self, user_parameters, logger):
        """
        Vytvorí nový objekt Output pre vykreslenie grafu funkcie, načíta zadanú funkciu a jej parametre.
        :param user_parameters:
        :param logger:
        """
        self.output = w.Output(layout=w.Layout(overflow='hidden'))
        plt.ioff()
        self.fig, self.ax = plt.subplots()
        self.fig.set_size_inches(settings['plot_parameters']['width'], settings['plot_parameters']['height'])
        plt.subplots_adjust(left=0.08, bottom=0.08, right=0.92, top=0.92, wspace=0, hspace=0)
        self.function = Function(user_parameters)
        self.updates = 0
        self.warnings = WarningsManager(logger)

    def get_function(self) -> Function:
        return self.function

    def update_plot(self, **kwargs) -> None:
        """
        Spustí prepočty hodnôt funkcie a vykreslí ich do grafu.
        :param kwargs: Zadané kľúče pre výpočet hodnôt v ComputationsManager
        :return:
        """
        function = self.get_function()
        if len(kwargs) > 0:
            manager = ComputationsManager(function=function)
            for arg, value in kwargs.items():
                if value:
                    with warnings.catch_warnings(record=True) as warnings_list:
                        warnings.simplefilter("always")
                        getattr(manager, arg)()
                        self.warnings.add(warnings_list, category=arg)
        self.warnings.print()
        if self.updates > 0:
            plt.close('all')
        function.plot(self.ax)
        self.updates += 1
        with self.output:
            clear_output(wait=True)
            display(self.ax.figure)
        plt.ion()

    def get_plot_widget(self):
        return self.output
