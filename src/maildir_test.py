import mailbox
for message in mailbox.Maildir('/mnt/iamaduck/mail/INBOX'):
  subject = message['subject']
  print(subject)
  
