import datetime
import sys

sys.path.append("../")
from employees.models import EmployeeSession, Attendance, Employee


def automatic_checkouts():

    active_sessions = EmployeeSession.objects.filter(checked_out__isnull=True)
    now = datetime.datetime.now()
    for session in active_sessions:
        session.checked_out_at = now
        session_length = now - session.checked_in_at
        attendance = Attendance.objects.get(id=session.fk_attendance.id)
        attendance.total_time = (
            datetime.datetime.combine(datetime.date.today(), attendance.total_time)
            + session_length
        ).time()

        attendance.save()
        session.save()



# def automatic_leave_generation():
