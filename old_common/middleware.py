from django.http import HttpResponse

class NoCacheMiddleware(object):
    def process_response(self, request, response):
        response['Pragma'] = 'no-cache'
#        response['Expires'] = '-1'
        response['Cache-Control'] = 'no-cache no-store must-revalidate proxy-revalidate'
        return response