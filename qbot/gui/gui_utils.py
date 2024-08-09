import wx


def _pydate2wxdate(date):
    import datetime

    assert isinstance(date, (datetime.datetime, datetime.date))
    tt = date.timetuple()
    dmy = (tt[2], tt[1] - 1, tt[0])
    return wx.DateTimeFromDMY(*dmy)


def _wxdate2pydate(date):
    import datetime

    assert isinstance(date, wx.DateTime)
    if date.IsValid():
        ymd = map(int, date.FormatISODate().split("-"))
        return datetime.date(*ymd)
    else:
        return None
