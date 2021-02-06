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
from traitlets import directional_link

"""
Triedy pre reprezentáciu ovládacích prvkov.
"""


class HBox:

    def __init__(self, description, disabled, color, link=False, tooltip=None):
        self.description = description
        self.disabled = disabled
        self.color = color
        self.link = link
        self.tooltip = tooltip

    def get(self):
        toggle = w.ToggleButton(
            value=False,
            description=self.description,
            disabled=self.disabled,
            button_style='',
            tooltip=self.tooltip if self.tooltip is not None else self.description,
            layout=w.Layout(width='90%')
        )
        cpicker = w.ColorPicker(
            concise=True,
            description='',
            value=self.color,
            disabled=False,
            layout=w.Layout(width='28px')
        )
        if self.link:
            directional_link((toggle, 'value'), (cpicker, 'disabled'), lambda case: not case)
        return w.HBox(children=[toggle, cpicker], layout=w.Layout(overflow='hidden'))


class Toggle:

    def __init__(self, description, disabled, tooltip=None):
        self.description = description
        self.disabled = disabled
        self.tooltip = tooltip

    def get(self):
        toggle = w.ToggleButton(
            value=False,
            description=self.description,
            disabled=self.disabled,
            button_style='',
            tooltip=self.tooltip if self.tooltip is not None else self.description,
            layout=w.Layout(width='100%')
        )
        return w.HBox(children=[toggle], layout=w.Layout(overflow='hidden'))


class Dropdown:

    def __init__(self, description, disabled, values, default_value, tooltip=None):
        self.description = description
        self.disabled = disabled
        self.values = values
        self.default_value = default_value
        self.tooltip = tooltip

    def get(self):
        toggle = w.ToggleButton(
            value=False,
            description=self.description,
            disabled=True,
            button_style='',
            tooltip=self.tooltip if self.tooltip is not None else self.description,
            layout=w.Layout(width='100%')
        )
        dropdown = w.Dropdown(
            options=self.values,
            value=self.default_value,
            description='',
            disabled=self.disabled,
            layout=w.Layout(width='70%', overflow='hidden')
        )
        return w.HBox(children=[toggle, dropdown], layout=w.Layout(overflow='hidden'))


class IntText:

    def __init__(self, description, disabled, minval, maxval, step, default_value, tooltip=None):
        self.description = description
        self.disabled = disabled
        self.min = minval
        self.max = maxval
        self.step = step
        self.default_value = default_value
        self.tooltip = tooltip

    def get(self):
        toggle = w.ToggleButton(
            value=False,
            description=self.description,
            disabled=True,
            button_style='',
            tooltip=self.tooltip if self.tooltip is not None else self.description,
            layout=w.Layout(width='100%')
        )
        textfield = w.BoundedIntText(
            value=self.default_value,
            min=self.min,
            max=self.max,
            step=self.step,
            description='',
            disabled=self.disabled,
            layout=w.Layout(width='40%', overflow='hidden')
        )
        return w.HBox(children=[toggle, textfield], layout=w.Layout(overflow='hidden'))


class Button:

    def __init__(self, description, disabled, tooltip=None):
        self.description = description
        self.disabled = disabled
        self.tooltip = tooltip

    def get(self):
        button = w.Button(
            value=False,
            description=self.description,
            disabled=self.disabled,
            button_style='',
            tooltip=self.tooltip if self.tooltip is not None else self.description,
            layout=w.Layout(width='100%')
        )
        return w.HBox(children=[button], layout=w.Layout(overflow='hidden'))
