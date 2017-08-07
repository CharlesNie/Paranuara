from django.conf.urls import include, url
from system.views import ParanuaraView

urlpatterns = [
		url(r'^', ParanuaraView.as_view(), name='pview'),
		]
