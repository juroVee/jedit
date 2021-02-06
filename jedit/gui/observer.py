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

from copy import deepcopy

from ..settings import settings


class Observer:
    """
    Trieda, ktorá spracuje užívateľské akcie a obsahuje metódy, ktoré po nich vykonávajú príslušné príkazy.
    """

    def __init__(self, board):
        self.function_manager = board.get_object('function_manager')
        self.menu = board.get_object('main_menu')
        self.logger = board.get_object('logger')
        self.logger.write(self.logger.new_message('editor spustený'), main=True)
        self.rules = {'vypnuté': False, 'zapnuté': True}
        self.svk = {True: 'áno', False: 'nie'}

    def _add_zero_points_info(self, function, refinement_support=False) -> None:
        """
        Pomocná metóda, ktorá pozbiera všetky informácie o nulových bodoch a pošle ich na výpis do objektu Logger.
        :param function: Objekt funkcie (Function)
        :param refinement_support: Ak True, výpis informácií sa udeje len na pozadí po zmene zjemnenia/presnosti,
        nie ako hlavná akcia
        :return: 
        """
        zero_points = function.get_analysis_data(key='zero_points', unpack=True)
        visible = function.get('zero_points_visible')
        method = function.get('zero_points_method')
        maxiter = function.get('zero_points_iterations')
        derivatives_provided = len(function.get('user_derivatives'))
        if not visible:
            if not refinement_support:
                self.logger.write(self.logger.new_message('nulové body',
                                                          derivácie=derivatives_provided,
                                                          metóda=method,
                                                          maxiter=maxiter), mini=True, main=True)
            return
        if not refinement_support:
            self.logger.write(self.logger.new_message('nulové body',
                                                      derivácie=derivatives_provided,
                                                      metóda=method,
                                                      maxiter=maxiter,
                                                      počet=len(zero_points)), mini=True)
        self.logger.write(self.logger.new_message('nulové body',
                                                  derivácie=derivatives_provided,
                                                  metóda=method,
                                                  maxiter=maxiter,
                                                  počet=len(zero_points),
                                                  v_bodoch=zero_points), main=True)

    def _add_extremes_info(self, function, refinement_support=False) -> None:
        """
        Pomocná metóda, ktorá pozbiera všetky informácie o ostrých lokálnych extrémoch a pošle ich na výpis
        do objektu Logger.
        :param function: Objekt funkcie (Function)
        :param refinement_support: Ak True, výpis informácií sa udeje len na pozadí po zmene zjemnenia/presnosti,
        nie ako hlavná akcia
        :return: 
        """
        visible = function.get('extremes_visible')
        if not visible:
            if not refinement_support:
                self.logger.write(self.logger.new_message('extrémy', viditeľné=self.svk[visible]), mini=True, main=True)
            return
        extremes = function.get_analysis_data(key='extremes', unpack=True)
        maxima = function.get_analysis_data(key='maxima', unpack=True)
        minima = function.get_analysis_data(key='minima', unpack=True)
        if not refinement_support:
            self.logger.write(self.logger.new_message('extrémy', viditeľné=self.svk[visible],
                                                      ostré_lokálne_extrémy=len(extremes)), mini=True)
        self.logger.write(self.logger.new_message('extrémy', viditeľné=self.svk[visible],
                                                  ostré_lokálne_extrémy_v_bodoch=extremes,
                                                  ostré_lokálne_minimá_v_bodoch=minima,
                                                  ostré_lokálne_maximá_v_bodoch=maxima), main=True)

    def _add_inflex_points_info(self, function, refinement_support=False) -> None:
        """
        Pomocná metóda, ktorá pozbiera všetky informácie o inflexných bodoch a pošle ich na výpis do objektu Logger.
        :param function: Objekt funkcie (Function)
        :param refinement_support: Ak True, výpis informácií sa udeje len na pozadí po zmene zjemnenia/presnosti,
        nie ako hlavná akcia
        :return: 
        """
        visible = function.get('inflex_points_visible')
        if not visible:
            if not refinement_support:
                self.logger.write(self.logger.new_message('inflexné body', viditeľné=self.svk[visible]), mini=True,
                                  main=True)
            return
        inflex_points = function.get_analysis_data(key='inflex_points', unpack=True)
        if not refinement_support:
            self.logger.write(
                self.logger.new_message('inflexné body', viditeľné=self.svk[visible], nájdené=len(inflex_points)),
                mini=True)
        self.logger.write(self.logger.new_message('inflexné body', viditeľné=self.svk[visible], v_bodoch=inflex_points),
                          main=True)

    def _add_analysis_info(self, function, op='increasing', refinement_support=False) -> None:
        """
        Pomocná metóda, ktorá pozbiera všetky informácie o intervaloch monotónnosti/konvexnosti/konkávnosti a pošle
        ich na výpis do objektu Logger.
        :param function: Objekt funkcie (Function)
        :param refinement_support: Ak True, výpis informácií sa udeje len na pozadí po zmene zjemnenia/presnosti,
        nie ako hlavná akcia
        :return: 
        """
        visible = function.get(f'{op}_visible')
        desc = {'increasing': 'rastúca',
                'decreasing': 'klesajúca',
                'concave_up': 'rýdzo konvexná',
                'concave_down': 'rýdzo konkávna'}
        if not visible:
            if not refinement_support:
                self.logger.write(self.logger.new_message(desc[op], viditeľné=self.svk[visible]), mini=True, main=True)
            return
        outer_points = [(interval[0], interval[-1]) for interval in
                        function.get_analysis_data(key=op, unpack=True, list_values=True)]
        if not refinement_support:
            self.logger.write(
                self.logger.new_message(desc[op], viditeľné=self.svk[visible], nájdené_intervaly_x=len(outer_points)),
                mini=True)
        self.logger.write(self.logger.new_message(desc[op], viditeľné=self.svk[visible], intervaly_x=outer_points),
                          main=True)

    def _changed_grid(self, event) -> None:
        """
        Ovládacia metóda, ktorá nastaví zobrazenie mriežky.
        :param event: Dátová štruktúra, ktorá ukladá užívateľskú voľbu.
        :return:
        """
        visible = event['new']
        function = self.function_manager.get_function()
        function.set('grid', visible)
        self.function_manager.update_plot()
        self.logger.write(self.logger.new_message('mriežka', viditeľné=self.svk[visible]), main=True, mini=True)

    def _changed_logger_order(self, event) -> None:
        """
        Ovládacia metóda, ktorá nastaví poradie výpisov.
        :param event: Dátová štruktúra, ktorá ukladá užívateľskú voľbu.
        :return:
        """
        self.logger.set_order_oldest(True if event['new'] == 'najstaršie' else False)
        self.logger.write(self.logger.new_message('výstupy', poradie=event['new']), main=True, mini=True)

    def _changed_logger_save(self, event) -> None:
        """
        Ovládacia metóda, ktorá uloží výpisy do súboru.
        :param event: Dátová štruktúra, ktorá ukladá užívateľskú voľbu.
        :return:
        """
        self.logger.write(self.logger.new_message('výstupy', stav='uložené', súbor=self.logger.to_file()), mini=True,
                          main=True)

    def _changed_json_save(self, event) -> None:
        """
        Ovládacia metóda, ktorá uloží výpočty do formátu JSON.
        :param event: Dátová štruktúra, ktorá ukladá užívateľskú voľbu.
        :return:
        """
        function = self.function_manager.get_function()
        data = deepcopy(function.get_analysis_data())
        for name, intervals in data.items():
            for Xi, interval in intervals.items():
                if type(interval) == list:
                    data[name][Xi] = list(map(list, interval))
                else:
                    data[name][Xi] = list(interval)
        self.logger.write(
            self.logger.new_message('vypočítané_hodnoty', stav='uložené', súbor=self.logger.to_file(data)), mini=True,
            main=True)

    def _changed_derivative1(self, event) -> None:
        """
        Ovládacia metóda, ktorá nastaví zobrazenie 1. derivácie.
        :param event: Dátová štruktúra, ktorá ukladá užívateľskú voľbu.
        :return:
        """
        visible = event['new']
        function = self.function_manager.get_function()
        function.set('active_derivative1', visible)
        self.function_manager.update_plot()
        self.logger.write(self.logger.new_message('prvá derivácia', viditeľné=self.svk[visible]), main=True, mini=True)

    def _changed_derivative2(self, event) -> None:
        """
        Ovládacia metóda, ktorá nastaví zobrazenie 2. derivácie.
        :param event: Dátová štruktúra, ktorá ukladá užívateľskú voľbu.
        :return:
        """
        visible = event['new']
        function = self.function_manager.get_function()
        function.set('active_derivative2', visible)
        self.function_manager.update_plot()
        self.logger.write(self.logger.new_message('druhá derivácia', viditeľné=self.svk[visible]), main=True, mini=True)

    def _changed_derivative3(self, event) -> None:
        """
        Ovládacia metóda, ktorá nastaví zobrazenie 3. derivácie.
        :param event: Dátová štruktúra, ktorá ukladá užívateľskú voľbu.
        :return:
        """
        visible = event['new']
        function = self.function_manager.get_function()
        function.set('active_derivative3', visible)
        self.function_manager.update_plot()
        self.logger.write(self.logger.new_message('tretia derivácia', viditeľné=self.svk[visible]), main=True,
                          mini=True)

    def _changed_color_main_function(self, event) -> None:
        """
        Ovládacia metóda, ktorá mení farbu vykreslenej funkcie, a to podľa užívateľových preferencií.
        :param event: Dátová štruktúra, ktorá ukladá užívateľskú voľbu.
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_function()
        function.set('main_function_color', choice)
        self.function_manager.update_plot()
        self.logger.write(self.logger.new_message('hlavná funkcia', farba=choice), main=True, mini=True)

    def _changed_color_derivative1(self, event) -> None:
        """
        Ovládacia metóda, ktorá mení farbu vykreslenej prvej derivácie, a to podľa užívateľových preferencií.
        :param event: Dátová štruktúra, ktorá ukladá užívateľskú voľbu.
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_function()
        function.set('derivative_color1', choice)
        self.function_manager.update_plot()
        self.logger.write(self.logger.new_message('prvá derivácia', farba=choice), main=True, mini=True)

    def _changed_color_derivative2(self, event) -> None:
        """
        Ovládacia metóda, ktorá mení farbu vykreslenej druhej derivácie, a to podľa užívateľových preferencií.
        :param event: Dátová štruktúra, ktorá ukladá užívateľskú voľbu.
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_function()
        function.set('derivative_color2', choice)
        self.function_manager.update_plot()
        self.logger.write(self.logger.new_message('druhá derivácia', farba=choice), main=True, mini=True)

    def _changed_color_derivative3(self, event) -> None:
        """
        Ovládacia metóda, ktorá mení farbu vykreslenej tretej derivácie, a to podľa užívateľových preferencií.
        :param event: Dátová štruktúra, ktorá ukladá užívateľskú voľbu.
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_function()
        function.set('derivative_color3', choice)
        self.function_manager.update_plot()
        self.logger.write(self.logger.new_message('tretia derivácia', farba=choice), main=True, mini=True)

    def _changed_refinement_x(self, event) -> None:
        """
        Ovládacia metóda, ktorá nastaví zjemnenie intervalov X.
        :param event: Dátová štruktúra, ktorá ukladá užívateľskú voľbu.
        :return:
        """
        options = {value + 'x': int(value) for value in settings['refinement_x']['values'] if value != 'pôvodné'}
        options['pôvodné'] = 1
        choice = options[event['new']]
        function = self.function_manager.get_function()
        function.set('refinement', choice)
        self.logger.write(self.logger.new_message('Prebieha prepočítavanie funkcie...'), timer=True)
        self.function_manager.update_plot(main_function=True, main_derivatives=True, zero_points=True, extremes=True,
                                          inflex_points=True, monotonic=True, concave=True)
        n_x_values = sum(map(len, function.get("x_values")))
        self.logger.write(
            self.logger.new_message('zjemnenie x-ovej osi', zjemnenie=event['new'], počet_intervalov=n_x_values - 1,
                                    počet_hodnôt=n_x_values), main=True, mini=True)
        self._add_zero_points_info(function, refinement_support=True)
        self._add_extremes_info(function, refinement_support=True)
        self._add_inflex_points_info(function, refinement_support=True)
        for op in 'increasing', 'decreasing', 'concave_up', 'concave_down':
            self._add_analysis_info(function, op=op, refinement_support=True)

    def _changed_zero_points(self, event) -> None:
        """
        Ovládacia metóda, ktorá nastaví zobrazenie nulových bodov.
        :param event: Dátová štruktúra, ktorá ukladá užívateľskú voľbu.
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_function()
        function.set('zero_points_visible', choice)
        if choice:
            function.set('zero_points_zorder', function.get_zorder_sum() + 1)
            function.update_zorder_sum()
        self.function_manager.update_plot()
        self._add_zero_points_info(function)

    def _changed_color_zero_points(self, event) -> None:
        """
        Ovládacia metóda, ktorá mení farbu nulových bodov, a to podľa užívateľových preferencií.
        :param event: Dátová štruktúra, ktorá ukladá užívateľskú voľbu.
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_function()
        function.set('zero_points_color', choice)
        self.function_manager.update_plot()
        self.logger.write(self.logger.new_message('nulové body', farba=choice), main=True, mini=True)

    def _changed_iterations(self, event) -> None:
        """
        Ovládacia metóda, ktorá nastaví počet iterácií Newtonovej metódy.
        :param event: Dátová štruktúra, ktorá ukladá užívateľskú voľbu.
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_function()
        function.set('zero_points_iterations', choice)
        self.function_manager.update_plot(zero_points=True)
        self._add_zero_points_info(function)

    def _changed_rounding(self, event) -> None:
        function = self.function_manager.get_function()
        function.set('rounding', event['new'])
        self.logger.write(self.logger.new_message('Prebieha prepočítavanie funkcie...'), timer=True)
        self.function_manager.update_plot(zero_points=True, extremes=True, inflex_points=True, monotonic=True,
                                          concave=True)
        self.logger.write(self.logger.new_message('presnosť výsledkov', platné_číslice=event['new']), main=True,
                          mini=True)
        self._add_zero_points_info(function, refinement_support=True)
        self._add_extremes_info(function, refinement_support=True)
        self._add_inflex_points_info(function, refinement_support=True)
        for op in 'increasing', 'decreasing', 'concave_up', 'concave_down':
            self._add_analysis_info(function, op=op, refinement_support=True)

    def _changed_extremes(self, event) -> None:
        """
        Ovládacia metóda, ktorá nastaví zobrazenie ostrých lokálnych extrémov.
        :param event: Dátová štruktúra, ktorá ukladá užívateľskú voľbu.
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_function()
        if choice:
            function.set('extremes_zorder', function.get_zorder_sum() + 1)
            function.update_zorder_sum()
        function.set('extremes_visible', choice)
        self.function_manager.update_plot()
        self._add_extremes_info(function)

    def _changed_color_extremes(self, event) -> None:
        """
        Ovládacia metóda, ktorá mení farbu ostrých kolkálnych extrémov, a to podľa užívateľových preferencií.
        :param event: Dátová štruktúra, ktorá ukladá užívateľskú voľbu.
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_function()
        function.set('extremes_color', choice)
        self.function_manager.update_plot()
        self.logger.write(self.logger.new_message('extrémy', farba=choice), main=True, mini=True)

    def _changed_inflex_points(self, event) -> None:
        """
        Ovládacia metóda, ktorá nastaví zobrazenie inflexných bodov.
        :param event: Dátová štruktúra, ktorá ukladá užívateľskú voľbu.
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_function()
        if choice:
            function.set('inflex_points_zorder', function.get_zorder_sum() + 1)
            function.update_zorder_sum()
        function.set('inflex_points_visible', choice)
        self.function_manager.update_plot()
        self._add_inflex_points_info(function)

    def _changed_color_inflex_points(self, event) -> None:
        """
        Ovládacia metóda, ktorá mení farbu inflexných bodov, a to podľa užívateľových preferencií.
        :param event: Dátová štruktúra, ktorá ukladá užívateľskú voľbu.
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_function()
        function.set('inflex_points_color', choice)
        self.function_manager.update_plot()
        self.logger.write(self.logger.new_message('inflexné body', farba=choice), main=True, mini=True)

    def _changed_increasing(self, event) -> None:
        """
        Ovládacia metóda, ktorá nastaví zobrazenie intervalov, kde je funkcia rastúca.
        :param event: Dátová štruktúra, ktorá ukladá užívateľskú voľbu.
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_function()
        if choice:
            function.set('increasing_zorder', function.get_zorder_sum() + 1)
            function.update_zorder_sum()
        function.set('increasing_visible', choice)
        self.function_manager.update_plot()
        self._add_analysis_info(function, op='increasing')

    def _changed_color_increasing(self, event) -> None:
        """
        Ovládacia metóda, ktorá mení farbu intervalu, kde je funkcia rastúca, a to podľa užívateľových preferencií.
        :param event: Dátová štruktúra, ktorá ukladá užívateľskú voľbu.
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_function()
        function.set('increasing_color', choice)
        self.function_manager.update_plot()
        self.logger.write(self.logger.new_message('rastúca', farba=choice), main=True, mini=True)

    def _changed_decreasing(self, event) -> None:
        """
        Ovládacia metóda, ktorá nastaví zobrazenie intervalov, kde je funkcia klesajúca.
        :param event: Dátová štruktúra, ktorá ukladá užívateľskú voľbu.
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_function()
        if choice:
            function.set('decreasing_zorder', function.get_zorder_sum() + 1)
            function.update_zorder_sum()
        function.set('decreasing_visible', choice)
        self.function_manager.update_plot()
        self._add_analysis_info(function, op='decreasing')

    def _changed_color_decreasing(self, event) -> None:
        """
        Ovládacia metóda, ktorá mení farbu intervalu, kde je funkcia klesajúca, a to podľa užívateľových preferencií.
        :param event: Dátová štruktúra, ktorá ukladá užívateľskú voľbu.
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_function()
        function.set('decreasing_color', choice)
        self.function_manager.update_plot()
        self.logger.write(self.logger.new_message('klesajúca', farba=choice), main=True, mini=True)

    def _changed_concave_up(self, event) -> None:
        """
        Ovládacia metóda, ktorá nastaví zobrazenie intervalov, kde je funkcia rýdzo konvexná.
        :param event: Dátová štruktúra, ktorá ukladá užívateľskú voľbu.
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_function()
        if choice:
            function.set('concave_up_zorder', function.get_zorder_sum() + 1)
            function.update_zorder_sum()
        function.set('concave_up_visible', choice)
        self.function_manager.update_plot()
        self._add_analysis_info(function, op='concave_up')

    def _changed_color_concave_up(self, event) -> None:
        """
        Ovládacia metóda, ktorá mení farbu intervalu konvexnosti podľa užívateľových preferencií.
        :param event: Dátová štruktúra, ktorá ukladá užívateľskú voľbu.
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_function()
        function.set('concave_up_color', choice)
        self.function_manager.update_plot()
        self.logger.write(self.logger.new_message('rýdzo konvexná', farba=choice), main=True, mini=True)

    def _changed_concave_down(self, event) -> None:
        """
        Ovládacia metóda, ktorá nastaví zobrazenie intervalov, kde je funkcia rýdzo konkávna.
        :param event: Dátová štruktúra, ktorá ukladá užívateľskú voľbu.
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_function()
        if choice:
            function.set('concave_down_zorder', function.get_zorder_sum() + 1)
            function.update_zorder_sum()
        function.set('concave_down_visible', choice)
        self.function_manager.update_plot()
        self._add_analysis_info(function, op='concave_down')

    def _changed_color_concave_down(self, event) -> None:
        """
        Ovládacia metóda, ktorá mení farbu intervalu konkávnosti podľa užívateľových preferencií.
        :param event: Dátová štruktúra, ktorá ukladá užívateľskú voľbu.
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_function()
        function.set('concave_down_color', choice)
        self.function_manager.update_plot()
        self.logger.write(self.logger.new_message('rýdzo konkávna', farba=choice), main=True, mini=True)

    def start(self) -> None:
        """
        Začne sledovať všetky ovládacie prvky a čaká na užívateľské akcie.
        :return:
        """
        gui_elements = self.menu.get_elements()

        for element in gui_elements['hbox']:
            dropdown, color_picker = gui_elements['hbox'][element].children
            if hasattr(self, f'_changed_{element}'):
                dropdown.observe(getattr(self, f'_changed_{element}'), 'value')
            if hasattr(self, f'_changed_color_{element}'):
                color_picker.observe(getattr(self, f'_changed_color_{element}'), 'value')

        for element in gui_elements['toggle']:
            button = gui_elements['toggle'][element].children[0]
            if hasattr(self, f'_changed_{element}'):
                button.observe(getattr(self, f'_changed_{element}'), 'value')

        for element in gui_elements['dropdown']:
            _, dropdown = gui_elements['dropdown'][element].children
            if hasattr(self, f'_changed_{element}'):
                dropdown.observe(getattr(self, f'_changed_{element}'), 'value')

        for element in gui_elements['text']:
            _, text = gui_elements['text'][element].children
            if hasattr(self, f'_changed_{element}'):
                text.observe(getattr(self, f'_changed_{element}'), 'value')

        for element in gui_elements['button']:
            button = gui_elements['button'][element].children[0]
            if hasattr(self, f'_changed_{element}'):
                button.on_click(getattr(self, f'_changed_{element}'))
