from flask_mail import Message
from entrymanagement import mail, message_client
from datetime import timedelta


def getdate(timestamp):
    utc_time = timestamp + timedelta(hours=5, minutes=30)
    return utc_time.strftime("%d-%b-%Y")


def get_time_from_timestamp(timestamp):
    if timestamp is None:
        return "N/A"
    datetime_object = timestamp + timedelta(hours=5, minutes=30)
    return datetime_object.strftime("%I:%M %p")


def send_mail_to_host(host, check_in_object):
    msg = Message(
        f"Guest check in",
        sender="entrymanagemen1sys1e@gmail.com",
        recipients=[host.email],
    )
    date = getdate(check_in_object.checkin_timestamp)
    check_in_time = get_time_from_timestamp(check_in_object.checkin_timestamp)
    msg.body = (
        f"Greetings {host.username}, A guest just checked in. The following are the details:-\n"
        f"Name: {check_in_object.guestname}\n"
        f"Email: {check_in_object.email}\n"
        f"Phone: {check_in_object.phone_no}\n"
        f"Check In Time: {check_in_time}\n"
        f"Date: {date}\n"
    )
    mail.send(msg)
    print("mail sent to host")


def send_mail_to_guest(host, check_in_object):
    msg = Message(
        f"Details of your visit",
        sender="entrymanagemen1sys1e@gmail.com",
        recipients=[check_in_object.email],
    )

    check_in_time = get_time_from_timestamp(check_in_object.checkin_timestamp)
    check_out_time = get_time_from_timestamp(check_in_object.checkout_timestamp)

    msg.body = (
        f"Greetings {check_in_object.guestname}, Thank you for your visit. The following are the details:-\n"
        f"Name: {check_in_object.guestname}\n"
        f"Phone: {check_in_object.phone_no}\n"
        f"Check In Time: {check_in_time}\n"
        f"Check Out Time: {check_out_time}\n"
        f"Host Name: {host.username}\n"
        f"Address Visited: {host.address}\n"
    )
    mail.send(msg)
    print("mail sent to guest")


def send_message(host, check_in_object):
    date = getdate(check_in_object.checkin_timestamp)
    check_in_time = get_time_from_timestamp(check_in_object.checkin_timestamp)

    message = (
        f"Greetings {host.username}, A guest just checked in. The following are the details:-\n"
        f"Name: {check_in_object.guestname}\n"
        f"Email: {check_in_object.email}\n"
        f"Phone: {check_in_object.phone_no}\n"
        f"Check In Time: {check_in_time}\n"
        f"Date: {date}\n"
    )

    try:
        message = message_client.messages.create(
            to=f"+91{host.phone_no}", from_="+12024105978", body=message
        )
    except:
        print("some problem with message api")

