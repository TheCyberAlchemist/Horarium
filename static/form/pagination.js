// $(document).ready(function(){

// });

function pageChanger() {
    var page1 = document.getElementById("first_page");
    var page2 = document.getElementById("second_page");
    var pageButton = document.getElementById("page_change");
    var pageButtonContainer = document.getElementById("page_changer_button_container");
    if(page2.style.display === "none") {
        console.log("HEY");
        page2.style.display = "block";
        page1.style.display = "none";
        pageButton.innerHTML = "Prev Page";
        pageButtonContainer.style.left = "3%";
    }
    else {
        page2.style.display = "none";
        page1.style.display = "block";
        pageButton.innerHTML = "Next Page";
        pageButtonContainer.style.left = "83%";
    }
}