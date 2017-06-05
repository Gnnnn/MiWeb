from django.conf.urls import url
from . import views
from django.contrib.auth.views import login
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


app_name = 'miweb'
urlpatterns = [
    # ex: /miweb/
    url(r'^$', views.home_views, name='home'),
    url(r'^login/', views.login_views, name='login'),
    url(r'^logout/', views.logout_views, name='logout'),
    url(r'^signup/', views.signup_views, name='signup'),
    url(r'^success/', views.success_views, name='success'),
    url(r'^results/', views.results_views, name='results'),
    url(r'^resultsimage/', views.resultsimage_views, name='resultsimage'),
    url(r'^personinfo/$', views.personinfo, name='personinfo'),
    url(r'^personnews/$', views.personnews, name='personnews'),
    url(r'^personcollect/$', views.personcollect, name='personcollect'),
    url(r'^personfriends/$', views.personfriends, name='personfriends'),
    url(r'^personsearch/$', views.personsearch, name='personsearch'),
    url(r'^advices/$', views.advices, name='advices'),
    url(r'^about/$', views.about, name='about'),
    url(r'^base/$', views.base, name='base'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^upload/record/$', views.upload_record, name='upload_record'),
    url(r'^details/([a-zA-Z][a-zA-Z][0-9]+)/$', views.details, name='details'),
    url(r'^worklog/$', views.worklog, name='worklog'),
    url(r'^change/([a-zA-Z][a-zA-Z][0-9]+)/$', views.change, name='change'),
    url(r'^review/$', views.review, name='review'),
    url(r'^begin/$', views.begin, name='begin'),
    url(r'^invitecode/$', views.invitecode, name='invitecode'),
    url(r'^safepass/$', views.safepass, name='safepass'),
    url(r'^saferealname/$', views.saferealname, name='saferealname'),
    url(r'^reviewdetails/([a-zA-Z][a-zA-Z][0-9]+)/$', views.reviewdetails, name='review'),
]

urlpatterns += [
    # ex: /miweb/
    url(r'^controller/frienddata/$', views.con_friend, name='con_friend'),
    url(r'^controller/newsboxdata/$', views.con_news, name='con_news'),
    url(r'^controller/test/$', views.con_test, name='con_test'),
    url(r'^controller/uploaddata/$', views.con_upload, name='con_upload'),
    url(r'^controller/reviewdata/$', views.con_review, name='con_review'),
    url(r'^controller/con_collect/$', views.con_collect, name='con_collect'),
    url(r'^controller/con_fagree/$', views.con_friendagree, name='con_friendagree'),
    url(r'^controller/con_details/$', views.con_details, name='con_details'),
    url(r'^controller/con_rightnews/$', views.con_rightnews, name='con_rightnews'),

]


urlpatterns += staticfiles_urlpatterns()