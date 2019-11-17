$(function () {
   // 第二种方式ajax实现登录
   $('button').click(function () {
       $.ajax({
           url: '/user/login_check/',
           type: 'POST',
           data: $('form').serialize(),
           dataType: 'JSON',
           success: function (data) {
               // console.log(data);
               if(data.error_name == 1){
                   $('.user_error').html('用户名错误').show();
               }else if(data.error_pwd == 1){
                   $('.pwd_error').html('密码错误').show();
               }else{
                   // $.ajax({
                   //     url: '/user/login_check2/',
                   //     type: 'POST',
                   //     dataType: 'JSON',
                   //     data: $('form').serialize(),
                   //     success: function (data) {
                   //         console.log(123);
                   //         if(data.status){
                   //             mysubmit();
                   //         }
                   //     }
                   // })
                   mysubmit();
               }
           }
       });
       return false;
   });
   function mysubmit() {
       $('form').submit();
   }

   $('.name_input').focus(function () {
       $('.user_error').hide();
   });
   $('.pass_input').focus(function () {
       $('.pwd_error').hide();
   })
});