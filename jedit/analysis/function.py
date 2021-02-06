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

import itertools
from collections import defaultdict

import numpy as np

from .plotter import Plotter
from ..settings import settings


class Function:
    """
    Trieda, ktorá načíta a spravuje všetky parametre užívateľskej funkcie
    """

    def __init__(self, user_parameters):
        self.parameters, self.analysis_data = {}, defaultdict(dict)
        self._init_function_details(user_parameters)
        self._init_plot_parameters(user_parameters)
        self._init_derivatives()
        self._init_zero_points()
        for op in 'extremes', 'inflex_points', 'increasing', 'decreasing', 'concave_up', 'concave_down':
            self._init_analysis(op)

    def _init_function_details(self, user_parameters):
        self.set('x_values', user_parameters['intervals'])
        self.set('original_x_values', user_parameters['intervals'])
        self.set('f', user_parameters['function'])
        self.set('user_derivatives', {i + 1: user_parameters.get('primes', [])[i] for i in range(len(user_parameters.get('primes', [])))})
        self.set('rounding', settings['editor']['round']['default'])
        self.set('refinement', 1)

    def _init_plot_parameters(self, user_parameters):
        self.set('grid', True if settings['plot_parameters']['grid'] == 'yes' else False)
        self.set('main_function_color', settings['main_function']['color'])
        ax = user_parameters['axes']
        for param in 'aspect', 'xticks', 'yticks', 'xlim', 'ylim':
            if hasattr(ax, f'get_{param}'):
                self.set(param, getattr(ax, f'get_{param}')())
        if ax.get_xticklabels()[0].get_text() != '':
            self.set('xticklabels', ax.get_xticklabels())
        if ax.get_yticklabels()[0].get_text() != '':
            self.set('yticklabels', ax.get_yticklabels())
        self.set('zorder_sum', 4)

    def _init_derivatives(self):
        for n in range(1, settings['derivative']['user_max'] + 1):
            self.set('active_derivative' + str(n), False)
            self.set('derivative_color' + str(n), settings['derivative']['colors'][n - 1])

    def _init_zero_points(self):
        self.set('zero_points_visible', False)
        self.set('zero_points_method', 'Newton' if len(self.get('user_derivatives')) > 0 else 'Secant')
        self.set('zero_points_color', settings['zero_points']['color'])
        self.set('zero_points_iterations', settings['zero_points']['iterations'])

    def _init_analysis(self, op):
        self.set(f'{op}_visible', False)
        self.set(f'{op}_color', settings[op]['color'])

    def plot(self, ax) -> None:
        """
        Pomocou triedy Plotter vykreslí všetky užívateľom zvolené informácie do grafu
        :param ax: objekt matplotlib Axes
        :return:
        """
        ax.clear()
        Plotter(self, ax).plot_all()

    def set(self, parameter_name, parameter_value) -> None:
        """
        Priradí parametru s menom name hodnotu value
        :return:
        """
        self.parameters[parameter_name] = parameter_value

    def get(self, parameter_name):
        """
        Vráti hodnotu parametra, ktorý ma názov parameter_name
        :return:
        """
        return self.parameters.get(parameter_name, None)

    def get_analysis_data(self, key=None, unpack=False, list_values=False) -> np.array:
        """
        Vráti vypočítané údaje - pre ich vykreslenie, resp. vypísanie.
        :param key: uvažovaný parameter (zero_points, inflex_points, ...)
        :param unpack: Ak True, spojí všetky dáta z intervalov Xi do jedného
        :param list_values: Povie funkcii, že uvažované hodnoty sú vo forme zoznamu (napr. intervaly monotónnosti)
        :return:
        """
        if key is None:
            return self.analysis_data
        if unpack and key in self.analysis_data:
            all_intervals = self.analysis_data.get(key)
            if list_values:
                return np.asarray(list(itertools.chain(*all_intervals.values())))
            return np.concatenate(list(all_intervals.values()))
        return self.analysis_data.get(key, np.asarray([]))

    def update_zorder_sum(self) -> None:
        """
        Pripočíta nový vykreslený objekt k celkovému počtu vykreslených objektov v grafe
        :return:
        """
        self.set('zorder_sum', self.get('zorder_sum') + 1)

    def get_zorder_sum(self) -> int:
        """
        Vráti celkový počet vykreslených objektov v grafe
        :return:
        """
        return self.get('zorder_sum')
