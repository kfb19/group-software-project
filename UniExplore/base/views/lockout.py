from .login import loginPage
from ..models import AccessAttemptAddons
from axes.models import AccessAttempt
from django.contrib import messages
from django.shortcuts import redirect
import datetime

"""
    Authors: Conor Behard Roberts
    Description: Converts timedelta object into a readable string
"""
def strfdelta_round(tdelta, round_period='second'):
    """timedelta to string,  use for measure running time
    attend period from days downto smaller period, round to minimum period
    omit zero value period
    """
    period_names = ('day', 'hour', 'minute', 'second', 'millisecond')
    if round_period not in period_names:
        raise Exception(f'round_period "{round_period}" invalid, should be one of {",".join(period_names)}')
    period_seconds = (86400, 3600, 60, 1, 1 / pow(10, 3))
    period_desc = ('days', 'hours', 'minutes', 'seconds', 'msecs')
    round_i = period_names.index(round_period)

    string = ''
    remainder = tdelta.total_seconds()
    for i in range(len(period_names)):
        q, remainder = divmod(remainder, period_seconds[i])
        if int(q) > 0:
            if not len(string) == 0:
                string += ' '
            string += f'{q:.0f} {period_desc[i]}'
        if i == round_i:
            break
        if i == round_i + 1:
            string += f'{remainder} {period_desc[round_i]}'
            break

    return string


"""
    Authors: Conor Behard Roberts
    Description: When user is locked out add message and redirect to home page
"""
def lockout(request, credentials, *args, **kwargs):
    try:
        username = request.POST.get("username").lower()
        ip_address = request.axes_ip_address
        account = AccessAttempt.objects.filter(username=username).filter(ip_address=ip_address)
        current_time = datetime.datetime.now()
        timeout = 5  # In minutes
        result = AccessAttempt.objects.raw(
            '''
                SELECT axes_accessattempt.id, base_accessattemptaddons.expiration_date
                FROM axes_accessattempt
                INNER JOIN base_accessattemptaddons
                ON axes_accessattempt.id = base_accessattemptaddons.accessattempt_id
                WHERE axes_accessattempt.username = %s and axes_accessattempt.ip_address = %s
                ''', [username, ip_address]
        )[0]

        # Check if the user still has to wait to login again
        if (current_time < result.expiration_date):
            time = result.expiration_date - current_time
            time_s = strfdelta_round(time)
            messages.warning(request, (f"Locked out for {time_s} due to too many login failures"))
        else:
            # Delete the user from the timeout model and re-request the login
            account.delete()
            return loginPage(request)

    except IndexError:
        expiration_date = current_time + datetime.timedelta(minutes=timeout)
        id = AccessAttempt.objects.filter(username=username, ip_address=ip_address)[0].id
        addons = AccessAttemptAddons(expiration_date=expiration_date, accessattempt_id=id)
        messages.warning(request, (f"Locked out for {timeout} minutes due to too many login failures"))
        addons.save()

    return redirect('login')