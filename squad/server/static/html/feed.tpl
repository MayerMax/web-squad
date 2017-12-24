<!DOCTYPE html>
<html>
<head>
	<title>feed</title>
	<meta charset="UTF-8">
	<link rel="shortcut icon" type="image/png" href="../resources/manager.png"/>
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
	<link rel="stylesheet" type="text/css" href="../styles/feed.css">
	<style type="text/css">
				.modal {
		    display: none; /* Hidden by default */
		    position: fixed; /* Stay in place */
		    z-index: 1; /* Sit on top */
		    padding-top: 100px; /* Location of the box */
		    left: 0;
		    top: 0;
		    width: 100%; /* Full width */
		    height: 100%; /* Full height */
		    overflow: auto; /* Enable scroll if needed */
		    background-color: rgb(0,0,0); /* Fallback color */
		    background-color: rgba(0,0,0,0.9); /* Black w/ opacity */
	}

	.modal-content {
    background-color: #fefefe;
    margin: 15% auto; /* 15% from the top and centered */
    padding: 20px;
    border: 1px solid #888;
    width: 80%; /* Could be more or less, depending on screen size */
}

.xml {
	cursor: pointer;
	text-decoration: none;
}

	</style>
</head>

<body onkeydown="close_windows(event)" onload="style_images()">
	<div class="w3-top">
  		<div class="w3-bar w3-white w3-wide w3-padding w3-card">
    		<a href="/" class="w3-bar-item w3-button"><b> Squad Feed </b>{{name}}</a>
    		<div class="w3-right w3-hide-small">
    			<a id='xml' onclick="download_xml(event)">
    				<span>Export Comments<i class="fa fa-download" aria-hidden="true"></i></span>
    			</a>
    			<form style="display: inline-block;" action="/stat" method="GET">
    				<button class="w3-btn w3-green w3-hover-light-grey" type="submit">Statistics</button>
    			</form>
    			<form style="display: inline-block;" action="/logout" method="GET">
    				<button class="w3-btn w3-yellow w3-hover-light-grey" type="submit">Log Out</button>
    			</form>
      			
    		</div>
  		</div>
	</div>
	%for post in posts:
		<div class="w3-row" style="margin-top: 100px;">
			<div class="w3-col s2 w3-center"><p> </p></div>
			<div class="w3-col s8">
				<div class="w3-card">
					<img src="{{post[3]}}", width="100%">
					<div class="w3-container title">
						<div class="w3-indigo">
							<h3>{{post[1]}}</h3>
						</div>
					</div>
					<div class="w3-container text">
						<p>{{post[2]}}</p>
					</div>
					<div class="w3-container comments">
						<button onclick="show(event)">Show Discussion</button>
						<button  onclick="hide(event)">Hide Discussion</button>
						
						<div class="w3-container comments-content">
							<ul class="w3-ul w3-margin-bottom w3-hoverable sup">
								%for comment in post[4]:
									<li>
										<div class="w3-right">
											{{!'<i class="fa fa-pencil" onclick="show_editions(event)"></i>' if name == comment[3] else ""}}
											<div class="modal">
												<div class="modal-content">
													<ul class="w3-ul w3-margin-bottom w3-hoverable">
														<h3 style="text-align: center;">Ваши правки к данному комментарию !</h3>
														%for edit in comment[4]:
															<li>
																<p>You said at {{edit[1]}}</p>
																<p>{{edit[2]}}</p>
															</li>
														%end
													</ul>
													<p>Edit Last Comment</p>
													<form action="/com/comment{{comment[0]}}" method="post" enctype="multipart/form-data">
														<textarea rows="4" cols="50" name="edition"> {{comment[2]}}</textarea>
														<input value='Send' type="submit" name="comm">
													</form>
												</div>
											</div>
										</div>
										<p>{{comment[3]}} said at {{comment[1]}}:</p>
										<p>{{comment[2]}}</p>
									</li>
								%end
							</ul>
							<div class="leave-comment">
									<textarea rows="4" cols="50" name="comment" placeholder="{{name}} Leave a reply..." style="display: block;"></textarea>
									<button name="{{name}}" class="w3-btn w3-indigo w3-hover-light-grey" id='thread{{post[0]}}' type="submit" onclick="send(event)" style="margin-bottom: 15px; margin-top: 15px;">Send</button>
								</form>
							</div>
						</div>
					</div>
				</div>
			</div>
			<div class="w3-col s2 w3-center"><p> </p></div>
		</div>
	%end 
</body>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
<script src="../scripts/ajax.js"></script>
<script type="text/javascript">

function send(event) {
	var textarea = event.target.previousElementSibling;
	ajax.post('/thr/' + event.target.id, {comment: textarea.value}, 

		function(response) {
			textarea.value = '';
			get_update();

		})

}


function get_update() {
	ajax.get('/upd', {}, function(response) {
		var result = JSON.parse(response);
		var posts = document.getElementsByClassName('sup');

		keys = Object.keys(result)
		console.log(keys);
		for (var i = 0; i < keys.length; i++) {
			var key = parseInt(keys[i]) - 1;
			var post = posts[key];
			if (post.children.length == 0) {
				post.insertAdjacentHTML('beforeend', result[keys[i]])
			}
			else {
			var last_comment = post.children[post.children.length - 1];
			last_comment.insertAdjacentHTML('afterend', result[keys[i]])
			}
		}
	})
}

setInterval(get_update, 5000);

function show(event) {
		var parent = event.target.parentElement;
		var child = parent.getElementsByClassName('comments-content')[0];
		$(child).show(500);
	}

	function hide(event) {
		var parent = event.target.parentElement;
		var child = parent.getElementsByClassName('comments-content')[0];
		$(child).hide(500);
	};

	function convert(event) {
		event.target.textarea.value = unescape(encodeURIComponent(event.target.textarea.value));
	}

	function show_editions(event) {
		event.target.nextElementSibling.style.display = 'block';
	}

	function close_windows(event) {
		var modals = document.getElementsByClassName('modal');
		if (event.keyCode == 27) {
		for (var i=0; i < modals.length; i++)
			modals[i].style.display = 'none';
		}
	}

	function style_images()  {
		$('p img').css('width: 100%');
		$('p img').prop("alt", "Player");
		$('p img').wrap('<div class="w3-card" style="max-height: 400px; max-width: 400px;"></div>')
	}

	function download_xml(event) {
		ajax.get('/load_xml', {}, function(response) {
			$('#xml').attr('href', response);
			$("#xml").attr("download", response);
		}, false);
		// document.getElementById('xml').click()
		
	}

</script>
</html>