# -*- coding: utf-8 -*-
"""
provide class functions to adjust rem form data based on old rem form data
such datastructure is useful when first-in-first-out mechanism considered in selling funds
and it is also useful when converting the shares of funds.

as the nested list structure is very fragile and tend to induce unpredicatble behaviors,
we strongly recommended anytime when rem data serves as function paramters, 
only utilize functions from this module
"""
from xalpha.cons import convert_date, myround

_errmsg = "One cannot move share before the lastest operation"


def copy(remc):
    """
    copy the rem form data so that the return is independent of the input
    """
    rem = [remcterm.copy() for remcterm in remc]
    return rem


def buy(remc, share, date):
    """
    :param remc: array of two-elements arrays, eg [[pd.Timestamp(), 50],[pd.Timestamp(), 30]
        the first element in tuple is pandas.Timestamp object for date while the second
        element is positive float for remaining shares, tuples in rem MUST be time ordered.
    :param share: positive float, only 2 decimal is meaningful.
    :param date: string in the date form or datetime object
    :returns: new rem after the buying
    """
    rem = copy(remc)
    share = myround(share)
    date = convert_date(date)
    if len(rem) == 0:
        return [[date, share]]
    elif (date - rem[-1][0]).days > 0:
        rem.append([date, share])
        return rem
    elif (date - rem[-1][0]).days == 0:
        rem[-1][1] = rem[-1][1] + share
        return rem
    else:
        raise Exception(_errmsg)


def sell(remc, share, date):
    """
    :returns: tuple, (sold rem, new rem)
        sold rem is the positions being sold while new rem is the positions being held
    """
    rem = copy(remc)
    share = myround(share)
    date = convert_date(date)
    totposition = sum([pos[1] for pos in rem])  # the remaining shares
    if totposition == 0:
        return ([], [])
    if (date - rem[-1][0]).days < 0:
        raise Exception(_errmsg)
    if share > totposition:
        share = totposition  # not raise error when you sell more than you buy
    soldrem = []
    newrem = []
    for i, pos in enumerate(rem):
        if share > myround(sum([rem[j][1] for j in range(i + 1)])):
            soldrem.append(rem[i])
        elif share == myround(sum([rem[j][1] for j in range(i + 1)])):
            soldrem.append(rem[i])
        elif share < myround(sum([rem[j][1] for j in range(i + 1)])):
            if share > sum([rem[j][1] for j in range(i)]):
                soldrem.append([rem[i][0], share - sum([rem[j][1] for j in range(i)])])
                newrem.append(
                    [rem[i][0], sum([rem[j][1] for j in range(i + 1)]) - share]
                )
            elif share <= sum([rem[j][1] for j in range(i)]):
                newrem.append(rem[i])
    return (soldrem, newrem)


def trans(remc, coef, date):
    """
    在基金份额折算时，将之前持有的仓位按现值折算，相当于前复权

    :param coef: the factor shown in comment column of fundinfo().price, but with positive value
    :param date: string in date form or datetime obj
    :returns: new rem after converting
    """
    rem = copy(remc)
    date = convert_date(date)
    if len(rem) == 0:
        return []
    if (date - rem[-1][0]).days <= 0:
        raise Exception(_errmsg)
    newrem = [[item[0], myround(item[1] * coef)] for item in rem]
    return newrem
