html = """<!DOCTYPE html>
<html>

<head>
<title>PyMail</title>
<style>
a.header:link {{
    color: black;
	text-decoration: none;
}}
a.header:visited {{
    color: black;
}}
a.header:hover {{
    color: blue;
}}
</style>
</head>
<body bgcolor="#E6E6FA">

<table style="width: 100%;" bgcolor="#AAAAFF">
<tbody>
<tr><td><h1><a class="header" href="http://github.com/bismarckjunior/pymail">PyMail</a>: E-mail Verification</h1></td>
<td style="text-align: right;"><h1>{0}/{1}</h1></td></tr>
</tbody>
</table>

<br>

<button onclick="location.href='{2}'" type="button" {3}>|<</button>
<button onclick="location.href='{4}'" type="button" {5}><</button>
<label for="name" onclick="location.href='{6}'">{0}/{1}</label>
<button onclick="location.href='{7}'" type="button" {8}>></button>
<button onclick="location.href='{9}'" type="button"{10}>>|</button>

<br><br>

<table style="border-collapse: collapse; width: 100%;" border="1">
<tbody>
<tr><td style="width: 10%;">Subject:		</td><td>{11}</td></tr>
<tr><td style="width: 10%">From:			</td><td>{12}</td></tr>
<tr><td style="width: 10%">To:				</td><td>{13}</td></tr>
<tr><td style="width: 10%">Cc:				</td><td>{14}</td></tr>
<tr><td style="width: 10%">Bcc				</td><td>{15}</td></tr>
<tr><td style="width: 10%">Attachments:		</td><td>{16}</td></tr>
<tr><td style="width: 10%" valign="top">Message:</td>
	<td style="padding-top: 10px;">{17}<br></td>
</tr>
</tbody>
</table>

</body>
</html>
"""