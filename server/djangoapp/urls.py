from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL
    path(route='about', view=views.about, name='about'),
    path(route='contact', view=views.contact, name='contact'),
    path(route='registration', view=views.registration_request, name='registration'),
    path(route='login', view=views.login_request, name='login'),
    path(route='logout', view=views.logout_request, name='logout'),
    path(route='dealerships', view=views.get_dealerships, name='dealerships'),
    path(route='dealer/<int:dealer_id/>', view=views.get_dealer_details, name='dealer_details'),
    # path(route='review/add>', view=views.get_dealer_details, name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
