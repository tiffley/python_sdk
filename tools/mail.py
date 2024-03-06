from email.mime.text import MIMEText
from email.utils import formatdate
import smtplib
from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart

# setting edit here ----------------------------------------------------
To = ['takaakira.yamauchi@xxx.com']  # if you want multiple, create list
CC = ['']  # optional. If this is not required, just pass empty string
BCC = ['']  # optional.

Subject = 'test'

fn = ''  # optional. path to your file to attach

From = 'takaakira.yamauchi@xxx.com'  # your email addr
# ----------------------------------------------------
# edit here for content
def body():
    txt = 'Hi xxxxxx'
    txt = txt + '\n\n'
    txt = txt + 'hello'
    txt = txt + '\n'
    txt = txt + 'xxxxxxxxxxxx'
    txt = txt + '\n\n'
    txt = txt + 'Best regards,'
    txt = txt + '\n'
    txt = txt + 'xxxxxxxxx'
    return txt


def create_message(from_addr, to_addr, subject, body, cc_addr='', bcc_addr=''):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Cc'] = cc_addr
    msg['Bcc'] = bcc_addr
    msg['Date'] = formatdate()
    msg.attach(MIMEText(body))
    return msg

def attach_file(msg, fn):
    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(fn, "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(fn))
    msg.attach(part)
    return msg


if __name__ == '__main__':
    body = body()
    msg = create_message(From, ','.join(To), Subject, body, ','.join(CC), ','.join(BCC))
    if fn != '':
        print('attach mode')
        msg = attach_file(msg, fn)

    li = []
    li.extend(To)
    li.extend(CC)
    li.extend(BCC)

    smtpobj = smtplib.SMTP('mgs.intra.xxx.co.jp', 25)
    smtpobj.sendmail(From, li, msg.as_string())
    smtpobj.quit()
