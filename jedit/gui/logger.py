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

import json
import os
from datetime import datetime

import ipywidgets as w
import numpy as np
from IPython.display import clear_output

from ..settings import settings


class Logger:

    def __init__(self):
        self.outputs = {'main': w.Output(layout=w.Layout(overflow='auto')),
                        'mini': w.Output(layout=w.Layout(overflow='hidden', height='100%')),
                        'warnings': w.Output(layout=w.Layout(overflow='auto'))}
        self.log_stack = LoggerStack()
        self.warning_stack = LoggerStack()

    def new_message(self, theme, **kwargs):
        return LoggerMessage(theme, kwargs)

    def set_order_oldest(self, value) -> None:
        """
        Vymení poradie výpisu výstupov
        :param value:
        :return:
        """
        self.log_stack.set_order(oldest=value)
        self.warning_stack.set_order(oldest=value)

    def write(self, message, main=False, mini=False, warnings=False, timer=False) -> None:
        """
        :param message: Objekt LoggerMessage
        :param main: vypíše do tabu Výstupy
        :param mini: vypíše do tabu Posledná zmena
        :param warnings: vypíše do tabu Upozornenia
        :param timer: Vypíše správu počas prepočtu funkcie
        :return: None
        """
        if timer:
            with self.outputs['mini']:
                clear_output()
                print(message.text(quick_info=True))
            return
        out = f'[{datetime.now().strftime("%d.%m.%Y %H:%M:%S")}]'
        if main:
            with self.outputs['main']:
                clear_output()
                self.log_stack.push(out + message.text())
                self.log_stack.reveal()
        if mini and settings['editor']['footer_log'] == 'yes':
            with self.outputs['mini']:
                clear_output()
                print(message.text(mini=True))
        if warnings:
            with self.outputs['warnings']:
                self.warning_stack.push(out + message.text())
                self.warning_stack.reveal()

    def to_file(self, analysis_dict=None) -> str:
        """
        Uloží všetky výstupy do textového súboru alebo všetky výpočty do formátu JSON
        :param analysis_dict: Ak je zadaný dataset, uloží ho do formátu JSON
        :return:
        """
        dir_name = 'jedit_out'
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        if analysis_dict is not None:
            file_name = str(datetime.now().strftime(f'{dir_name}/computings-%d-%m-%Y-%H-%M-%S.json'))
            with open(file_name, 'w') as file:
                json.dump(analysis_dict, file, sort_keys=True)
        else:
            file_name = str(datetime.now().strftime(f'{dir_name}/log-%d-%m-%Y-%H-%M-%S.txt'))
            with open(file_name, 'w') as file:
                self.log_stack.reveal(file=file)
        return file_name

    def get_widget(self, t=None) -> w.Output:
        return self.outputs[t]


class LoggerMessage:

    def __init__(self, theme, kwargs):
        self.theme, self.kwargs = theme, kwargs

    def text(self, mini=False, quick_info=False):
        """
        Spracuje správu do čitateľnejšej formy.
        :param mini: Ak True, tak zmenšená verzia pre tab Posledná zmena
        :param quick_info: Ak True, tak jednoslovná správa
        :return: Textový reťazec pripravený na vypísanie.
        """
        if mini:
            return f'{self.theme}: {self.kwargs}'
        if quick_info:
            return f'{self.theme}'
        result = f'\n\tpopis akcie: {self.theme}'
        for arg, val in self.kwargs.items():
            result += '\n\t'
            if type(val) == list or type(val) == np.ndarray:
                if len(val) > 0:
                    result += f'{arg}: [\n\t   '
                    result += ',\n\t   '.join(map(str, val)) + '\n\t]'
                else:
                    result += f'{arg}: []'
            else:
                result += f'{arg}: {val}'
        return result


class LoggerStack:
    """
    Ukladá všetky výpisy a manažuje spôsob ich výpisov.
    """

    def __init__(self, oldest=False):
        self.oldest = oldest
        self.data = []

    def set_order(self, oldest):
        self.oldest = oldest

    def push(self, item):
        self.data.append(item)

    def reveal(self, file=None):
        """
        Vypíše všetky výpisy v zadanom poradí, poprípade ich uloží do súboru file.
        :param file: Ak zadané, vypíše do súboru.
        :return:
        """
        if self.oldest:
            for value in self.data:
                print(value) if file is None else print(value, file=file)
        else:
            for i in range(len(self.data) - 1, -1, -1):
                print(self.data[i]) if file is None else print(self.data[i], file=file)

    def is_empty(self):
        return len(self.data) == 0
