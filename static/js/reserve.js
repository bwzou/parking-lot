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

//ת��ʱ����
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
    if($("#time-from").val()==""||$("#end-time").val()=="") {
        $("#time-from").val(checkTime(from.getHours())+':'+checkTime(from.getMinutes()))
        $("#start-time").val(checkTime(from.getHours())+':'+checkTime(from.getMinutes()))
    }
    else{
        from=new Date(Number($("#time-from").val()));
    }
    return from.getHours()*4+Math.ceil(from.getMinutes()/15);
}
GetDefaultToTime = function(){
    var to=new Date();
    var today= new Date()
    to.setHours(to.getHours()+4);
    if(to.getDate()!=today.getDate()){
        to.setHours(23);
        to.setMinutes(45);
    }
   if($("#time-to").val()==""||$("#end-time").val()==""){
        $("#time-to").val(checkTime(to.getHours())+':'+checkTime(to.getMinutes()));
        $("#end-time").val(checkTime(to.getHours())+':'+checkTime(to.getMinutes()))
    }
    else{
        to=new Date(Number($("#time-to").val()));
    }
    return to.getHours()*4+Math.ceil(to.getMinutes()/15);
}


function isBefore(tx_start,tx_end){
    var start = tx_start.split(':');
    var end = tx_end.split(':');
    console.log(start,end);
    if(parseInt(start[0])*100+parseInt(start[1])>=parseInt(end[0])*100+parseInt(end[1]))
        return false
    else return true
}
function NormalizeTime(tx_time){
    var arr=tx_time.split(':');
    var hour=Number(arr[0]);
    var minute=Number(arr[1]);
    hour+=Math.floor(Math.ceil(minute/15)*15/60)
    minute=Math.ceil(minute/15)*15%60;
    if(hour==24){
        hour=23;
        minute=45
    }
    return checkTime(hour)+':'+checkTime(minute)
}

$(document).ready(function(){
    //��ʼ��datepicker
    var date = GetDefaultDate();
    $("#picker").datepicker({
        changeMonth: true,
        changeYear: true,
        minDate: new Date(),
        showAnim: "slideDown",
        defaultDate: date,
        preText: "pre Month",
        nextText: "Next Month"
    });
    $("#picker").datepicker( "setDate", date );
    //��ʼ��slider
    note = new Array([97]);
    for(var i=0;i<=96;i++){
        note[i]=Num2Str(i);
    }
    var from=GetDefaultFromTime();
    var to = GetDefaultToTime();
    console.log(from,to)
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
        $('#reserve-form').submit();
    });


    //picker for mobile
    $("#picker-mobile").datepicker({
        changeMonth: true,
        changeYear: true,
        minDate: new Date(),
        showAnim: "slideDown",
        defaultDate: date,
        preText: "pre Month",
        nextText: "Next Month"
    });
    $("#picker-mobile").datepicker( "setDate", date );

    //slider for mobile
    var curr=new Date();
    $("#time-hour").slider({
        max: 23,
        value:curr.getHours()
    }).slider("pips", {
        rest: "label",
        step:3
    }).slider("float");

    $("#time-minute").slider({
        max: 59,
        value:curr.getMinutes()
    }).slider("pips", {
        rest: "label",
        step:15,
    }).slider("float");

    $('#timeModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget) // Button that triggered the modal
        var content = button.data('whatever') // Extract info from data-* attributes
        var modal = $(this)
        modal.find('.modal-title').text(content)
        if(content=='Start'){
            var hour=Number($('#start-time').val().split(':')[0]);
            var minute=Number($('#start-time').val().split(':')[1]);
            $("#time-hour").slider('option','value',hour);
            $('#time-minute').slider('option','value',minute)
        }
        else if(content=='End'){
            var hour=Number($('#end-time').val().split(':')[0]);
            var minute=Number($('#end-time').val().split(':')[1]);
            $("#time-hour").slider('option','value',hour);
            $('#time-minute').slider('option','value',minute)
        }
    })
    $('#btn-done').on('click',function(event){
        var modal = $('#timeModal')
        var title = modal.find('.modal-title').text();
        var hour = $( "#time-hour").slider( 'option','value');
        var minute = $( "#time-minute").slider( 'option','value');
        if(title=='Start'){
            $('#start-time').val(NormalizeTime(checkTime(hour)+':'+checkTime(minute)));
        }
        else if(title=='End'){
            $('#end-time').val(NormalizeTime(checkTime(hour)+':'+checkTime(minute)));
        }
        $('#timeModal').modal('hide')
    });
    $('#submit-btn-mobile').on('click',function(event){
        var tx_start=NormalizeTime($('#start-time').val())
        var tx_end=NormalizeTime($('#end-time').val())
        if(isBefore(tx_start,tx_end))
        {
            console.log('start time is before leaving time')
            $('#slider-value-mobile').val("from: "+tx_start + " to: "+tx_end)
            console.log( $('#slider-value-mobile').val())
            $('#reserve-form-mobile').submit();
        }
        else {
            alert('start time is after leaving time');
            console.log('start time is after leaving time')
        }
    });

});