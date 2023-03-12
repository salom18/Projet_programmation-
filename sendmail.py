####PART 4 ----Send email with all information###
import smtplib
import time

def send_email():
    message1 = get_weather()
    if message1 is not None:
        message1 = str(message1)

    message2 = find_hotels()
    if message2 is not None:
        message2 = str(message2)

    message3 = get_sent()
    if message3 is not None:
        message3 = str(message3)

    message_final = (message1 or "") + (message2 or "") + (message3 or "")
    s=smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login("projectpythonse@gmail.com", "cbodytjuxpnmorbe")
    SUBJECT="Informations"
    TEXT=message_final.encode('utf-8')
    message="Subject:{}\n\n{}".format(SUBJECT,TEXT.decode('utf-8'))
    while True:
        destinateur=input("Enter your email:")
        if not destinateur:
            print("Email address cannot be empty. Please try again.")
        elif "@" not in destinateur:
            print("Invalid email address. Please try again.")
        else:
            break
    s.sendmail("projectpythonse@gmail.com", destinateur,message.encode('utf-8'))
    s.quit()
    print("Formuler le mail.")
    time.sleep(2)
    print("En train d'envoyer le mail...")
    time.sleep(1)
    print("Email envoyé! ")

send_email()
