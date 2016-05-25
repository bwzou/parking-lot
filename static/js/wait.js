/**
 * Created by zuodexin on 2016/5/22.
 */
time =20

polling=function(){
    $.get("/get_result",
        {
            name: $('input[name="a"]').val(),
        },
        function(data){
            if(data=='success'){
                window.location.href="/customer_index"
            }
            else if(data=='wait'){
                time --;
                if (time>0){
                    var t=setTimeout("polling()",1000)
                }else{
                    $("#loadinfo").toggle()
                    $("#failinfo").toggle()
                    $("#btn_changetime").toggle()
                    $("#btn_returnhome").toggle()
                }
            }
            
        })
}


$(document).ready(function(){
    $('#reserveModal').modal('show')
    polling();
});