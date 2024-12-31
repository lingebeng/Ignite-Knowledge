from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.path_info in ('/login','/register','/send_email/','/send_email',):
            return
        if request.session.get('info'):
            return
        return redirect("/login")