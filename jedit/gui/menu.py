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

from collections import defaultdict

import ipywidgets as w

from .elements import HBox, Dropdown, IntText, Toggle, Button
from ..settings import settings


class MainMenu:
    """
    Trieda MainMenu združuje všetky užívateľské ovládacie prvky, rozdelené do dvoch tabov, Analýza a Možnosti.
    """

    def __init__(self):
        self.elements = defaultdict(dict)
        self._init_menu()

    def _init_menu(self):
        """
        Vytvorí a vráti mriežkové štruktúry pre uloženie ovládacích prvkov, ktoré sú prístupné v objekte Tab.
        :return: Hlavné menu v podobe Tab objektu
        """
        n_elements_max = 13

        a_grid = w.GridspecLayout(n_elements_max, 1)

        a_grid[0, 0] = self.elements['hbox']['zero_points'] = HBox(description='Nulové body',
                                                                   disabled=False,
                                                                   color=settings['zero_points']['color'],
                                                                   link=True).get()

        a_grid[1, 0] = self.elements['hbox']['extremes'] = HBox(description='Ostré lokálne extrémy',
                                                                disabled=False,
                                                                color=settings['extremes']['color'],
                                                                link=True).get()

        a_grid[2, 0] = self.elements['hbox']['inflex_points'] = HBox(description='Inflexné body',
                                                                     disabled=False,
                                                                     color=settings['inflex_points']['color'],
                                                                     link=True).get()

        a_grid[4, 0] = self.elements['hbox']['increasing'] = HBox(description='Rastúca',
                                                                  disabled=False,
                                                                  color=settings['increasing']['color'],
                                                                  link=True).get()

        a_grid[5, 0] = self.elements['hbox']['decreasing'] = HBox(description='Klesajúca',
                                                                  disabled=False,
                                                                  color=settings['decreasing']['color'],
                                                                  link=True).get()

        a_grid[6, 0] = self.elements['hbox']['concave_up'] = HBox(description='Rýdzo konvexná',
                                                                  disabled=False,
                                                                  color=settings['concave_up']['color'],
                                                                  link=True).get()

        a_grid[7, 0] = self.elements['hbox']['concave_down'] = HBox(description='Rýdzo konkávna',
                                                                    disabled=False,
                                                                    color=settings['concave_down']['color'],
                                                                    link=True).get()

        a_grid[9, 0] = self.elements['dropdown']['refinement_x'] = Dropdown(description='Zjemnenie osi x',
                                                                            disabled=False,
                                                                            values=list(map(lambda
                                                                                                n: n + 'x' if n != 'pôvodné' else n,
                                                                                            settings['refinement_x'][
                                                                                                'values'])),
                                                                            default_value='pôvodné').get()

        a_grid[11, 0] = self.elements['text']['rounding'] = IntText(description='Presnosť výsledkov',
                                                                    disabled=False,
                                                                    minval=settings['editor']['round']['from'],
                                                                    maxval=settings['editor']['round']['to'],
                                                                    step=1,
                                                                    default_value=settings['editor']['round'][
                                                                        'default'],
                                                                    tooltip='Presnosť výsledkov na počet platných cifier').get()

        a_grid[12, 0] = self.elements['text']['iterations'] = IntText(description='Iterácie Newtonovej metódy',
                                                                      disabled=False,
                                                                      minval=1,
                                                                      maxval=1000,
                                                                      step=1,
                                                                      default_value=settings['zero_points'][
                                                                          'iterations']).get()

        f_grid = w.GridspecLayout(n_elements_max, 1)

        f_grid[0, 0] = self.elements['hbox']['main_function'] = HBox(description='Funkcia',
                                                                     disabled=True,
                                                                     color=settings['main_function']['color']).get()

        f_grid[2, 0] = self.elements['hbox']['derivative1'] = HBox(description='1. derivácia',
                                                                   disabled=False,
                                                                   color=settings['derivative']['colors'][0]).get()

        f_grid[3, 0] = self.elements['hbox']['derivative2'] = HBox(description='2. derivácia',
                                                                   disabled=False,
                                                                   color=settings['derivative']['colors'][1]).get()

        f_grid[4, 0] = self.elements['hbox']['derivative3'] = HBox(description='3. derivácia',
                                                                   disabled=False,
                                                                   color=settings['derivative']['colors'][2]).get()

        f_grid[6, 0] = self.elements['toggle']['grid'] = Toggle(description='Mriežka',
                                                                disabled=False).get()

        f_grid[8, 0] = self.elements['dropdown']['logger_order'] = Dropdown(description='Poradie výstupov',
                                                                            disabled=False,
                                                                            values=['najnovšie',
                                                                                    'najstaršie'],
                                                                            default_value='najnovšie').get()

        f_grid[10, 0] = self.elements['button']['logger_save'] = Button(description='Uložiť textové výstupy (txt)',
                                                                        disabled=False).get()

        f_grid[11, 0] = self.elements['button']['json_save'] = Button(description='Uložiť vypočítané hodnoty (JSON)',
                                                                      disabled=False).get()

        tab_nest = w.Tab(layout=w.Layout(overflow='hidden'))
        tab_nest.children = [a_grid, f_grid]
        tab_nest.set_title(0, 'Analýza')
        tab_nest.set_title(1, 'Možnosti')
        self.main_menu = tab_nest

    def get_elements(self) -> defaultdict:
        """
        :return: Slovník všetkých ovládacích prvkov menu pre rýchly prístup.
        """
        return self.elements

    def get_widget(self) -> w.Tab:
        """
        :return: Hlavné menu v podobe Tab objektu
        """
        return self.main_menu
