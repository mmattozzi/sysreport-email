import subprocess
import argparse
from datetime import datetime

def get_disk_usage():
    result = subprocess.run(['df', '-h'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise RuntimeError(f"Error running df: {result.stderr.decode()}")
    return result.stdout.decode()

def get_mdadm_detail():
    result = subprocess.run(['mdadm', '--detail', '/dev/md0'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise RuntimeError(f"Error running mdadm: {result.stderr.decode()}")
    return result.stdout.decode()
    
def get_hostname():
    result = subprocess.run(['hostname'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise RuntimeError(f"Error running hostname: {result.stderr.decode()}")
    return result.stdout.decode().strip()

def send_email(from_email, to_email, sendmail_cmd):
    hostname = get_hostname()
    subject = f"{hostname} System Report: {datetime.today().strftime('%m/%d/%Y')}"

    # Get the disk usage and mdadm details
    disk_usage = get_disk_usage()
    mdadm_detail = get_mdadm_detail()

    # Construct the email headers and body
    message = f"""From: {from_email}
Subject: {subject}
To: {to_email}
Content-Type: text/html

<html>
<head>
    <style>
        pre {{
            font-family: monospace;
        }}
    </style>
</head>
<body>
    <h2>System Report for {hostname}</h2>
    <h3>Disk Usage:</h3>
    <pre>{disk_usage}</pre>
    <h3>MDADM Detail:</h3>
    <pre>{mdadm_detail}</pre>
</body>
</html>
"""

    # Use subprocess to send the email via msmtp
    process = subprocess.Popen(
        [sendmail_cmd, to_email],
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate(input=message.encode())

    if process.returncode != 0:
        print(f"Error sending email: {stderr.decode()}")
    else:
        print("Email sent successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send an email containing system details.')
    parser.add_argument('--from', dest='from_email', required=True, help='The sender email address')
    parser.add_argument('--to', dest='to_email', required=True, help='The recipient email address')
    parser.add_argument('--sendmail-cmd', dest='sendmail_cmd', default='msmtp', help='The command to use to send email')

    args = parser.parse_args()

    send_email(args.from_email, args.to_email, args.sendmail_cmd)
    