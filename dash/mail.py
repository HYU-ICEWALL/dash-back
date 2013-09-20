import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from conf import admin_email

def sendmail(dest, subject, message):
	msg = MIMEMultipart('alternative')
	msg['Subject'] = subject
	msg['From'] = admin_email
	msg['To'] = dest

	s = smtplib.SMTP('localhost')
	part1 = MIMEText(message, 'plain')
	part2 = MIMEText(message, 'html')
	msg.attach(part1)
	msg.attach(part2)
	
	s.sendmail(admin_email, dest, msg.as_string())
	s.quit()

