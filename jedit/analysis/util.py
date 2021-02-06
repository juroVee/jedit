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

from fractions import Fraction

import numpy as np
from scipy.misc import derivative
from scipy.signal import argrelextrema

from ..settings import settings


def zero_crossings(array) -> list:
    """
    Nájde medzi hodnotami indexy hodnôt, kde sa mení znamienko na opačné.
    Niekedy sa toto znamienko môže meniť v krajných bodoch intervalu, čo ignorujeme.
    :param array: Vstupné pole hodnôt, v ktorom hľadáme hodnoty, kde sa mení znamienko na opačné.
    :return: Zoznam dvojíc indexov hodnôt v poli, medzi ktorými sa mení znamienko na opačné
    """
    result = np.where((np.diff(np.sign(array)) != abs(0)) * 1)[0]
    if 0 in result:
        result = result[1:]
    if len(array) - 1 in result + 1:
        result = result[:-1]
    return list(zip(result, result + 1))


def approximate_zeros(array):
    """
    Pri hľadaní nulových hodnôt derivácií sa často stretávame s problémom, že tieto hodnoty
    sú nule len blízke, pričom samotné nuly sa v našich vypočítaných hodnotách ani nenachádzajú.
    To však nebráni správnemu odhadu "nuly", t.j. nájdeniu hodnôt najbližších nule.
    Najjednoduchší spôsob výberu hodnôt najbližsích nule, je nájsť medzi hodnotami indexy hodnôt,
    kde sa mení znamienko na opačné (zero_crossings), resp. kde sa hodnoty podľa nejakej presnosti
    dotýkajú nuly.
    :param array: Vstupné pole hodnôt, v ktorom hľadáme hodnoty najbližšie nule.
    :return: Zoznam dvojíc indexov hodnôt v poli, medzi ktorými sa mení znamienko na opačné
    """
    atol = float(settings['editor']['zero_tolerance'])
    touching_zero_pos = argrelextrema(array, np.less)[0]
    touching_zero_neg = argrelextrema(array, np.greater)[0]
    if np.any(np.isclose(array[touching_zero_pos], 0, atol=atol)):
        array[touching_zero_pos] = 0.
    if np.any(np.isclose(array[touching_zero_neg], 0, atol=atol)):
        array[touching_zero_neg] = 0.
    crossings = [pair[np.abs(array[np.array(pair)]).argmin()] for pair in zero_crossings(array)]
    array[crossings] = 0.
    return array


def get_derivative(func, X, n):
    """
    Vypočíta hodnoty derivácií funkcie func stupňa n pre celý interval X
    :param func: definícia funkcie
    :param X: interval
    :param n: stupeň derivácie
    :return: pole derivácií funkcie func stupňa n, prislúchajúcich intervalu X
    """
    delta_x, order = np.diff(X)[0], n + 3 if n % 2 == 0 else n + 2
    return derivative(func, X, n=n, dx=delta_x / 10, order=order)


def round_to_n_significant(array, n):
    """
    Prepočíta hodnoty v poli array na n platných cifier.
    :param array: vstupné pole hodnôt
    :param n: počet platných cifier
    :return: prepočítané pole hodnôt
    """
    x_positive = np.where(np.isfinite(array) & (array != 0), np.abs(array), 10 ** (array - 1))
    mags = 10 ** (n - 1 - np.floor(np.log10(x_positive)))
    return np.round(array * mags) / mags


def prepare(array, n):
    """
    Pripraví výsledné hodnoty, ktoré sa pošlú na výstup (textový/grafický).
    Pythonovské pole hodnôt zmení na numpy pole, zaokrúhli jeho hodnoty, odstráni duplikáty a zoradí hodnoty vzostupne.
    :param array: vstupné pole hodnôt (polí hodnôt)
    :param n: počet platných číslic
    :return:
    """
    return np.sort(np.unique(round_to_n_significant(array, n)))


def init_subplot(ax):
    """
    Author: J. Komara

    Hides the top and right spines, only shows ticks on the bottom and left spines
    """
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data', 0))
    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position(('data', 0))


def smart_ticklabel(n, unit, d):
    """
    Author: J. Komara
    Returns normalized fraction n/d of the unit in latex represenation.
    Example: smart_ticklabel(3, r"\pi", 2) == "$\\\\dfrac{3\\\\pi}{2}$"
    """

    def smart_sign(n):
        if n < 0:
            return "-"
        else:
            return ""

    def smart_nat(n):
        if n == 1:
            return ""
        else:
            return str(n)

    n1, d1 = Fraction(n, d).numerator, Fraction(n, d).denominator
    if n1 == 0:
        return "$0$"
    elif d1 == 1:
        return "$" + smart_sign(n1) + smart_nat(abs(n1)) + unit + "$"
    else:
        return "$" + smart_sign(n1) + r"\dfrac{" + smart_nat(abs(n1)) + unit + "}{" + str(d1) + "}$"
