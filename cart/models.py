# coding: utf-8
from __future__ import unicode_literals

from decimal import Decimal
import json
from operator import attrgetter

from . import settings
from .exceptions import CartModelError, CartProductError


class CartProduct(object):
    """ Wrapper for abstract product that is defined by cart application settings.

    Provides cart product properties as serializable values.
    """

    def __init__(self, pk, count=0, total=0):
        try:
            self.product = settings.external_models.Product.objects.get(pk=pk)
        except settings.external_models.Product.DoesNotExist:
            raise CartProductError("Cannot find product with pk {}".format(pk))
        self.count = count
        self._calculate_total()

    def _get_attr(self, attr):
        try:
            value = attrgetter(attr)(self.product)
        except AttributeError:
            raise CartProductError("Cannot get attribute '{}' from product {}".format(attr, self.product))
        if hasattr(value, '__call__'):
            return value()
        return value

    @property
    def pk(self):
        return str(self._get_attr('pk'))

    @property
    def name(self):
        return str(self._get_attr(settings.PRODUCT_NAME))

    @property
    def code(self):
        return str(self._get_attr(settings.PRODUCT_CODE))

    @property
    def price(self):
        return self._get_attr(settings.PRODUCT_PRICE)

    @property
    def serialized_price(self):
        return '{0:.2f}'.format(self._get_attr(settings.PRODUCT_PRICE))

    @property
    def serialized_total(self):
        return '{0:.2f}'.format(self.total)

    def set_count(self, count):
        self.count = count
        self._calculate_total()

    def serialize(self):
        return {
            'pk': self.pk,
            'name': self.name,
            'code': self.code,
            'price': self.serialized_price,
            'count': self.count,
            'total': self.serialized_total,
        }

    def _calculate_total(self):
        self.total = Decimal(self.price) * self.count


class Cart(object):
    """ Cart model that stores products in session

    Cart is stored in session in next format:
    {
        <count> - count of all products in cart
        <total> - price for all products in cart
        <products> - list of serialized products in cart. Last added/modified product will be last in list.
            Product format:
            {
                <pk> - product PK,
                <name>
                <code>
                <price>
                <count> - particular product count
                <total> - price for all products
            }
    }
    Cart key in session: "cart"
    """

    CART_KEY = 'cart'

    def __init__(self, session):
        serialized_cart = session.get(self.CART_KEY, {})
        self.session = session
        self.count = serialized_cart.get('count', 0)
        self.total = Decimal(serialized_cart.get('total', 0))
        self.products = serialized_cart.get('products', [])

    def set(self, product_pk, count):
        product = self._get_product(product_pk)
        self._set_product_count(product, count)

    def remove(self, product_pk):
        self.set(product_pk, 0)

    def add(self, product_pk, count):
        if count == 0:
            raise CartModelError('It is useless to add zero count to product')
        product = self._get_product(product_pk)
        self._set_product_count(product, product.count + count)

    def _get_product(self, product_pk):
        """ Try to find product in cart, if does not exist - return new CartProduct """
        try:
            return [CartProduct(product_pk, count=p['count'])
                    for p in self.products if p['pk'] == str(product_pk)][0]
        except IndexError:
            return CartProduct(product_pk)

    def _set_product_count(self, product, count):
        if count < 0:
            raise CartModelError('Cannot set product count to value less them zero')

        old_count, old_total = product.count, product.total
        product.set_count(count)

        total_diff = product.total - old_total
        count_diff = product.count - old_count
        self.total += total_diff
        self.count += count_diff

        if product.count:
            self._add_product(product)
        else:
            self._remove_product(product)

        self.save()

    def _add_product(self, product):
        self.products = [p for p in self.products if p['pk'] != product.pk] + [product.serialize()]

    def _remove_product(self, product):
        self.products = [p for p in self.products if p['pk'] != product.pk]

    def save(self):
        """ Save changes to session """
        serialized_total = '{0:.2f}'.format(self.total)
        self.session[self.CART_KEY] = {
            'total': serialized_total,
            'count': self.count,
            'products': self.products,
        }

    def serialized(self):
        """ Return serialized cart """
        return json.dumps(self.session[self.CART_KEY])
