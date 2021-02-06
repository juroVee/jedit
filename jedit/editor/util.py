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

from IPython.display import display, HTML


def hide_interactive_toolbars():
    """
    Skryje na úrovni CSS interaktívne prvky v notebooku, ktoré narúšajú celkový vizuál aplikácie a nie sú podstatné.
    :return:
    """
    html = '''
            <style>
            .output_wrapper button.btn.btn-default,
            .output_wrapper .ui-dialog-titlebar,
            .output_wrapper .mpl-message,
            .output_wrapper .ui-icon {
              display: none!important;
            }
            </style>
           '''
    display(HTML(html))


def check_parameters(params) -> tuple:
    """
    Prekontroluje užívateľský vstup, zadané parametre, ich formát a hodnoty.
    :param params: užívateľské prametre
    :param logger: referencia na objektu Logger, pre prípadný výpis upozornení
    :return:
    """
    allowed_params = {'figure', 'axes', 'function', 'intervals', 'primes'}
    required_params = {'figure', 'axes', 'function', 'intervals'}
    error_message = None
    for param in params.keys():
        if param not in allowed_params:
            error_message = f'Neznámy parameter {param}. Povolené parametre sú {allowed_params}.'
            return error_message, params
    if any(param not in params for param in required_params):
        error_message = f'Parametre {required_params} sú nevyhnutné pre analýzu funkcie.'
        return error_message, params
    else:
        others = {k: params[k] for k in set(params) - {'figure', 'axes', 'function'}}
        for param, value in others.items():
            if type(value) != list:
                error_message = f'Hodnota parametra "{param}" musí byť typu list, napr. {param}=[a, b, ...].'
                return error_message, params
    return error_message, params
