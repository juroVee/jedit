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

from queue import Queue


class WarningsManager:
    """
    Združuje všetky varovania, ktoré vznikli pri výpočtoch.
    """

    def __init__(self, logger):
        self.logger = logger
        self.data = Queue()

    def add(self, warnings_list, category=None):
        messages = set()
        for warning in warnings_list:
            if str(warning.message) not in messages:
                self.data.put((category, warning))
                messages.add(str(warning.message))

    def get(self):
        return self.data

    def print(self) -> None:
        """
        Metóda pošle všetky varovania objektu Logger, ktorý ich vypíše do tabu Upozornenia.
        """
        while not self.data.empty():
            category, warning = self.data.get()
            message = self.logger.new_message('upozornenie',
                                              správa=str(warning.message),
                                              kategória=f'{warning.category} at {category}',
                                              súbor=str(warning.filename))
            self.logger.write(message, warnings=True)
