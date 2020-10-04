
function toggle() {
    var x = document.getElementById("show_tree");
    var y = document.getElementById("show_navbar");
    var z = document.getElementById("whole_container_id");
    if (x.style.display === "none") {
      x.style.display = "block";
      y.style.display = "none";
      z.style.display = "none";
    } else {
      x.style.display = "none";
      y.style.display = "inline";
      z.style.display = "block";
    }
  }
