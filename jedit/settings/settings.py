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

import yaml


class Settings:
    """
    Pomocná trieda pre spracovanie konfiguračného súboru yml a vytvorenie globálnej inštancie settings,
    ktorá je prístupná všetkým modulom.
    """

    def __init__(self):
        with open('jedit/settings/settings.yml', 'r') as yml:
            self.data = yaml.load(yml, Loader=yaml.FullLoader)

    def get_data(self):
        return self.data


# create instance alongside editor
settings = Settings().get_data()
