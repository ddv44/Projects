function required() {
            var user = document.forms["loginform"]["uname"].value;
            var pass = document.forms["loginform"]["upass"].value;

            if (user === "tri" && pass === "voo") {
                alert("Successful Login");
		setTimeout(function () {
            window.location.href = "Homepageindex.html";
        }, 10); 
            } else {
                alert("Failure Login");
            }
        }
