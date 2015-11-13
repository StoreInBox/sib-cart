from django.apps import apps
from django.conf import settings

from .exceptions import CartSettingsError


class ExternalModels(object):
    PRODUCT_MODEL_KEY = 'Product'

    EXTERNAL_MODELS_MAP = {
        'Product': PRODUCT_MODEL_KEY,
    }

    def __getattr__(self, name):
        return self.get_model(name)

    def get_model(self, name):
        if not hasattr(self, name):
            path = self.get_model_path(name)
            try:
                model = apps.get_model(path)
            except LookupError as e:
                raise CartSettingsError(
                    'Cannot import model "%s" for cart application: %s' % (name, e))
            setattr(self, name, model)
        return getattr(self, name)

    def get_model_path(self, name):
        if name not in self.EXTERNAL_MODELS_MAP:
            raise CartSettingsError('Model %s is not defined as external model' % name)
        key = self.EXTERNAL_MODELS_MAP[name]
        try:
            cart_settings = settings.CART
        except AttributeError:
            raise CartSettingsError(
                'Cannot find CART variable in settings. It need to be configured for application "cart"')
        try:
            path = cart_settings[key]
        except KeyError:
            raise CartSettingsError(
                'Cannot find model "%s" in CART settings. It has to be configured with key "%s"' % (name, key))
        return path


external_models = ExternalModels()
PRODUCT_PRICE = getattr(settings, 'CART', {}).get('product_price')
PRODUCT_NAME = getattr(settings, 'CART', {}).get('product_name')
PRODUCT_CODE = getattr(settings, 'CART', {}).get('product_code')
