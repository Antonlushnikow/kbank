# from mainapp.models import Notification
# from authapp.models import KbankUser


def create_notification(request, body, scope=None):
    if scope == "all":
        users = KbankUser.objects.all()
    elif scope == "moderators":
        users = [user for user in KbankUser.objects.all() if user.is_privileged]
    else:
        users = [request.user]
    for user in users:
        obj = Notification.objects.create(user=user, body=body)
        obj.save()


def plural_days(days):
    days_variants = ['день', 'дня', 'дней']

    if days % 10 == 1 and days % 100 != 11:
        index = 0
    elif 2 <= days % 10 <= 4 and (days % 100 < 10 or days % 100 >= 20):
        index = 1
    else:
        index = 2

    return str(days) + ' ' + days_variants[index]


def plural_hours(hours):
    hours_variants = ["час", "часа", "часов"]

    last_two_digits = hours % 100
    tens = last_two_digits // 10
    ones = last_two_digits % 10
    index = 2

    if tens == 1:
        index = 2
    elif ones == 1:
        index = 0
    elif 2 <= ones <= 4:
        index = 1

    return f"{hours} {hours_variants[index]}"


for i in range(1, 50):
    print(plural_hours(i), sep='\n')
