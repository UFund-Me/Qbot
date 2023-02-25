# -*- coding: utf-8 -*-
"""
exceptions in xalpha packages
"""


class XalphaException(Exception):
    pass


class FundTypeError(XalphaException):
    """
    The code mismatches the fund type obj, fundinfo/mfundinfo
    """

    pass


class FundNotExistError(XalphaException):
    """
    There is no fund with given code
    """

    pass


class TradeBehaviorError(XalphaException):
    """
    Used for unreal trade attempt, such as selling before buying
    """

    pass


class HttpStatusError(XalphaException):
    """
    Used when the return request has http code beyond 200
    """

    pass


class ParserFailure(XalphaException):
    """
    Used for exception when parsing fund APIs
    """

    pass


class DataSourceNotFound(XalphaException):
    """
    Used when authentication required data source is not ready to use
    """

    pass


class DataPossiblyWrong(XalphaException):
    """
    Used for data failed to verify
    """

    pass


class DateMismatch(XalphaException):
    """
    Used for lof prediction
    """

    def __init__(self, code, reason=""):
        self.code = code
        self.reason = reason

    def __repr__(self):
        return self.reason

    __str__ = __repr__


class NonAccurate(XalphaException):
    """
    Used for lof prediction
    """

    def __init__(self, code, reason=""):
        self.code = code
        self.reason = reason

    def __repr__(self):
        return self.reason

    __str__ = __repr__
