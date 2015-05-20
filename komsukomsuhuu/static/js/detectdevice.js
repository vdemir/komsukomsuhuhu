function detectDevice() { 
	if( navigator.userAgent.match(/Android/i)
		|| navigator.userAgent.match(/webOS/i)
		|| navigator.userAgent.match(/iPhone/i)
		|| navigator.userAgent.match(/iPad/i)
		|| navigator.userAgent.match(/iPod/i)
		|| navigator.userAgent.match(/BlackBerry/i)
		|| navigator.userAgent.match(/Windows Phone/i)){
			document.getElementById("detect-device-mobile").style.display = "block";
	}
	else {
			document.getElementById("detect-device-mobile").style.display = "none";
	}
}