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

	</style>
</head>

<body onkeydown="close_windows(event)">
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
													<form action="/com/comment{{comment[0]}}" method="post">
														<textarea rows="4" cols="50" name="edition"> {{comment[2]}}</textarea>
														<input value='Send' type="submit" name="comm">
													</form>
												</div>
											</div>
										</div>
										<p>{{comment[3]}} said:</p> <span> at {{comment[1]}}</span>
										<p>{{comment[2]}}</p>
									</li>
								%end
							</ul>
							<div class="leave-comment">
								<form action="/thr/thread{{post[0]}}" method="POST">
									<textarea rows="4" cols="50" name="comment" placeholder="{{name}} Leave a reply..."></textarea>
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

	function show_editions(event) {
		event.target.nextElementSibling.style.display = 'block';
	}

	function close_windows(event) {
		var modals = document.getElementsByClassName('modal');
		console.log(1);
		if (event.keyCode == 27) {
		for (var i=0; i < modals.length; i++)
			modals[i].style.display = 'none';
		}
	}

</script>
</html>