import re
from django.db import models
from django.core import validators


class Account(models.Model):

    code = models.CharField(max_length=15,
                            unique=True,
                            help_text=('Required. 30 characters or fewer. Letters, numbers and '
                                       '@/./+/-/_ characters'),
                            validators=[
                                validators.RegexValidator(re.compile(
                                    '^[\w.@+-]+$'), ('Enter a valid username.'), 'invalid')
                            ],
                            verbose_name=('Account')
                            )
    name = models.CharField(max_length=60)
    debit = models.FloatField(help_text=('Calculated field'))
    credit = models.FloatField(help_text=('Calculated field'))
