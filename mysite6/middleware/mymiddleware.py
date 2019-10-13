from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse, Http404


class MyMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print('路由是：', request.path)
        print('请求方法是：', request.method)
        print("中间件 process_request方法被调用")
        if request.path == '/aaaa':
            return HttpResponse('当前路由是/aaaa')


class VisitLimit(MiddlewareMixin):
    visit_times = {} # 此字典的键为IP地址，值为该IP访问次数
    def process_request(self, request):
        ip = request.META['REMOTE_ADDR'] # 得到客户端IP
        if request.path_info != '/test':
            return
        # 获取以前的方位次数
        times = self.visit_times.get(ip, 0)
        print('IP', ip, '已访问/test', times, '次')
        self.visit_times[ip] = times + 1
        if times <= 5:
            return
        return HttpResponse('您已经访问过'+str(times)+'次')
