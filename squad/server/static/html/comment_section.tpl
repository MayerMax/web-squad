%for comment in post:
	<li>
		<div class="w3-right">
			{{!'<i class="fa fa-pencil" onclick="show_editions(event)"></i>' if comment.get('editions') != None else ""}}
			<div class="modal">
				<div class="modal-content">
					<ul class="w3-ul w3-margin-bottom w3-hoverable">
						<h3 style="text-align: center;">Ваши правки к данному комментарию !</h3>
						%if comment.get('editions') != None:
							%for edit in comment.get('editions'):
								<li>
									<p>You said at {{edit[1]}}</p>
									<p>{{edit[2]}}</p>
								</li>
							%end
						%end
					</ul>
					<p>Edit Last Comment</p>
					<form action="/com/comment{{comment.get('id')}}" method="post" enctype="multipart/form-data">
						<textarea rows="4" cols="50" name="edition"> {{comment.get('text')}}</textarea>
						<input value='Send' type="submit" name="comm">
					</form>
				</div>
			</div>
		</div>
		<p>{{comment.get('user')}} said at {{comment.get('date')}}:</p>
		<p>{{comment.get('text')}}</p>
	</li>
%end