function emailValidate(email) {
	var emailRegex = /[A-Za-z0-9.]+@[A-Za-z.]+\.[A-Za-z]+/
	console.log(emailRegex.test(email));
	return emailRegex.test(email);
}

function passwordValidate(password) {
	var passwordRegex = /[A-Za-z0-9]+/
	if (passwordRegex.test(password)) {
		if (length(password)) {
			return true;
		}
	}
	return false;
}

function valid() {
	console.log("VALID");
	if (emailValidate(document.getElementByName('email')) == true) {
		console.log("EMAIL");
		if (passwordValidate(document.getElementsByName(password))) {
			console.log("PASSWORD V");
			if (document.getElementsByName('password') == document.getElementsByName(psw2)) {
				console.log("PWS");
				document.getElementByName('signup').submit();
			} else {
				document.getElementByName('errordiv').innerHTML = "Passwords do not match.";
			}
		} else {
				document.getElementByName('errordiv').innerHTML = "Password does not meet requirements";
		}
	} else {
		console.log("EMAIL WRONG");
				document.getElementByName('errordiv').innerHTML = "Email is not a valid format.";
	}
}
