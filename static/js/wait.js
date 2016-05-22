/**
 * Created by zuodexin on 2016/5/22.
 */

//ÂÖÑ¯
polling=function(){
    $.get("url",{},function(data){
        if(data=='success'){
            window.location.href="home"
        }
        else if(data=='wait'){
            var t=setTimeout("polling()",1000)
        }
        else if(data=='fail'){
            $("#loadinfo").toggle()
            $("#failinfo").toggle()
            $("#btn_changetime").toggle()
            $("#btn_returnhome").toggle()
        }
    })
}


$(document).ready(function(){
   $('#reserveModal').modal('show')
    polling();
});