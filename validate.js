function emailValidate(email) {
	var emailRegex = /[A-Za-z0-9.]+@[A-Za-z.]+\.[A-Za-z]+/
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
	if (emailValidate(document.getElementByName('email'))) {
		if (passwordValidate(document.getElementsByName(password))) {
			if (document.getElementsByName('password') == document.getElementsByName(psw2)) {
				document.getElementByName('signup').submit();
			}
		}
	}
}
