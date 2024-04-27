import mailbox
import email
import random

# This script selects a random Quack Of The Hour (qoth)

mb=mailbox.Maildir('~/iamaduck/mail/INBOX')
qmb=mailbox.Maildir('~/iamaduck/mail/qoth')
mb.colon = '!' # makes the maildir Windows compatible
qmb.colon = '!'
msg=random.choice(mb.values())
raw_subject = msg['subject']
decoded_subject = email.header.decode_header(raw_subject)
re_encoded_subject = email.header.make_header(decoded_subject)
subject = str(re_encoded_subject)
# The following line removes newlines (\r\n) sometimes present in long subjects
q = ''.join(subject.splitlines())
print("new quoth: ", q)
qmb.clear()
qmb.add(msg)