from django.urls import include, path

from api import views as v


auth_url = [
    (path('signup/', v.SignUpView.as_view(),
          name='signup')),
    (path('token/', v.TokenView.as_view(),
          name='token')),
]

urlpatterns = [
    path('auth/', include(auth_url)),
    path('check-imei/', v.ImeiView.as_view(), name='imei'),
]