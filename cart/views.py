#  -*- coding: utf-8 -*-
from django.http import HttpResponse, QueryDict
from django.views.generic import View

from . import exceptions
from .models import Cart


class CartView(View):

    def dispatch(self, request, *args, **kwargs):
        self.cart = Cart(request.session)
        try:
            return super(CartView, self).dispatch(request, *args, **kwargs)
        except (exceptions.CartModelError, exceptions.CartViewError) as e:
            return HttpResponse(str(e), status=400)

    def get(self, request, *args, **kwargs):
        self.cart.save()
        return HttpResponse(self.cart.serialized())

    def post(self, request, *args, **kwargs):
        print QueryDict(request.body)
        product_pk = self._get_field_from_request(request, 'product_pk')
        count = self._get_field_from_request(request, 'count', int)
        self.cart.set(product_pk, count)
        return HttpResponse(self.cart.serialized())

    def patch(self, request, *args, **kwargs):
        product_pk = self._get_field_from_request(request, 'product_pk')
        count = self._get_field_from_request(request, 'count', int)
        self.cart.add(product_pk, count)
        return HttpResponse(self.cart.serialized())

    def delete(self, request, *args, **kwargs):
        product_pk = self._get_field_from_request(request, 'product_pk')
        self.cart.remove(product_pk)
        return HttpResponse(self.cart.serialized())

    def _get_field_from_request(self, request, field, convert_to_type=None):
        try:
            value = QueryDict(request.body)[field]
        except KeyError:
            raise exceptions.CartViewError('Field "%s" is required.' % field)
        if convert_to_type is None:
            return value
        try:
            return convert_to_type(value)
        except TypeError:
            raise exceptions.CartViewError('Field "%s" has to be instance of type %s' % (field, convert_to_type))
