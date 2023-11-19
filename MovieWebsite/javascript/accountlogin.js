function showinput(){
	var a = document.getElementById("cruname").value;
	var b = document.getElementById("crupass").value;
	var c = document.getElementById("cusfname").value;
	var d = document.getElementById("cuslname").value;

	if ( a == "" && b == "" && c == "" && d == "") {
	alert (" Please provide your log-in information");
	}
	else if( a == "") {
	alert (" Please provide your username");}
	else if( b == "") {
	alert (" Please provide your password");}
	else if( c == "") {
	alert (" Please provide your first name");}
	else if (d == ""){
	alert (" Please provide your last name");
	}
	else{
	alert ("Account created successfully. Welcome" + " " + c + " " + d +"!");

	 setTimeout(function () {
            window.location.href = "loginpage.html";
        }, 10); 
	}
}
	
