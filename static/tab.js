function tab(e) {
	if(e.keyCode==9 || e.which==9){
		e.preventDefault();
		var s = this.selectionStart;
		this.value = this.value.substring(0,this.selectionStart) + "\t" + this.value.substring(this.selectionEnd);
		this.selectionEnd = s+1; 
	}
}

function modalOn() {
	document.getElementById('myModal').style.display = "block";
}

function modalOff() {
	document.getElementById('myModal').style.display = "none"
}

window.onclick = function(event) {
	if (event.target == modal) {
		modal.style.display = "none";
	}
}