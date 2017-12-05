
function checkLoading() {
	var loading_interval = setInterval(function(){
	var items = document.getElementsByClassName('spinner');
	for (var i = 0; i < items.length; i++){
		var image = items[i];
		image.setAttribute('src', image.getAttribute('data-src'));
		image.style.width = '100%';
		image.style.marginTop = '0px';
	}
	if (items.length == 0)
		clearInterval(loading_interval);
	}, 1000);
}

function Gallery() {
	this.elements = document.getElementsByClassName('hover-shadow');

	this.association = {};
	this.paths = [];
	this.max_views = [];

	for (var i=0; i < this.elements.length; i++) {
		this.association[this.elements[i].id] = i;
		this.paths[i] = this.elements[i].getAttribute('data-src').replace(/thmb_/gi, '');
		this.max_views[i] = null;
	}

	this.getNeighboursIdx = function(pos){
		if (pos < 0 || pos >= this.elements.length)
			throw 'Troubleshooting case';
		if (pos == 0)
			return [this.elements.length- 1, 1]
		if (pos == this.elements.length - 1)
			return [pos - 1, 0]
		return [pos -1, pos + 1]
	}


}



var g = new Gallery();
var documentation = false;
var view = false;
var global_position = 0;
init();
var d;

function openWindow(event) {
  var id = event.target.id;

  var pos = g.association[id];
  
  
  global_position = pos;
  view = true;

  loadHighQuality(pos);
  initHash(global_position);

}

function eventHandler(event) {
	event.preventDefault();
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
  	var wide = document.getElementById('wide-image');
	wide.style.display = 'none';
  	document.getElementById('window').style.display = "none";
  	document.getElementById('ld').style.display = 'block';
  
}

function actOnDocumentation(state) {
	if (state == true)
		document.getElementById('documentation').style.display = "block";
	else
		document.getElementById('documentation').style.display = "none";
}

function nextPicture(direction) {
	var neighboursIdx = g.getNeighboursIdx(global_position);
	var position = direction > 0 ? neighboursIdx[1] : neighboursIdx[0];
	
	loadHighQuality(position);

  	global_position += direction;
  	if (global_position < 0)
  		global_position = g.elements.length -1;
  	if (global_position >= g.elements.length)
  		global_position = 0;

  	initHash(global_position);
}



function init() {
	var photoCache = retrieveCoookie('index');
	if (photoCache != null) {
		global_position = parseInt(photoCache.value);
		view = true;
		loadHighQuality(global_position);
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

	createCookie('theme', g.max_views[global_position].src);

}

window.onpopstate = function(event) {
	var state = getHash();
	if (state !== "" && !isNaN(state.substring(1))) {
		var pos = parseInt(state.substring(1));
		global_position = pos;
		view = true;
		loadHighQuality(global_position);
		return;
	}

	if (state == '') {
		document.getElementById('window').style.display = "none";
	}
}

//TODO убрать якорь

function loadHighQuality(idx) {
  var path = g.paths[idx];
  var state = checkShowImmediately(idx);
  if (state)
  	return;

  document.getElementById('window').style.display = "block";
  document.getElementById('ld').style.display = 'block';
  var wide = document.getElementById('wide-image');
  wide.style.display = 'none';

  var button = document.getElementById('th-btn');
  button.style.visibility = 'hidden';

  if (g.max_views[idx] == null) {
  		g.max_views[idx] = new Image();
  		g.max_views[idx].src = path;
  }

  var load_int = setInterval(
  	function() {
  		if (g.max_views[idx].complete == true) {
  			wide.src = g.max_views[idx].src;
  			document.getElementById('ld').style.display = 'none';
  			wide.style.display = 'block'; 
  			button.style.visibility = 'visible';
  			smartPreloader(idx);
  			clearInterval(load_int);
  		}
  	}, 500
  	)

}

function checkShowImmediately(idx) {
	if (g.max_views[idx] == null)
		return false;
	var pic = g.max_views[idx]
	if (pic.complete == false || pic.naturalHeight == 0)
		return false;

	document.getElementById('ld').style.display = 'none';
	var wide = document.getElementById('wide-image');
	wide.src = pic.src;
	document.getElementById('window').style.display = "block";
	wide.style.display = 'block';
	smartPreloader(idx);
	return true;

}

function smartPreloader(curr_loading_idx) {
	var next = curr_loading_idx += 1;
	next = next >= g.elements.length ? 0 : next;
	if (next < 0)
		return;
	if (g.max_views[next] == null) {
		var path = g.paths[next];
		g.max_views[next] = new Image();
		g.max_views[next].src = path;
	}
	
}
