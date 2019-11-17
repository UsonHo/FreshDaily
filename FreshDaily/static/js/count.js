$(function () {
   $('.add').click(function () {
       var $count = $('.num_show');
       $count.val(parseInt($count.val()) + 1);
       $count.blur();
   });
   $('.minus').click(function () {
       var $count = $('.num_show');
       if($count.val() <= 1){
           $count.val(1)
       }else{
           $count.val(parseInt($count.val()) - 1);
       }
       $count.blur();
   });
   $('.num_show, .stock_show').blur(function () {
       var num = parseInt($(this).val());
       $(this).val(num);
       var price = $('.gprice').text();
       $('.totalPrice').text((num * parseFloat(price)).toFixed(2) + '元');
   })
});