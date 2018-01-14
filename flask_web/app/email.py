import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from threading import Thread
from flask import current_app, render_template
# 项目原代码，使用flask-mail
# from flask_mail import Message
from . import mail


# 项目原代码，使用flask-mail
# def send_async_email(app, msg):
#     with app.app_context():
#         mail.send(msg)
#
# def send_email(to, subject, template, **kwargs):
#     app = current_app._get_current_object()
#     msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
#                   sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
#     msg.body = render_template(template + '.txt', **kwargs)
#     msg.html = render_template(template + '.html', **kwargs)
#     thr = Thread(target=send_async_email, args=[app, msg])
#     thr.start()
#     return thr

#  版本1,使用SMTP和Message，(成功,但是只能给QQ邮箱发邮件，例如163就会报错)
def send_async_email(app, msg, to):
    with app.app_context():
        mail.login(app.config['FLASKY_MAIL_SENDER'], app.config['MAIL_PASSWORD'])
        try:
            mail.sendmail(app.config['FLASKY_MAIL_SENDER'], to, msg)
        except Exception as exc:
            sys.exit("send failed!")
        finally:
            mail.quit()

def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg_body = render_template(template + '.txt', **kwargs)
    msg_html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg_body, to])
    thr.start()
    return thr

# 版本2,使用SMTP和MIMEMultipart、MIMEText，(抛异常)
# def send_async_email(app, msg, to):
#     with app.app_context():
#         mail.login(app.config['FLASKY_MAIL_SENDER'], app.config['MAIL_PASSWORD'])
#         try:
#             mail.sendmail(app.config['FLASKY_MAIL_SENDER'], to, msg)
#         except Exception as exc:
#             print('error !')
#             sys.exit("send failed !")
#         finally:
#             mail.quit()
#
# def send_email(to, subject, template, **kwargs):
#     app = current_app._get_current_object()
#
#     body = render_template(template + '.txt', **kwargs)
#     msg = MIMEText(body, 'plain', 'utf-8')
#
#     msg['From'] = 'k_ling'
#     msg['Subject'] = app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
#     msg['To'] = 'px-zero'
#
#     thr = Thread(target=send_async_email, args=[app, msg, to])
#     thr.start()
#     return thr
