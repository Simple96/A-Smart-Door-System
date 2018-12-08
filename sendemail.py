import smtplib

smtpUser = 'hs978xh344@gmail.com'
smtpPass = 'ece5725!'

toAdd='xh344@cornell.edu'
fromAdd = smtpUser

subject = 'Python Test'
header = 'To: ' + toAdd + '\n' + 'From: ' + fromAdd + '\n' + 'Subject: ' + subject
body = 'door is open'

print header + '\n' + body

s = smtplib.SMTP('smtp.gmail.com',587)
s.ehlo()
s.starttls()
s.ehlo()

s.login(smtpUser,smtpPass)
s.sendmail(fromAdd, toAdd, header + '\n' + body)
s.quit()