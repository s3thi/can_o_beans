from django.utils.decorators import method_decorator
from django.contrib.auth.views import login
from functools import wraps


def staff_member_required(view_func):
    """
    Decorator for views that checks that the user is logged in and is a staff
    member, displaying the login page if necessary. This is stolen straight
    from the Django source code.
    """
    @wraps(view_func)
    def _checklogin(request, *args, **kwargs):
        if request.user.is_active and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        return login(request, extra_context={'next': request.get_full_path()})

    return _checklogin


class StaffMemberRequiredMixin(object):
    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(StaffMemberRequiredMixin, self).dispatch(*args, **kwargs)
