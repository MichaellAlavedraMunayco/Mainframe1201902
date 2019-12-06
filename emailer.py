import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

graphs = [
    'https://plot.ly/~MichaellAlavedraMunayco/10',
    'https://plot.ly/~MichaellAlavedraMunayco/8',
    'https://plot.ly/~MichaellAlavedraMunayco/6',
    'https://plot.ly/~MichaellAlavedraMunayco/4'
]


def email_template(graph_url, caption=''):
    template = (''
                '<a href="{graph_url}" target="_blank"><img src="{graph_url}.png"></a>'
                '{caption}'
                '<br>'
                '<a href="{graph_url}" style="font-weight: 200;" target="_blank">Visualizar y comentar Grafico interactivo</a>'
                '<br>'
                '<hr>'
                '')
    return template.format(graph_url=graph_url, caption=caption)


def build_email():
    email_body = ''
    for graph in graphs:
        email_body += email_template(graph, caption='')
    return email_body


def send_email(sender_email_password, receiver_email_address):
    me = 'f.michaell.a.m@gmail.com'
    recipient = receiver_email_address  # wfloresn1@upao.edu.pe
    subject = 'Reporte metropolitano'

    email_server_host = 'smtp.gmail.com'
    port = 587
    email_username = me
    email_password = sender_email_password

    msg = MIMEMultipart('alternative')
    msg['From'] = me
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(build_email(), 'html'))

    server = smtplib.SMTP(email_server_host, port)
    server.ehlo()
    server.starttls()
    server.login(email_username, email_password)
    server.sendmail(me, recipient, msg.as_string())
    server.close()
