class CartError(Exception):
    pass


class CartSettingsError(CartError):
    pass


class CartModelError(CartError):
    pass


class CartProductError(CartModelError):
    pass


class CartViewError(CartError):
    pass
