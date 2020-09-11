var rd=['man.png','girl.png','man2.png','girl2.png','boy.png'];
	function avatr()
{
	var ava=document.getElementById('av').src=rd[Math.floor(Math.random() * rd.length)];
}
function submith()
{
	console.log('hi');
	var name1=document.getElementById('name').value;
	var email1=document.getElementById('email').value;
	var pwd1=document.getElementById('pwd').value;
	var cpwd1=document.getElementById('cpwd').value;
	console.log(name1);
	if(name1=="")
	{
		alert("Name should not be blank!");
	}
	else if(email1=="")
	{
		alert("Email should not be blank!");
	}
	else if(pwd1=="")
	{
		alert("Enter a password!");
	}
	else if(cpwd1=="")
	{
		alert("Enter Confirm password!");
	}
	else if(pwd1!=cpwd1)
	{
		alert("Password doesn't match!");
	}
	else{
		window.location.replace("nikal_login.html");
	}
	
}
function submitl()
{
	console.log('hi');
	var name_l=document.getElementById('uname').value;
	var pwd_l=document.getElementById('lpwd').value;
    console.log(name_1);
	if(name_l=="")
	{
		alert("Enter your Username");
	}
}
