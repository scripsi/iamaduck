# import lots of necessary stuff
import config
from PIL import Image,ImageDraw,ImageFont
import random
import math
import mailbox
import email
import os

LEADING = 2
MARGIN = 20

img = Image.new(mode='P',size=(config.WIDTH,config.HEIGHT), color=config.WHITE)
img_draw = ImageDraw.Draw(img)

fonts_dir = "/home/anas/iamaduck/assets/fonts"

# colour schemes (background,foreground)
colours = [(config.BLACK,config.WHITE),(config.BLACK,config.YELLOW),(config.BLACK,config.ORANGE),
           (config.WHITE,config.BLACK),(config.WHITE,config.GREEN),(config.WHITE,config.BLUE),(config.WHITE,config.RED),
           (config.GREEN,config.WHITE),(config.GREEN,config.YELLOW),
           (config.BLUE,config.WHITE),(config.BLUE,config.YELLOW),(config.BLUE,config.ORANGE),
           (config.RED,config.WHITE),(config.RED,config.YELLOW),
           (config.YELLOW,config.BLACK),(config.YELLOW,config.GREEN),(config.YELLOW,config.BLUE),(config.YELLOW,config.RED),
           (config.ORANGE,config.BLACK),(config.ORANGE,config.BLUE)]


def get_image():
    """Returns an image to be displayed on the screen
    """

    quack = get_random_quack()
    font = get_random_font()
    bg,fg = random.choice(colours)

    fs,q = smoosh_text(quack, font, config.WIDTH - (MARGIN * 2), config.HEIGHT - (MARGIN * 2))
    output_font = ImageFont.truetype(font, fs)

    ax, ay, bx, by = img_draw.multiline_textbbox((0,0),q,font=output_font,align="center",spacing=LEADING)
    x = ((config.WIDTH - (bx - ax)) / 2) - ax
    y = ((config.HEIGHT - (by - ay)) / 2) - ay
    img_draw.rectangle([0,0,config.WIDTH,config.HEIGHT],fill=bg)
    img_draw.multiline_text((x,y),q,fill=fg,font=output_font,spacing=LEADING,align="center")

    return img

def get_random_quack():
    """Returns a random quack from messages in a mailbox
    """

    mb=mailbox.Maildir('~/iamaduck/mail/INBOX')
    mb.colon = '!' # makes the maildir Windows compatible
    msg=random.choice(mb.values())
    raw_subject = msg['subject']
    decoded_subject = email.header.decode_header(raw_subject)
    re_encoded_subject = email.header.make_header(decoded_subject)
    subject = str(re_encoded_subject)
    # The following line removes newlines (\r\n) sometimes present in long subjects
    q = ''.join(subject.splitlines())
    
    return q

def get_random_font():
    """Returns a random font from a series of font files in subdirectories
    """

    font_dir = random.choice([d.path for d in os.scandir(fonts_dir) if d.is_dir()])
    font = os.path.join(font_dir,[f for f in os.listdir(font_dir) if f.endswith(".ttf")][0])

    return font


def smoosh_text(text, font_name, box_width, box_height):
    """Wraps, centres and shrinks a text string to fit a rectangular image area
    """
    # Create a font instance for testing, at size 100
    test_font = ImageFont.truetype(font_name, 100)
    # Find the width of a space
    ax, ay, bx, by = img_draw.textbbox((0,0),' ',font=test_font,spacing=0)
    space_width = bx - ax
    # split the text into individual words
    words = text.split()
    # Find the biggest words
    # print("Word size optimisation ...")
    word_width_max = 0
    word_height_max = 0
    word_width_total = 0
    for w in words:
        ax, ay, bx, by = img_draw.textbbox((0,0),w,font=test_font,spacing=0)
        w_width = bx - ax
        word_width_total += w_width
        w_height = by - ay
        if w_width > word_width_max:
            word_width_max = w_width
            widest_word = w
        if w_height > word_height_max:
            word_height_max = w_height
            tallest_word = w
    # print("Widest word is: ", widest_word)
    # print("Tallest word is: ", tallest_word)

    # Set the maximum font size so that the biggest words will fit
    font_size = math.floor((box_width / (word_width_max/100)))
    font_size = math.floor(min(font_size, (box_height / (word_height_max/100))))
    # print("First round font size is: ", font_size)

    # Now set the maximum font size so that the total area occupied by the text fits the area available
    # print("Area optimisation ...")
    box_area = box_width * box_height
    unit_text_width = ((len(words)-1) * (space_width / 100)) + (word_width_total / 100)
    unit_line_height = word_height_max / 100
    unit_text_area = unit_text_width * unit_line_height
    font_size = math.floor(min(font_size,math.sqrt(box_area / unit_text_area)))
    # print("Second round font size is: ", font_size)

    # Finally, try and find the maximum font size where the text actually fits
    # print("Line length optimisation ...")
    unfitted = True
    lines = []
    while unfitted:
        # print("Trying font size: ", font_size, "...")
        line_height = (unit_line_height * font_size) + LEADING
        display_font = ImageFont.truetype(font_name, font_size)
        lines.clear()
        line = ''
        for w in words:
            if line == '':
                l = w
            else:
                l = line + ' ' + w
            ax, ay, bx, by = img_draw.textbbox((0,0),l,font=display_font,spacing=0)
            line_width = bx - ax
            if line_width > box_width:
                lines.append(line)
                line = w
            else:
                line = l
        if line != '':
            lines.append(line)
        ax, ay, bx, by = img_draw.multiline_textbbox((0,0),"\n".join(lines),font=display_font,align="center",spacing=LEADING)
        if by - ay > box_height:
            # print("Too big.")
            font_size -= 1
        else:
            # print("It fits!")
            unfitted = False

    # print("Third round font size is: ", font_size)
    # for l in lines:
    #   print(l)

    return font_size, "\n".join(lines)
