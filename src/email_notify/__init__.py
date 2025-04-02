import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import click
from dotenv import load_dotenv


def send_email(
    from_addr: str, to_addr: str, subject: str, body: str, env_file: str | None = None
) -> None:
    if env_file:
        load_dotenv(dotenv_path=env_file)
    elif Path('.env').exists():
        load_dotenv()
    elif Path.home().joinpath('.email_notify.env').exists():
        load_dotenv(dotenv_path=Path.home().joinpath('.email_notify.env'))
    else:
        raise ValueError('cannot locate .env file with SMTP config')

    smtp_server = os.environ.get('SMTP_SERVER')
    smtp_port = int(os.environ.get('SMTP_PORT', '587'))
    smtp_username = os.environ.get('SMTP_USERNAME')
    smtp_password = os.environ.get('SMTP_PASSWORD')

    assert smtp_server is not None, 'stmp_server is unset'
    assert smtp_username is not None, 'stmp_username is unset'
    assert smtp_password is not None, 'stmp_password is unset'

    if not all([smtp_server, smtp_username, smtp_password]):
        raise ValueError(
            'Missing SMTP configuration. Please create a .env file with '
            'SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, and SMTP_PASSWORD.'
        )

    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        server.quit()
        click.echo(f'Email sent successfully to {to_addr}')
    except Exception as e:
        click.echo(f'Failed to send email: {str(e)}', err=True)
        raise


@click.command()
@click.option('--from', 'from_', required=True, help='Email address of the sender')
@click.option('--to', required=True, help='Email address of the recipient')
@click.option('--title', required=True, help='Subject of the email')
@click.option('--body', required=True, help='Body content of the email')
@click.option('--env-file', help='Path to .env file with SMTP configuration')
def main(from_: str, to: str, title: str, body: str, env_file: str | None) -> None:
    try:
        send_email(from_, to, title, body, env_file)
    except Exception as e:
        click.echo(f'Error: {e}', err=True)
        exit(1)
