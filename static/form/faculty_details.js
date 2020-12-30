let old_load,subject_events;
function set_load(load,events){
    old_load = load;
    events = events.replace(/&#34;/ig,'"',);
    subject_events= JSON.parse(events);
    // for(i in json){
    //     console.log(json[i]);
    // }
}
$(document).ready(function(){
    $("#first").click(function(){
        $("#second_page").hide();
        $("#third_page").hide();
        $("#first_page").show(100);

        $(this).addClass("active");
        $("#second").removeClass("active");
        $("#third").removeClass("active");
    });
    $("#second").click(function(){
        $("#first_page").hide();
        $("#third_page").hide();
        $("#second_page").show(100);

        $(this).addClass("active");
        $("#third").removeClass("active");
        $("#first").removeClass("active");
    });
    $("#third").click(function(){
        $("#second_page").hide();
        $("#first_page").hide();
        $("#third_page").show(100);

        $(this).addClass("active");
        $("#second").removeClass("active");
        $("#first").removeClass("active");
    });

    $(".submit_button").click(function(){
        if(old_load > parseInt($("input[name='total_load']").val())){
            // swal 
            console.table(subject_events);
        }
        // if yes
        // $(".myform").submit();
    });
});

// function pageChanger() {
//     var page1 = document.getElementById("first_page");
//     var page2 = document.getElementById("second_page");
//     var page3 = document.getElementById("third_page");
//     var pageButton = document.getElementById("page_change");
//     var pageButtonContainer = document.getElementById("page_changer_button_container");
//     if(page2.style.display === "none") {
//         console.log("HEY");
//         page2.style.display = "block";
//         page1.style.display = "none";
//         pageButton.innerHTML = "Prev Page";
//         pageButtonContainer.style.left = "3%";
//     }
//     else if() {
//         page2.style.display = "none";
//         page1.style.display = "block";
//         pageButton.innerHTML = "Next Page";
//         pageButtonContainer.style.left = "83%";
//     }
// }