/*
Connect:
    1. <script src="{{ STATIC_URL }}cart/cart.js"> </script>
    2. Должен быть задан урл в свойстве тега data-cart-url='some/url/'.

cart data in request.session: {'cart':{"total": total sum, "count":
        cart count, "products": {product_pk_1: {'product_code': product_code,
       'name': name,  'price': price,  'quant': quant, 'sum_': sum_}...}}

Object cart:
    After  successfully execution all methods update the attributes of the cart and call function callback

    Methods:

        cart.set(product_pk, quant, callback) - set quantity of the product in the cart equal quant

        cart.add(product_pk, quant, callback) - add quantity of the product in the cart equal quant

        cart.remove(product_pk, callback) - remove the product from the cart

        cart.get(callback) - get attributes of the cart

        cart.clear(callback) -clear the cart

     Attributes :
        cart.products = {{'product_pk': product_code,  'name': name,  'price': price,
           'quant': quant, 'sum_': sum_}...} - dictionary

        cart.total - total cost of the cart products

        cart.count - total quantity of the cart products

        getUrl() - url

While no use settings .
Settings:
    There is necessary insert in  settings:
    CART_SETTINGS = {
        'model_name': model_name,
        'appl_name': appl_name,
        'price_field_name': price_field_name,
        'code_field_name': code_field_name,
        'name_field_name': name_field_name
    }
*/

// TODO

function Cart(cartUpdateCallback) {
    var url = null,
        vm = this;

    init();

    vm.set = function(product_pk, count, callback) {
        $.ajax({
            url: getUrl(),
            type: "POST",
            data: {product_pk: product_pk, count: count},
        }).done(function(response) {
            updateData(response, callback);
        });
    }

    vm.add = function(product_pk, count, callback) {
        $.ajax({
            url: getUrl(),
            type: "PATCH",
            data: {product_pk: product_pk, count: count},
        }).done(function(response) {
            updateData(response, callback);
        });
    }

    vm.delete = function(product_pk, callback) {
        $.ajax({
            url: getUrl(),
            type: "DELETE",
            data: {product_pk: product_pk},
        }).done(function(response) {
            updateData(response, callback);
        });
    }

    function init() {
        $.ajax({
            url: getUrl(),
            type: "GET",
        }).done(function(response) {
            updateData(response);
        });
    }

    function getUrl() {
        if (url === null) {
            url = $('[sib-cart-role="init"]').attr('sib-cart-url');
        }
        return url;
    }

    // update object properties based on server response
    function updateData(response, callback) {
        parsedResponse = $.parseJSON(response)
        vm.count = parsedResponse.count;
        vm.total = parsedResponse.total;
        vm.products = parsedResponse.products;

        if (callback) {
            callback();
        }
        if (cartUpdateCallback) {
            cartUpdateCallback();
        }
    }
}
