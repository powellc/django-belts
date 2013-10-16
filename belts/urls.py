from django.conf.urls.defaults import patterns, url
import .views as belts_views

'''
  URL map example:

    /student/newuser/  -- NewUser's dashboard
    /dojo/adamsschool/ -- Dojo homepage
    /discipline/learn-gmail/ -- discpline detail
    /discipline/learn-gmail/white-belt/ -- test detail
    /discipline/learn-gmail/white-belt/attempts/ -- test attempt list

'''

urlpatterns = patterns('',
    url(r'^student/(?P<slug>[-\w]+)/$', belts_views.StudentDetailView.as_view(),
    name='belts-student-detail', ),
    url(r'^dojo/$', belts_views.DojoListView.as_view(), name='belts-list', ),
    url(r'^dojo/(?P<slug>[-\w]+)/$', belts_views.DojoDetailView.as_view(), name='belts-detail', ),
    url(r'^disciplines/$', belts_views.DisciplineListView.as_view(), name='belts-discipline-list', ),
    url(r'^disciplines/add/$', belts_views.DisciplineCreateView.as_view(), name='belts-discipline-create', ),
    url(r'^disciplines/(?P<slug>[-\w]+)/$', belts_views.DisciplineDetailView.as_view(),
        name='belts-discipline-detail', ),
    url(r'^disciplines/(?P<discipline_slug>[-\w]+)/tests/add/$', belts_views.TestCreateView.as_view(),
        name='belts-test-create', ),
    url(r'^disciplines/(?P<discipline_slug>[-\w]+)/tests/(?P<slug>[-\w]+)/$', belts_views.TestDetailView.as_view(),
        name='belts-test-detail', ),
    url(r'^disciplines/(?P<discipline_slug>[-\w]+)/tests/(?P<test_slug>[-\w]+)/attempts/(?P<pk>[\d]+)/$', belts_views.TestCompleteView.as_view(),
        name='belts-test-attempts', ),
    url(r'^disciplines/(?P<discipline_slug>[-\w]+)/tests/(?P<test_slug>[-\w]+)/attempts/$', belts_views.TestAttemptListView.as_view(),
        name='belts-test-attempt-list', ),
    url(r'^', belts_views.BeltsIndexView.as_view(), name="belts-index")
)
