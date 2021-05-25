import smtplib
from email.message import EmailMessage

import settings


def notify(uploaded_files):
    buff = []
    for stem, files in uploaded_files.items():
        buff.append('<p>')
        buff.append(f'<b>{stem}</b><br>')
        for file, url in files:
            buff.append(f'<a href="{url}">{file}</a><br>')
        buff.append('</p>')
    uploaded_files = '\n'.join(buff)
    subject = '📊 Actualización de datos SIEMAC'
    content = f'''<p>Hola,</p>
<p>Se ha realizado la subida de datos SIEMAC tras el scraping a EUROSTAT y su posterior
procesamiento.</p>
<p>Relación de ficheros con sus URLs de descarga:</p>

{uploaded_files}

Saludos,<br>
El equipo de informática.
'''

    msg = EmailMessage()
    msg.set_content(content, subtype='html')
    msg['Subject'] = subject
    msg['From'] = settings.NOTIFICATION_FROM_ADDR
    msg['To'] = settings.NOTIFICATION_TO_ADDRS

    s = smtplib.SMTP(settings.SMTP_SERVER, port=settings.SMTP_PORT)
    s.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
    s.send_message(msg)
    s.quit()
