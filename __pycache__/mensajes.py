import smtplib
from email.mime.text import MIMEText


def send_emails(file, text):
    csvreader = csv.reader(file)
    header = next(csvreader)
    header = next(csvreader)

    rows = []
    for row in csvreader:
        rows.append(row)
        receptor = str(row[0])
        emisor = str(row[1])
        clave = str(row[2])
        cc= str(row[3])
        nombre_emisor= str(row[4])
        nombre_receptor= str(row[5])
    # Define the recipient list
    #recipients = ['recipient1@example.com', 'recipient2@example.com']
    #for receptor in recipients:
    # Define the message content
        message = MIMEText('This is an automatic massive email sent from Python')
        message['Subject'] = 'Automatic Massive Email'
        message['From'] = 'sender@example.com'

        # Create a connection to the SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 465)
        server.ehlo()
        server.starttls()
        server.login('leasingagata@gmail.com', 'password')

        # Send the email to each recipient
        for recipient in recipients:
            message['To'] = recipient
            server.sendmail('sender@example.com', [recipient], message.as_string())

        # Close the connection to the SMTP server
        server.quit()
