function checkFullIn(){
    var x  = document.getElementById('username').value;
   // var x=document.forms["myform"]["username"].value;
   if (x==null || x== "" || x == "用户名")
   {
        alert("请填写用户名！");
        return false;
   }
    // var y=document.forms["myform"]["password"].value;
   var y  = document.getElementById('password').value;
    if (y==null || y=="" || y == "密码")
    {
        alert("请填写密码！");
        return false;
    }
    //这里不用cookie缓存 用Redis来做缓存
    //
    // if ("wtk" == x && "qweasdzxc" == y){
    //     if (document.getelementbyid('checkboxid').checked){
    //         setcookie("checkboxc", true, 7);
    //         setcookie("usernamec", document.getelementbyid('usernameid').value, 7);
    //         setcookie("passwordc", document.getelementbyid('passwordid').value, 7);
    //     }
    //     else{
    //         setcookie(checkbox, false, 7);
    //     }
    //     return true;
    // }else{
    //     <!-- 这里没有去数据库中调用用户名和密码 -->
    //     if("wtk" != x){
    //         alert("该用户不存在，是否注册？");
    //         <!-- 以后可以添加注册页面 -->
    //     }else if ("qweasdzxc" != y){
    //         alert("密码错误！");
    //     }
    //     <!-- 需要借鉴商店网站来更新注册功能 -->
    //     return false;
    // }
}

function setcookie(cname,cvalue,exdays){
    var d = new date();
    d.settime(d.gettime()+(exdays*24*60*60*1000));
    var expires = "expires="+d.togmtstring();
    document.cookie = cname+"="+cvalue+"; "+expires + "; path=/";
}

function getcookie(cname){
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i].trim();
        if (c.indexof(name)==0) return c.substring(name.length,c.length);
    }
    return "";
}

function checkcookie(){
    if (true == getcookie("checkboxc")){
        //选中复选框，自动填入用户名和密码
        document.getelementbyid('checkboxid').checked = true;
        document.getelementbyid('usernameid').value = getcookie("usernamec");
        document.getelementbyid('passwordid').value = getcookie("passwordc");
    }
}