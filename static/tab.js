function tab(t, e) {
    if(e.keyCode==9 || e.which==9) {
        e.preventDefault();
        var s = t.selectionStart;
        t.value = t.value.substring(0,t.selectionStart) + "\t" + t.value.substring(t.selectionEnd);
        t.selectionEnd = s + 1;
	}
}
