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
$(document).ready(function(){
    //初始化datepicker
    var today = new Date();
    $("#picker").datepicker({
        changeMonth: true,
        changeYear: true,
        minDate: today,
        showAnim: "slideDown",
        defaultDate: today,
        preText: "pre Month",
        nextText: "Next Month"
    });
    $("#picker").datepicker( "setDate", today );
    //初始化slider
    note = new Array([97]);
    for(var i=0;i<=96;i++){
        note[i]=Num2Str(i);
    }
    $("#slider").slider({
        range: true,
        min: 0,
        max: 96,
        values: [ 28, 68 ],
        slide: function(event,ui){
            $("#slider_value").val("from: "+Num2Str(ui.values[0]) + " to: "+Num2Str(ui.values[1]));
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
});