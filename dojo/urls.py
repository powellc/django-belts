from django.conf.urls.defaults import patterns, url
from dojo import views as dojo_views

'''
  URL map example:

    /student/newuser/  -- NewUser's dashboard
    /dojo/adamsschool/ -- Dojo homepage
    /discipline/learn-gmail/ -- discpline detail
    /discipline/learn-gmail/white-belt/ -- test detail
    /discipline/learn-gmail/white-belt/attempts/ -- test attempt list

'''

urlpatterns = patterns('',
                       url(r'^student/(?P<slug>[-\w]+)/$', dojo_views.StudentDetailView.as_view(),
                           name='dojo-student-detail', ),
                       url(r'^dojo/$', dojo_views.DojoListView.as_view(), name='dojo-list', ),
                       url(r'^dojo/(?P<slug>[-\w]+)/$', dojo_views.DojoDetailView.as_view(), name='dojo-detail', ),
                       url(r'^disciplines/$', dojo_views.DisciplineListView.as_view(), name='dojo-discipline-list', ),
                       url(r'^disciplines/add/$', dojo_views.DisciplineCreateView.as_view(), name='dojo-discipline-create', ),
                       url(r'^disciplines/(?P<slug>[-\w]+)/$', dojo_views.DisciplineDetailView.as_view(),
                           name='dojo-discipline-detail', ),
                       url(r'^disciplines/(?P<discipline_slug>[-\w]+)/tests/add/$', dojo_views.TestCreateView.as_view(),
                           name='dojo-test-create', ),
                       url(r'^disciplines/(?P<discipline_slug>[-\w]+)/tests/(?P<slug>[-\w]+)/$', dojo_views.TestDetailView.as_view(),
                           name='dojo-test-detail', ),
                       url(r'^disciplines/(?P<discipline_slug>[-\w]+)/tests/(?P<test_slug>[-\w]+)/attempts/(?P<pk>[\d]+)/$', dojo_views.TestCompleteView.as_view(),
                           name='dojo-test-attempts', ),
                       url(r'^disciplines/(?P<discipline_slug>[-\w]+)/tests/(?P<test_slug>[-\w]+)/attempts/$', dojo_views.TestAttemptListView.as_view(),
                           name='dojo-test-attempt-list', ),
                       url(r'^', dojo_views.DojoIndexView.as_view(), name="dojo-index")
)
