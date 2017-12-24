<?xml version="1.0" encoding="UTF-8"?>
<posts>
	%for id, post in posts.items():
		<post>
			<id>{{id}}</id>
			<title>{{post.get('title')}}</title>
			<img>{{post.get('img')}}</img>
			<text>{{post.get('text')}}</text>
			<comments>
				%for com in post.get('comments'):
				    <comment>
                        <id>{{com[0]}}</id>
                        <who>{{com[3]}}</who>
                        <when>{{com[2]}}</when>
                        <text>{{com[1]}}</text>
                    </comment>
				%end
			</comments>
		</post>
	%end
</posts>