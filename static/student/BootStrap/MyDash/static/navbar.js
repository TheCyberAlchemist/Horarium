function toggle() {
    var el1 = document.getElementById("light"),
      el2 = document.getElementById("dark");
    if (el1.disabled) {
      el1.disabled = false;
      el2.disabled = "disabled";
    } else {
      el1.disabled = "disabled";
      el2.disabled = false;
    }
  }