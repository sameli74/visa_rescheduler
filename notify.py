import yagmail


class Gmail():
    def __init__(self, user, app_password):
        self.__user = user
        self.__password = app_password
    def send(self, to, subject, content):
        with yagmail.SMTP(self.__user, self.__password) as yag:
            yag.send(to, subject, content)




def push_notification(dates, sender, receivers, subject, scopes):
    msg = "date: "
    for d in dates:
        msg = msg + d.get('date') + '; '
    for receiver in receivers:
        gmail_send_message(msg, sender, receiver, subject, scopes)
