from django.core.mail import send_mail


def send(user_email):
    """ Отправка письма о подписке """

    send_mail(
        'Вы подписались на рассылку',
        'Мы будем присылать вам много спама.',
        'claytemateam@gmail.com',
        [user_email],
        fail_silently=False
    )
