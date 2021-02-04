import re
from collections import OrderedDict
from datetime import datetime, date

from dateutil.relativedelta import relativedelta
from django.db import models


class PersonIIN(models.Model):
    iin = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return self.iin

    @staticmethod
    def _is_valid(iin):
        reg_exp = re.compile(r'[0-9]{12}')
        if reg_exp.search(iin):

            if iin[6:7] == '3' or iin[6] == '4':
                user_born = int('19' + iin[0:2])
            else:
                user_born = int('20' + iin[0:2])
            month = int(iin[2:4])
            day = int(iin[4:6])
            current_date = datetime.now()
            try:
                difference = relativedelta(
                    current_date,
                    date(user_born, month, day)
                )
            except ValueError as e:
                return 'day is out of range for month'

            if difference.years < 0:
                return 'You cannot be less than 0'
            return difference

        else:
            return 'IIN should not consist of letters'

    @classmethod
    def check_object(cls, person):
        if isinstance(person, PersonIIN):
            return cls._is_valid(person.iin)
        elif isinstance(person, OrderedDict):
            return cls._is_valid(person['iin'])
        raise ValueError
