from string import Template
from .ccavutil import encrypt,decrypt
from decouple import config
def res(encResp):
    workingKey = config('WORKING_KEY')
    decResp = decrypt(encResp,workingKey)
    data = '<table border=1 cellspacing=2 cellpadding=2><tr><td>'	
    data = data + decResp.replace('=','</td><td>')
    data = data.replace('&','</td></tr><tr><td>')
    data = data + '</td></tr></table>'
    html = '''\
	<html>
		<head>
			<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
			<title>Response Handler</title>
		</head>
		<body>
			<center>
				<font size="4" color="blue"><b>Response Page</b></font>
				<br>
				$response
			</center>
			<br>
			
		</body>
	</html>
	'''
    fin = Template(html).safe_substitute(response=data)
    return fin
