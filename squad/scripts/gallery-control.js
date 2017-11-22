function Gallery() {
	this.elements = document.getElementsByClassName('hover-shadow');

	this.association = {};
	for (var i=0; i < this.elements.length; i++) {
		this.association[this.elements[i].id] = i;
	}

	this.getNeighbours = function(pos){
		if (pos < 0 || pos >= this.elements.length)
			throw 'Troubleshooting case';
		if (pos == 0)
			return [this.elements[this.elements.length- 1], this.elements[1]]
		if (pos == this.elements.length - 1)
			return [this.elements[pos - 1], this.elements[0]]
		return [this.elements[pos -1], this.elements[pos + 1]]
	}


}



var g = new Gallery();
var documentation = false;
var view = false;
var global_position = 0;
init();

function openWindow(event) {
  var pos = g.association[event.target.id];
  var imgObj = g.elements[pos];
  //var neighbours = g.getNeighbours(pos);
  
  global_position = pos;
  view = true;  
  document.getElementById('window').style.display = "block";

  var wide = document.getElementById('wide-image');
  wide.src = imgObj.src;

}

function eventHandler(event) {
	if (event.keyCode == 112 && !documentation) {
		documentation = true;
		actOnDocumentation(documentation);
		return;
	}
	if (event.keyCode == 27 && documentation) {
		documentation = false;
		actOnDocumentation(documentation);
		return;
	}

	if (event.keyCode == 27 && view) {
		view = false;
		closeWindow();
		return;
	}

	if (event.keyCode == 37 && view) {
		nextPicture(-1);
		return;
	}

	if (event.keyCode == 39 && view) {
		nextPicture(1);
		return;
	}


}

function closeWindow() {
  document.getElementById('window').style.display = "none";
  
}

function actOnDocumentation(state) {
	if (state == true)
		document.getElementById('documentation').style.display = "block";
	else
		document.getElementById('documentation').style.display = "none";
}

function nextPicture(direction) {
	var neighbours = g.getNeighbours(global_position);
	var imgObj = direction > 0 ? neighbours[1] : neighbours[0];

	var wide = document.getElementById('wide-image');
  	wide.src = imgObj.src;

  	global_position += direction;
  	if (global_position < 0)
  		global_position = g.elements.length -1;
  	if (global_position >= g.elements.length)
  		global_position = 0;
}



function init() {
	var photoCache = retrieveCoookie('index');
	if (photoCache != null) {
		global_position = parseInt(photoCache.value);
		view = true;
		var imgObj = g.elements[global_position];
  		document.getElementById('window').style.display = "block";
  		var wide = document.getElementById('wide-image');
  		wide.src = imgObj.src;
  		// needs image loading effect
	}
}

window.onbeforeunload = function reloading() {
	if (view) {
		createCookie('index', global_position);
	}
	else {
		if (retrieveCoookie('index') != null)
			deleteCookie('index');
	}
}


function btnclick() {
	if (retrieveCoookie('theme') != null)
		deleteCookie('theme');

	createCookie('theme', g.elements[global_position].src);

}


