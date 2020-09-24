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
function toggle_form() {
	let form_container = document.getElementsByClassName('form-container')[0];
	if(form_container.style.display == 'block'){
		form_container.style.display = 'none';
	}else {
		form_container.style.display = 'block';
	}
}