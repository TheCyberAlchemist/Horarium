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
    function getColor(value){
        //value from 0 to 1
        value /= 100;
        var hue=((1-value)*120).toString(10);
        return ["hsl(",hue,",100%,50%)"].join("");
    }
    $(".progress-bar").each(function(){
        $(this).css("backgroundColor" , getColor($(this).attr("aria-valuenow"))); 
        console.log(($(this).attr("aria-valuenow")));
        
    });
})