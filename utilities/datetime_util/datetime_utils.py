# -*- coding: utf-8 -*-
import os
from datetime import datetime

import pandas as pd
import pytz
from dateutil.relativedelta import relativedelta
from pandas import DataFrame


def get_sys_date(to_format: str = '%Y-%m-%d %H:%M:%S')->str:
    """
    Get system date of today

    :return:
    system datetime string of today
    """
    sys_date = datetime.now().strftime(to_format)
    return sys_date


def get_months_diff(date1: datetime.date, date2: datetime.date)->int:
    """
    Return date difference in months

    :param date1:
    target date

    :param date2:
    referencing date

    :return:
    date difference in months
    """
    rd = relativedelta(date1, date2)
    return (12 * rd.years + rd.months) + 1


def format_date_iso(d: str, from_format: str = '%Y%m%d')->str:
    """
    Format from '20161231' to '2016-12-31'

    :param d:
    source date

    :param from_format:
    source date format

    :return:
    date in iso format
    """
    d = datetime.strptime(d, from_format)

    return d.date().isoformat()


def format_date(d: str, from_format: str = '%Y-%m-%d', to_format: str = '%Y%m%d')->str:
    """
    Format date

    :param d:
    source date

    :param from_format:
    source format

    :param to_format:
    target format

    :return:
    date in target format
    """
    d = datetime.strptime(d, from_format)

    return d.strftime(to_format)


def format_24time(t:str, format_str:str = '%I:%M%p')->str:
    """
    Format to 24h time

    :param t:
    source time

    :param format_str:
    source time format

    :return:
    time format in 24H
    """
    t = datetime.strptime(t, format_str)

    return t.strftime("%H:%M")


def local_time_diff(local1: str, local2: str)->int:
    """
    Calculate local time difference in minutes

    :param local1:
    target time

    :param local2:
    referencing time

    :return:
    time difference in minutes
    """
    h1, m1 = [int(i) for i in local1.split(":")]
    h2, m2 = [int(i) for i in local2.split(":")]

    diff = 60 * (h1 - h2) + (m1 - m2)
    return diff


def get_month_to_date(today: datetime.date)->datetime.date:
    """
    Return first date of month on today

    :param today:
    target date

    :return:
    first date of month on today
    """
    mtd = today + relativedelta(days=(-1 * today.day + 1))

    return mtd


def get_year_to_date(today: datetime.date)->datetime.date:
    """
    Return first date of year on today

    :param today:
    target date

    :return:
    first date of year on today
    """
    ytd = today + relativedelta(days=(-1 * today.day + 1), months=(-1 * today.month + 1))

    return ytd


def get_year_to_date_bystr(today_str: str, today_format: str = '%Y-%m-%d')->datetime.date:
    """
    Return first date of year on today

    :param today_str:
    target date string

    :param today_format:
    target date format

    :return:
    first date of year on today
    """
    today = datetime.strptime(today_str, today_format)
    ytd = today + relativedelta(days=(-1 * today.day + 1), months=(-1 * today.month + 1))

    return ytd


def get_ytd(today: datetime.date, to_format: str = '%Y%m%d')->str:
    """
    Return first date of year on today

    :param today:
    target date

    :param to_format:

    :return:
    first date of year on today
    """

    ytd = today + relativedelta(days=(-1 * today.day + 1), months=(-1 * today.month + 1))
    ytd_str = ytd.strftime(to_format)
    return ytd_str


def get_ytd_bystr(today_str: str, from_format: str = '%Y%m%d', to_format: str = '%Y%m%d')->str:
    """
    Return first date of year on today

    :param today_str:
    target date string

    :param from_format:
    target date org format

    :param to_format:
    target date output format

    :return:
    first date of year on today
    """
    today = datetime.strptime(today_str, from_format)
    ytd = today + relativedelta(days=(-1 * today.day + 1), months=(-1 * today.month + 1))
    ytd_str = ytd.strftime(to_format)
    return ytd_str


def get_delta_date(today: datetime.date,
                   days: int = 0,
                   weeks: int = 0,
                   months: int = 0,
                   years: int = 0)->datetime.date:
    """
    Return a date add/minus days, weeks, months or years to today

    :param today:
    :param days:
    :param weeks:
    :param months:
    :param years:

    :return:
    A date add/minus days, weeks, months or years to today
    """
    start_date = today + relativedelta(days=days, weeks=weeks, months=months, years=years)
    return start_date


def get_delta_date_str(today: datetime.date,
                       to_format: str = '%Y%m%d',
                       days: int = 0,
                       weeks: int = 0,
                       months: int = 0,
                       years: int = 0)->str:
    """
    Return a date add/minus days, weeks, months or years to today

    :param today:
    :param to_format:
    :param days:
    :param weeks:
    :param months:
    :param years:

    :return:
    A date add/minus days, weeks, months or years to today in str format
    """
    start_date = today + relativedelta(days=days, weeks=weeks, months=months, years=years)
    return start_date.strftime(to_format)


def get_delta_date_bystr(today_str: str,
                         from_format: str = '%Y-%m-%d',
                         days: int = 0,
                         weeks: int = 0,
                         months: int = 0,
                         years: int = 0)->datetime.date:
    """
    Return a date add/minus days, weeks, months or years to today str

    :param today_str:
    :param from_format:
    :param days:
    :param weeks:
    :param months:
    :param years:

    :return:
    A date add/minus days, weeks, months or years to today
    """
    today = datetime.strptime(today_str, from_format)
    start_date = today + relativedelta(days=days, weeks=weeks, months=months, years=years)
    return start_date


def convert_datetime_timezone(dt: (str, datetime.date), tz1: str, tz2: str,
                              from_format: str = "%Y-%m-%d %H:%M:%S",
                              to_format: str = "%Y-%m-%d %H:%M:%S")->datetime.date:
    """
    Convert timezone of a datetime object from tz1 to tz2

    :param dt:
    target date, str or datetime object

    :param tz1:
    from timezone

    :param tz2:
    to timezone

    :param from_format:
    target date org format

    :param to_format:
    target date output format

    :return:
    datetime object in timezone tz2 in format "%Y-%m-%d %H:%M:%S"
    """

    tz1 = pytz.timezone(tz1)
    tz2 = pytz.timezone(tz2)

    if isinstance(dt, str):
        dt = datetime.strptime(dt, from_format)
    elif isinstance(dt, datetime.date):
        pass
    else:
        raise TypeError('input dt must be str or datetime.date')

    dt = tz1.localize(dt)
    dt = dt.astimezone(tz2)
    dt = dt.strftime(to_format)

    return dt
