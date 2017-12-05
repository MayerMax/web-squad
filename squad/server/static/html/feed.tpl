<!DOCTYPE html>
<html>
<head>
	<title>feed</title>
	<meta charset="UTF-8">
	<link rel="shortcut icon" type="image/png" href="../resources/manager.png"/>
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
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
					<img src="{{post[2]}}", width="100%">
					<div class="w3-container title">
						<div class="w3-indigo">
							<h3>{{post[0]}}</h3>
						</div>
					</div>
					<div class="w3-container text">
						<p>{{post[1]}}</p>
					</div>
					<div class="w3-container comments">
						<p> Left: 0 comments</p>
						<button id="show">Show Discussion</button>
						<button id="hide">Hide Discussion</button>
						<div class="w3-container comments-content">
							<ul class="w3-ul w3-margin-bottom w3-hoverable">
								<li>
									<div class="w3-right">0<i class="fa fa-heart" aria-hidden="true"></i>0<i class="fa fa-pencil" aria-hidden="true"></i></div>
									<p>He Said</p>
									<p>Классная статья, понравилось!</p>
								</li>
								<li>
									<p>He Said</p>
									<p>Норм!</p>
								</li>
							</ul>
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
	$(document).ready(function(){
    $("#hide").click(function(){
        $(".comments-content").hide(500);
    });
    $("#show").click(function(){
        $(".comments-content").show(500);
    });
});
</script>
</html>