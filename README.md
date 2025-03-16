# sysreport-email

This is a really simple python program that will send out an email with some system details. This depends on a mail sender like msmtp or sendmail being setup correctly. This is a good program to just put in a crontab to run daily or once a week for a homelab type of server. I will probably evolve this over time. 

# Usage 
```
usage: sysreport-email.py [-h] --from FROM_EMAIL --to TO_EMAIL [--sendmail-cmd SENDMAIL_CMD]

Send an email containing system details.

options:
  -h, --help            show this help message and exit
  --from FROM_EMAIL     The sender email address
  --to TO_EMAIL         The recipient email address
  --sendmail-cmd SENDMAIL_CMD
                        The command to use to send email
```
