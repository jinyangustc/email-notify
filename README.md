# Email Notify

A simple command-line tool to send email notifications using SMTP.

## Installation

You can install Email Notify using `pip` or `uv`:

```bash
# Using pip
pip install git+https://github.com/jinyangustc/email-notify.git

# Using uv
uv tool install git+https://github.com/jinyangustc/email-notify.git
```

## Configuration

Email Notify requires SMTP configuration in a `.env` file. Create either:
- A `.env` file in your current directory, or
- A `.email_notify.env` file in your home directory

Example `.env` file:
```
SMTP_SERVER=smtp.example.com
SMTP_PORT=587
SMTP_USERNAME=your_email@example.com
SMTP_PASSWORD=your_password
```

## Usage

```bash
# Send an email
email-notify --from sender@example.com --to recipient@example.com --title "Experiment has finished" --body "Total runtime = 2.34h"

# Use a specific .env file
email-notify --from sender@example.com --to recipient@example.com --env-file /path/to/.env --title "Experiment has finished" --body "Total runtime = 2.34h"
```

## License

MIT
