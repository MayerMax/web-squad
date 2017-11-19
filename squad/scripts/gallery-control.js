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

function openWindow(event) {
  var pos = g.association[event.target.id];
  var imgObj = g.elements[pos];
  var neighbours = g.getNeighbours(pos);
  
  document.getElementById('window').style.display = "block";

  var wide = document.getElementById('wide-image');
  wide.src = imgObj.src;

}

function closeWindow() {
  document.getElementById('window').style.display = "none";
}

function saveClose(event) {
	if (document.getElementById('window').style.display == 'block') {
		if (event.keyCode == 27)
			closeWindow();
	} 
}