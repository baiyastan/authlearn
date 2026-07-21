from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def api_root(request):
    return JsonResponse(
        {
            "message": "Auth API is running!",
            "endpoints": {
                "register": "/api/auth/register/",
                "login": "/api/auth/login/",
                "logout": "/api/auth/logout/",
                "profile": "/api/auth/profile/",
                "change_password": "/api/auth/change-password/",
                "token_refresh": "/api/auth/token/refresh/",
                "users": "/api/auth/users/",
            },
        }
    )


urlpatterns = [
    path("", api_root, name="api-root"),
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
]
