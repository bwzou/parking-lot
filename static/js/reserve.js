/**
 * Created by zuodexin on 2016/4/22.
 */

// add a zero in front of numbers<10
function checkTime(i)
{
    if (i<10)
    {i="0" + i}
    return i
}

//转换时间间隔
Num2Str = function(num){
    hour=Math.floor(num/4);
    minute=(num%4)*15;
    //console.log("hour",hour,"minute",minute);
    return checkTime(hour)+":"+checkTime(minute);
    //return num;
};
Num2Time = function(num){
    hour=Math.floor(num/4);
    minute=(num%4)*15;
    var today=new Date();
    today.setHours(hour,minute,0);
    return today;
};

GetDefaultDate=function(){
    var date=new Date(Date.parse($("#picker").val()));
    if(isNaN(date.getTime()))
        date= new Date();
    return date;
}
GetDefaultFromTime = function(){
    var from=new Date();
    if($("#time-from").val()=="") {
        $("#time-from").val(from.getTime());
    }
    else{
        from=new Date(Number($("#time-from").val()));
    }
    return from.getHours()*4+Math.floor(from.getMinutes()/15);
}
GetDefaultToTime = function(){
    var to=new Date();
    to.setHours(to.getHours()+4);
    if($("#time-to").val()=="") {
        $("#time-to").val(to.getTime());
    }
    else{
        to=new Date(Number($("#time-to").val()));
    }
    return to.getHours()*4+Math.floor(to.getMinutes()/15);
}
$(document).ready(function(){
    //初始化datepicker
    var date = GetDefaultDate();
    $("#picker").datepicker({
        changeMonth: true,
        changeYear: true,
        minDate: date,
        showAnim: "slideDown",
        defaultDate: new Date(),
        preText: "pre Month",
        nextText: "Next Month"
    });
    $("#picker").datepicker( "setDate", date );
    //初始化slider
    note = new Array([97]);
    for(var i=0;i<=96;i++){
        note[i]=Num2Str(i);
    }
    var from=GetDefaultFromTime();
    var to = GetDefaultToTime();
    $("#slider").slider({
        range: true,
        min: 0,
        max: 96,
        values: [ from, to ],
        slide: function(event,ui){
            var from=new Date();
            var to= new Date();
            from.setHours(Math.floor(ui.values[0]/4));
            from.setMinutes((ui.values[0]%4)*15);
            to.setHours(Math.floor(ui.values[1]/4));
            to.setMinutes((ui.values[1]%4)*15);
            $("#slider_value").val("from: "+Num2Str(ui.values[0]) + " to: "+Num2Str(ui.values[1]));
            $("#time-from").val(from.getTime());
            $("#time-to").val(to.getTime());
        }
    }) .slider("pips", {
        rest: "label",
        labels: note,
        step:8
    }).slider("float",{
        labels: note
    });

    $( "#slider_value" ).val( "from: "+Num2Str($( "#slider" ).slider( "values", 0 )) +
        " to: "+ Num2Str($( "#slider" ).slider( "values", 1 ) ));
    $("#submit-btn").click(function(){
        var from = new Date(Number($("#time-from").val()));
        var to = new Date(Number($("#time-to").val()));
        from.setDate(new Date(Date.parse($("#picker").val())).getDate());
        from.setMonth(new Date(Date.parse($("#picker").val())).getMonth());
        from.setFullYear(new Date(Date.parse($("#picker").val())).getFullYear());
        to.setDate(new Date(Date.parse($("#picker").val())).getDate());
        to.setMonth(new Date(Date.parse($("#picker").val())).getMonth());
        to.setFullYear(new Date(Date.parse($("#picker").val())).getFullYear());

        $("#time-from").val(from.getTime());
        $("#time-to").val(to.getTime());
        $('form').submit();
    });

});
