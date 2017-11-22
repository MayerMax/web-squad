function createCookie(name, value, daysToExpire=3, path="/") {
	// var d = new Date();
	// d.setTime(d.getTime() + (daysToExpire * 24 * 60 * 60 * 1000));

	// var expires = 'expires=' + d.toUTCString();
	// + expires + ";" + "path=" + path;
	document.cookie = name + "=" + value + ";"; 
}


function retrieveCoookie(name) {
	var cookies = decodeURIComponent(document.cookie);
	var regExp = new RegExp(name +'=([0-9a-zA-z./:-]+);?(expires=([a-zA-Z0-9;,: ]+);?)?(path=([a-zA-Z0-9\/]+))?');
	var match = cookies.match(regExp);
	if (match == null)
		return null;
	return {'value' : match[1], 'expires' : match[2], 'path' : match[3]};
}

function deleteCookie(name) {
	document.cookie = name + "=; expires=Thu, 01 Jan 1970 00:00:01 GMT;";
}