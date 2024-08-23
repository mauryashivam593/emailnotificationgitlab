import argparse, os
import logging
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from pathlib import Path

FORMAT = '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

COMMASPACE = ', '
SMTP_HOST = 'smtp.in.here.com'
SEND_FROM = 'gitlab-pipeline@here.com'


def parse_arguments():
    parser = argparse.ArgumentParser(description='Send an email')
    parser.add_argument('--smtp-host', type=str, help='SMTP host',
                        default=SMTP_HOST)
    parser.add_argument('--send-from', type=str, help='E-mail author',
                        default=SEND_FROM)
    parser.add_argument('--subject', type=str, help='E-mail subject',
                        required=True)
    parser.add_argument('--send-to', nargs='+', type=str,
                        help='E-mail recipient(s)', required=True)
    parser.add_argument('--send-cc', nargs='+', type=str,
                        help='E-mail recipient(s)')
    parser.add_argument('--message', type=str, help='E-mail body', required=True)
    parser.add_argument('--attach', nargs='*', type=str,
                        help='List of paths to attachments')
    return parser.parse_args()


def send_mail(send_from, send_to, send_cc, subject, message, smtp_host='localhost',
              files=[]):
    """Compose and send email with provided info and attachments.

    Args:
        send_from (str): from name
        send_to (list[str]): to name(s)
        send_cc (list[str]): to name(s)
        subject (str): message title
        message (str): message body
        files (list[str]): list of file paths to be attached to email
        smtp_host (str): mail server host name
    """

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Cc'] = COMMASPACE.join(send_cc)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'html'))

    for path in files:
        part = MIMEBase('application', 'octet-stream')
        with open(path, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename="{}"'.format(Path(path).name))
        msg.attach(part)

    email_list = send_to + send_cc
    smtp = smtplib.SMTP(smtp_host)
    smtp.sendmail(send_from, email_list, msg.as_string())
    smtp.quit()


if __name__ == '__main__':
    args = parse_arguments()

    if os.path.isfile(args.message):
        html_file=args.message
        f = open(html_file, 'r')
        msg=f.read()
        f.close()
    else:
        msg=args.message

    send_mail(
        send_from=args.send_from,
        send_to=args.send_to,
        send_cc=args.send_cc,
        subject=args.subject,
        message=msg,
        smtp_host=args.smtp_host,
        files=args.attach or []
    )
    logger.info('An email from "%s" with the message "%s" and attached files:'
                ' %s was successfully sent to %s and cc %s',
                args.send_from,
                args.message,
                args.attach or [],
                args.send_to,
                args.send_cc)

