from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data = {
            "status_code": response.status_code,
            "errors": response.data,
            "message": getattr(exc, "detail", "정의되지 않는 오류가 발생했습니다."),
        }
    return response
