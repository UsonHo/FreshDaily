function logOut(){
    $.get('/user/logout/', function (data) {
       if(data.status){
           location.reload();
       }
    });
    return false;
}