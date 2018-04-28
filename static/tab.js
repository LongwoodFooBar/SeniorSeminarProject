var textareas = document.getElementById('code');
//textareas.value = "HELLO, WORLD!";
textareas.onkeydown = function(e){
	if(e.keyCode==9 || e.which==9){
		e.preventDefault();
		var s = this.selectionStart;
		this.value = this.value.substring(0,this.selectionStart) + "\t" + this.value.substring(this.selectionEnd);
		this.selectionEnd = s+1; 
	}
}
//UPLOAD CODE STARTS HERE
var modal = document.getElementById('myModal');
// Get the button that opens the modal
var btn = document.getElementById("prompt");
// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];
// When the user clicks the button, open the modal 
btn.onclick = function() {
	modal.style.display = "block";
}
// When the user clicks on <span> (x), close the modal
span.onclick = function() {
	modal.style.display = "none";
}
// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
	if (event.target == modal) {
		modal.style.display = "none";
	}
}