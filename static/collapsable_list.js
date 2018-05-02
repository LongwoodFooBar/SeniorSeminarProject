/*Code adapted from code found at https://www.w3schools.com/howto/howto_js_topnav.asp*/

var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
	coll[i].addEventListener("click", function() {
	this.classList.toggle("active");
	var content = this.nextElementSibling;
	if (content.style.display === "block") {
		content.style.display = "none";
	} 
	else {
		content.style.display = "block";
	}
});
}	

var coll = document.getElementsByClassName("Profcollapsible");
var i;

for (i = 0; i < coll.length; i++) {
	coll[i].addEventListener("click", function() {
	this.classList.toggle("active");
	var content = this.nextElementSibling;
	if (content.style.display === "block") {
		content.style.display = "none";
	} 
	else {
		content.style.display = "block";
	}
});
}	

var coll = document.getElementsByClassName("memcollapsible");
var i;

for (i = 0; i < coll.length; i++) {
	coll[i].addEventListener("click", function() {
	this.classList.toggle("active");
	var content = this.nextElementSibling;
	if (content.style.display === "block") {
		content.style.display = "none";
	} 
	else {
		content.style.display = "block";
	}
});
}


