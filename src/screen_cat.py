import config
import io
import mailbox
import email
import random
from PIL import Image

def get_image():
    """Returns an image to be displayed on the screen
    """
    
    mb=mailbox.Maildir('~/iamaduck/mail/scp')
    mb.colon = '!' # makes the maildir Windows compatible
    msg=random.choice(mb.values())
    for part in msg.walk():
        if part.get_content_type() == "image/png":
            attachment = io.BytesIO(part.get_payload(decode=True))
    img = Image.open(attachment)

    return img
    
