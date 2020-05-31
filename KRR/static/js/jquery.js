$(document).ready(function(){
    function rec_play(){
    $.ajax({
        url: "/rec-play",
        data: $("form").serialize(),
        type:"POST",
        success: function(response) {
            console.log(response);
        },
        error: function(error){
            console.log(error);
        }
    });
    };
    
    $("rec-play").submit(function(event){
        event.prevemtDefault();
    });
});

