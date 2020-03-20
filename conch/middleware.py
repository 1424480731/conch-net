from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render
class MyMiddleWare(MiddlewareMixin):

    def process_request(self,request):
        pass

    def process_response(self, request, response):
        return response