# 中间件
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
# 继承中间件类

class LoginMiddleware(MiddlewareMixin):

    def process_request(self, request):
        print('启动用户权限校验')

        if request.path_info == "/login/":
            return

        user_session = request.session.get('info')
        if not user_session:
            return redirect('/login/')

    def process_response(self, request, response):
        print("用户校验完成")
        return response