// ben and tyler 
function pasSame(){ 
	
	var one=document.getElementById("P1").value; 
	var two=document.getElementById("P2").value;
	 if(one != two){
		document.getElementByName("errordiv").innerHTML = "Passwords not the same";
	}
}	

