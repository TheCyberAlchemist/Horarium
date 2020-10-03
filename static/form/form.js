function visibility1(self) {
  console.log(self);
  var a = document.getElementById("myinput1");
  var b = document.getElementById("hide1");
  var c = document.getElementById("hide2");

  if (a.type === "password") {
    a.type = "text";
    b.style.display = "inline";
    c.style.display = "none";
  }
  else if(a.type === "text"){
    a.type = "password";
    b.style.display = "none";
    c.style.display = "inline";
  }
}

function visibility2() {
  var x = document.getElementById("myinput2");
  var y = document.getElementById("hide3");
  var z = document.getElementById("hide4");

  if (x.type === "password") {
    x.type = "text";
    y.style.display = "inline";
    z.style.display = "none";
    }
  else if(x.type === "text" ){
    x.type = "password";
    y.style.display = "none";
    z.style.display = "inline";
  }
}


/*//////////////DROPDOWN//////////////*/

const selected = document.querySelector(".selected");
const optionsContainer = document.querySelector(".options_container");
const searchBox = document.querySelector(".search_box input");

const optionsList = document.querySelectorAll(".dropdown_option");

selected.addEventListener("click", () => {
  optionsContainer.classList.toggle("active");

  searchBox.value = "";
  filterList("");

  if (optionsContainer.classList.contains("active")) {
    searchBox.focus();
  }
});

optionsList.forEach(o => {
  o.addEventListener("click", () => {
    selected.innerHTML = o.querySelector("label").innerHTML;
    optionsContainer.classList.remove("active");
  });
});

searchBox.addEventListener("keyup", function(e) {
  filterList(e.target.value);
});

const filterList = searchTerm => {
  searchTerm = searchTerm.toLowerCase();
  optionsList.forEach(option => {
    let label = option.firstElementChild.nextElementSibling.innerText.toLowerCase();
    if (label.indexOf(searchTerm) != -1) {
      option.style.display = "block";
    } else {
      option.style.display = "none";
    }
  });
};
