/*
Add to page:
    <script sib-cart-role="init" sib-cart-url="{% url 'cart' %}" src="{% static 'cart/cart.js' %}"></script>

Module provides Cart class that represents cart data and allow to execute operations with cart.
*/

function Cart(cartUpdateCallback) {
    var url = null,
        vm = this;

    init();

    // set product count in cart
    vm.set = function(product_pk, count, callback) {
        $.ajax({
            url: getUrl(),
            type: "POST",
            data: {product_pk: product_pk, count: count},
        }).done(function(response) {
            updateData(response, callback);
        });
    }

    // increase/decrease product count in cart
    vm.add = function(product_pk, count, callback) {
        $.ajax({
            url: getUrl(),
            type: "PATCH",
            data: {product_pk: product_pk, count: count},
        }).done(function(response) {
            updateData(response, callback);
        });
    }

    // delete product in cart
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
