# coding: utf-8
from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CartConfig(AppConfig):
    name = 'cart'
    verbose_name = _('Cart')

    def ready(self):
        pass
