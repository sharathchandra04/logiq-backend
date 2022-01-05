from django.conf.urls import url
# from user.views import UserRegistrationView
from pycaretapp.views import PycaretDataMeans
from pycaretapp.views import PycaretDataAnamoly

# from pycaretapp.views import UserValidateView

urlpatterns = [
    # url(r'^signup', UserRegistrationView.as_view()),
    url(r'^getmean', PycaretDataMeans.as_view()),
    url(r'^getanamoly', PycaretDataAnamoly.as_view()),
    # url(r'^validate', UserValidateView.as_view()),
]
