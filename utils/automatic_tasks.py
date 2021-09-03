import datetime

def automatic_checkouts():

    active_sessions = EmployeeSession.objects.filter(checked_out__isnull = True)
    now = datetime.datetime.now()
    for session in active_sessions:
         attendance = session.   
