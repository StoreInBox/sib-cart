
$(document).ready(function() {

    var order = {
        'setProduct': function(data) {
            product = cart.products[data.productPk];
            var name = data.productPk + '_sum';
            $(order.selectorRole(name)).text(product.sum_);
            order.setTotalData();
        },
        'setTotalData': function() {
            $('[data-role="cart-count"]').text(cart.count);
            $('[data-role="cart-total"]').text(cart.total);
            checkOrderAvailability();
        },

        'selectorRole': function(name) {
            return '[data-role=' + '"' + name  + '"'+ "]";
        }
     };

    $('[data-role="remove"]').on('click', function() {
        var productPk = $(this).attr('data-value');
        if (confirm("Удалить товар из корзины?")) {
            $(order.selectorRole(productPk)).remove();
            var productPkList = [productPk,];
            cart.remove(productPkList, order.setTotalData);
            var nextCartRow = $('[data-visible="false"]').first();
            if (nextCartRow) {
                nextCartRow.attr({'data-visible': 'true'});
                nextCartRow.css({'display': 'block'});
            }
        }
   });

    $('[data-role="quant"]').on('change', function() {
       var productPk = parseInt($(this).attr('data-product-id'));
       var quant = $(this).val();
       order.productPk = productPk;
       var callback = order.setProduct.bind('context', {'productPk': productPk});
       var productDict = {};
       productDict[productPk] = quant;
       cart.set(productDict, callback);
       $('[data-product-id="'+ productPk + '"][data-role="quant"]').val(quant);
    });

    $('[data-role="clear"]').on('click', function() {
        cart.clear(order.setTotalData);
    });

    function checkOrderAvailability() {
        if (parseFloat($('[data-role="cart-count"]').text()) === 0) {
            $('[data-role="order-block"]').hide();
        }
    }

    checkOrderAvailability();

});
