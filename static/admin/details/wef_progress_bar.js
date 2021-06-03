$(document).ready(function() {

    let p = 0;
    function get_colour(per){
        p+=1;
        let unit = parseInt(255 * (per/100));
        let red = unit;
        let green = 255- unit;
        //document.getElementsByClassName("progress-bar").style.backgroundColor = `rgb(${red},${green},3)`;
        return `rgb(${red},${green},3)`;
    };
    $(".progress-bar").each(function(){
        $(this).css("backgroundColor" , get_colour($(this).attr("aria-valuenow"))); 
        console.log(($(this).attr("aria-valuenow")));
        
    });
})