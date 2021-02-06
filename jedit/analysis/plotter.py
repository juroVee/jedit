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

from .util import init_subplot
from ..settings import settings


class Plotter:
    """
    Trieda združujúca metódy, ktoré vykresľujú údaje do grafu.
    """

    def __init__(self, function, axes):
        self.function, self.ax = function, axes

    def plot_main_function(self) -> None:
        """
        Vykreslí užívateľom zadanú alebo predvolenú funkciu (intervaly X a príslušné funkčné hodnoty)
        :return:
        """
        f = self.function.get('f')
        for X in self.function.get('x_values'):
            init_subplot(self.ax)
            for param in self.function.parameters:
                try:
                    method = getattr(self.ax, 'set_' + param)
                    method(self.function.get(param))
                except AttributeError:
                    pass
            self.ax.grid(self.function.get('grid'))
            self.ax.plot(X, f(X),
                         color=self.function.get('main_function_color'),
                         linestyle=settings['main_function']['linestyle'],
                         linewidth=settings['main_function']['linewidth'],
                         zorder=3)

    def plot_derivatives(self):
        """
        Vykreslí predvolený počet derivácii, ak sa ich užívateľ rozhodol zobraziť.
        :return:
        """
        for i, Xi in enumerate(self.function.get('x_values')):
            for n in range(1, settings['derivative']['user_max'] + 1):
                key, primes = f'X{i}', self.function.get_analysis_data(key=f'primes{n}')
                if self.function.get(f'active_derivative{n}'):
                    color = self.function.get('derivative_color' + str(n))
                    linestyle = settings['derivative']['linestyle']
                    linewidth = settings['derivative']['linewidth']
                    self.ax.plot(Xi, primes[key],
                                 color=color,
                                 linestyle=linestyle,
                                 linewidth=linewidth,
                                 zorder=2)

    def plot_zero_points(self) -> None:
        """
        Vykreslí nulové body, ak sa ich užívateľ rozhodol zobraziť.
        :return:
        """
        if self.function.get('zero_points_visible'):
            marker = settings['zero_points']['marker']
            markersize = settings['zero_points']['markersize']
            zorder = self.function.get('zero_points_zorder')
            f = self.function.get('f')
            zero_points = self.function.get_analysis_data(key='zero_points', unpack=True)
            self.ax.plot(zero_points, f(zero_points), marker, c=self.function.get('zero_points_color'),
                         markersize=markersize, zorder=zorder)

    def plot_extremes(self) -> None:
        """
        Vykreslí ostré lokálne extrémy, ak sa ich užívateľ rozhodol zobraziť.
        :return:
        """
        if self.function.get('extremes_visible'):
            marker = settings['extremes']['marker']
            markersize = settings['extremes']['markersize']
            zorder = self.function.get('extremes_zorder')
            f = self.function.get('f')
            extremes = self.function.get_analysis_data(key='extremes', unpack=True)
            self.ax.plot(extremes, f(extremes), marker, c=self.function.get('extremes_color'), markersize=markersize,
                         zorder=zorder)

    def plot_inflex_points(self) -> None:
        """
        Vykreslí inflexné body, ak sa ich užívateľ rozhodol zobraziť.
        :return:
        """
        if self.function.get('inflex_points_visible'):
            marker = settings['inflex_points']['marker']
            markersize = settings['inflex_points']['markersize']
            zorder = self.function.get('inflex_points_zorder')
            f = self.function.get('f')
            inflex_points = self.function.get_analysis_data(key='inflex_points', unpack=True)
            self.ax.plot(inflex_points, f(inflex_points), marker, c=self.function.get('inflex_points_color'),
                         markersize=markersize, zorder=zorder)

    def plot_intervals(self, op) -> None:
        """
        Vykreslí intervaly monotónnosti/konvexnosti/konkávnosti, ak sa ich užívateľ rozhodol zobraziť.
        :param op:
        :return:
        """
        if self.function.get(f'{op}_visible'):
            linestyle = settings[op]['linestyle']
            linewidth = settings[op]['linewidth']
            color = self.function.get(f'{op}_color')
            f = self.function.get('f')
            zorder = self.function.get(f'{op}_zorder')
            for interval in self.function.get_analysis_data(key=op, unpack=True, list_values=True):
                self.ax.plot(interval, f(interval), color=color, linestyle=linestyle, linewidth=linewidth,
                             zorder=zorder)

    def plot_all(self) -> None:
        """
        Združujúca metóda pre vykreslenie všetkých informácii vybratých užívateľom do grafu.
        :return:
        """
        self.plot_main_function()
        self.plot_derivatives()
        self.plot_zero_points()
        self.plot_extremes()
        self.plot_inflex_points()
        for op in 'increasing', 'decreasing', 'concave_up', 'concave_down':
            self.plot_intervals(op)
