
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

urlpatterns=[
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name = 'index'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url( r'^login/$',auth_views.LoginView.as_view(template_name="useraccounts/login.html"), name="login"),
    url(r'^logout/$', auth_views.logout, {"next_page": '/'}), 
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^post/(?P<post_id>\d+)/$', views.post, name='post'),
    url(r'^follow/(?P<followed_id>\d+)/$', views.follow, name='follow'),
    url(r'^like/(?P<post_id>\d+)/$', views.like, name='like')
] 
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)