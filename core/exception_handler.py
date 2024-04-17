from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call DRF's default exception handler first
    response = exception_handler(exc, context)

    if response is not None:
        # Change the key 'detail' to 'message'
        response.data['message'] = response.data.pop('detail')
    
    if response is not None and response.status_code == 403:
        response.status_code = 401

    return response
