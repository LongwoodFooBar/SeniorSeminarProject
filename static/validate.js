function emailValidate(email) {
	var emailRegex = /[A-Za-z0-9.]+\@[A-Za-z.]+\.[A-Za-z]+/;
	console.log(emailRegex.test(email));
	console.log(email);
	return emailRegex.test(email);
}

function passwordValidate(password) {
	var passwordRegex = /[A-Za-z0-9]+/;
	if (passwordRegex.test(password)) {
		if (password.length >= 8) {
			return true;
		}
	}
	return false;
}

function valid() {
	console.log("VALID");
	if (emailValidate(document.getElementsByName('email')[0].value) == true) {
		if (passwordValidate(document.getElementsByName('password')[0].value)) {
			console.log("PASSWORD V");
			if (document.getElementsByName('password')[0].value == document.getElementsByName('psw2')[0].value) {
				console.log("PWS");
				document.getElementsByName('signup')[0].submit();
			} else {
				document.getElementsByName('errordiv')[0].innerHTML = "Passwords do not match.";
			}
		} else {
				document.getElementsByName('errordiv')[0].innerHTML = "Password does not meet requirements. Must Contain at least 8 characters.";
		}
	} else {
		console.log("EMAIL WRONG");
				document.getElementsByName('errordiv')[0].innerHTML = "Email is not a valid format.";
	}
}
