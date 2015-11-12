
$(function(){   
    $("#lofinform").on('submit', function(e){
        var isvalidate=$("#lofinform").valid();
        if(isvalidate)
        {
            e.preventDefault();
            alert(getvalues("lofinform"));
        }
    });
});

function getvalues(f)
{
    var form=$("#"+f);
    var str='';
    $("input:not('input:submit')", form).each(function(i){
        str+='\n'+$(this).prop('name')+': '+$(this).val();
    });
    return str;
}

$(".a").on("click", function(event){
    if ($(this).is("[disabled]")) {
        event.preventDefault();
    }
});
