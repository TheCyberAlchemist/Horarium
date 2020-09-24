// function showPass() {
//   const x = document.getElementById("myinput");
//   if (x.type === "password") {
//       document.getElementById("toggle").src == "visibility1.png";
//       x.type = "text";
//   }
//   else {
//     x.type = "password";
//     document.getElementById("toggle").src == "visibility.png";
//   }
// }

function toggle() {
  if(document.getElementById("toggle").src == "visibility1.png"){
    document.getElementById("toggle").src == "visibility.png";}
  else {
    document.getElementById("toggle").src == "visibility1.png";
  }
}
