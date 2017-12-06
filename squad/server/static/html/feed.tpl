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
</head>

<body>
	<div class="w3-top">
  		<div class="w3-bar w3-white w3-wide w3-padding w3-card">
    		<a href="profile.html" class="w3-bar-item w3-button"><b> Squad Feed </b>{{name}}</a>
    		<div class="w3-right w3-hide-small">
      			<a href="#" class="w3-bar-item w3-button w3-red">Personal Room</a>
      			<a href="gallery.html" class="w3-bar-item w3-button">Gallery</a>
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
							<ul class="w3-ul w3-margin-bottom w3-hoverable">
								%for comment in post[4]:

									<li>
										<div class="w3-right">0<i class="fa fa-heart" aria-hidden="true"></i>0<i class="fa fa-pencil" aria-hidden="true"></i></div>
										<p>{{comment[2]}} said:</p> <span> at {{comment[0]}}</span>
										<p>{{comment[1]}}</p>
									</li>
								%end
							</ul>
							<div class="leave-comment">
								<form action="/thread{{post[0]}}" method="POST">
									<textarea rows="4" cols="50" name="comment">{{name}}, Leave a reply...</textarea>
									<input value='Send' type="submit" name="comm" >
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
<script type="text/javascript">
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

</script>
</html>