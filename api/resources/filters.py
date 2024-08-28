from datetime import datetime
from enum import Enum
from typing import Optional


class OrderByOption(str, Enum):
    ASC = "asc"
    DESC = "desc"


class SortByOption(str, Enum):
    DATE_FROM = "date_from"
    DATE_TO = "date_to"


class QueryFilter:

    @staticmethod
    def __format_date(date_input: Optional[str]):
        return datetime.strptime(
            f"{date_input}-01",
            "%Y-%m-%d").date() if date_input else datetime.today().date()

    @staticmethod
    def __set_sort_option(option: OrderByOption) -> bool:
        return option is option.DESC

    def sort(self, data: list, sort_by: SortByOption, order_by: OrderByOption):
        try:
            return sorted(
                data,
                key=lambda x: self.__format_date(getattr(x, sort_by)),
                reverse=self.__set_sort_option(order_by))
        except AttributeError:
            return data
