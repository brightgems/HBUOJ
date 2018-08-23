from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.core.urlresolvers import reverse
from django.http import HttpResponsePermanentRedirect
from django.utils.translation import ugettext_lazy as _

from judge.feed import CommentFeed, AtomCommentFeed, BlogFeed, AtomBlogFeed, ProblemFeed, AtomProblemFeed
from judge.sitemap import ProblemSitemap, UserSitemap, HomePageSitemap, UrlSitemap, ContestSitemap, OrganizationSitemap, \
    BlogPostSitemap, SolutionSitemap
from judge.views import organization, language, status, blog, problem, license, user, \
    submission, widgets, comment, contests, api, ranked_submission, stats, ticket
from judge.views.problem_data import ProblemDataView, ProblemSubmissionDiff, \
    problem_data_file, problem_init_view
from judge.views.select2 import UserSelect2View, OrganizationSelect2View, ProblemSelect2View, CommentSelect2View, \
    ContestSelect2View, UserSearchSelect2View, ContestUserSearchSelect2View, TicketUserSelect2View, AssigneeSelect2View

admin.autodiscover()


def paged_list_view(view, name):
    return include([
        url(r'^$', view.as_view(), name=name),
        url(r'^(?P<page>\d+)$', view.as_view(), name=name),
    ])


urlpatterns = [
    url(r'^$', blog.PostList.as_view(template_name='home.html', title=_('Home')), kwargs={'page': 1}, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^accounts/', include('allauth.urls')),

    url(r'^problems/$', problem.ProblemList.as_view(), name='problem_list'),
    url(r'^problems/random/$', problem.RandomProblem.as_view(), name='problem_random'),

    url(r'^problem/(?P<problem>[^/]+)', include([
        url(r'^$', problem.ProblemDetail.as_view(), name='problem_detail'),
        url(r'^/editorial$', problem.ProblemSolution.as_view(), name='problem_editorial'),
        url(r'^/raw$', problem.ProblemRaw.as_view(), name='problem_raw'),
        url(r'^/pdf$', problem.ProblemPdfView.as_view(), name='problem_pdf'),
        url(r'^/pdf/(?P<language>[a-z-]+)$', problem.ProblemPdfView.as_view(), name='problem_pdf'),
        url(r'^/clone', problem.clone_problem, name='problem_clone'),
        url(r'^/submit$', problem.problem_submit, name='problem_submit'),
        url(r'^/resubmit/(?P<submission>\d+)$', problem.problem_submit, name='problem_submit'),

        url(r'^/rank/', paged_list_view(ranked_submission.RankedSubmissions, 'ranked_submissions')),
        url(r'^/submissions/', paged_list_view(submission.ProblemSubmissions, 'chronological_submissions')),
        url(r'^/submissions/(?P<user>\w+)/', paged_list_view(submission.UserProblemSubmissions, 'user_submissions')),

        url(r'^/$', lambda _, problem: HttpResponsePermanentRedirect(reverse('problem_detail', args=[problem]))),

        url(r'^/test_data$', ProblemDataView.as_view(), name='problem_data'),
        url(r'^/test_data/init$', problem_init_view, name='problem_data_init'),
        url(r'^/test_data/diff$', ProblemSubmissionDiff.as_view(), name='problem_submission_diff'),
        url(r'^/data/(?P<path>.+)$', problem_data_file, name='problem_data_file'),

        url(r'^/tickets$', ticket.ProblemTicketListView.as_view(), name='problem_ticket_list'),
        url(r'^/tickets/new$', ticket.NewProblemTicketView.as_view(), name='new_problem_ticket'),
    ])),

    url(r'^submissions/', paged_list_view(submission.AllSubmissions, 'all_submissions')),
    url(r'^submissions/user/(?P<user>\w+)/', paged_list_view(submission.AllUserSubmissions, 'all_user_submissions')),

    url(r'^src/(?P<submission>\d+)$', submission.SubmissionSource.as_view(), name='submission_source'),
    url(r'^src/(?P<submission>\d+)/raw$', submission.SubmissionSourceRaw.as_view(), name='submission_source_raw'),

    url(r'^submission/(?P<submission>\d+)', include([
        url(r'^$', submission.SubmissionStatus.as_view(), name='submission_status'),
        url(r'^/abort$', submission.abort_submission, name='submission_abort'),
        url(r'^/html$', submission.single_submission),
    ])),

    url(r'^users/', include([
        url(r'^$', user.users, name='user_list'),
        url(r'^(?P<page>\d+)$', lambda request, page:
        HttpResponsePermanentRedirect('%s?page=%s' % (reverse('user_list'), page))),
        url(r'^find$', user.user_ranking_redirect, name='user_ranking_redirect'),
    ])),

    url(r'^user$', user.UserAboutPage.as_view(), name='user_page'),
    url(r'^edit/profile/$', user.edit_profile, name='user_edit_profile'),
    url(r'^user/(?P<user>\w+)', include([
        url(r'^$', user.UserAboutPage.as_view(), name='user_page'),
        url(r'^/solved', include([
            url(r'^$', user.UserProblemsPage.as_view(), name='user_problems'),
            url(r'/ajax$', user.UserPerformancePointsAjax.as_view(), name='user_pp_ajax'),
        ])),
        url(r'^/submissions/', paged_list_view(submission.AllUserSubmissions, 'all_user_submissions_old')),
        url(r'^/submissions/',
            lambda _, user: HttpResponsePermanentRedirect(reverse('all_user_submissions', args=[user]))),

        url(r'^/$', lambda _, user: HttpResponsePermanentRedirect(reverse('user_page', args=[user]))),
    ])),

    url(r'^comments/upvote/$', comment.upvote_comment, name='comment_upvote'),
    url(r'^comments/downvote/$', comment.downvote_comment, name='comment_downvote'),
    url(r'^comments/hide/$', comment.comment_hide, name='comment_hide'),
    url(r'^comments/(?P<id>\d+)/', include([
        url(r'^edit$', comment.CommentEdit.as_view(), name='comment_edit'),
        url(r'^history/ajax$', comment.CommentRevisionAjax.as_view(), name='comment_revision_ajax'),
        url(r'^edit/ajax$', comment.CommentEditAjax.as_view(), name='comment_edit_ajax'),
        url(r'^votes/ajax$', comment.CommentVotesAjax.as_view(), name='comment_votes_ajax'),
        url(r'^render$', comment.CommentContent.as_view(), name='comment_content'),
    ])),

    url(r'^contests/$', contests.ContestList.as_view(), name='contest_list'),
    url(r'^contests/(?P<year>\d+)/(?P<month>\d+)/$', contests.ContestCalendar.as_view(), name='contest_calendar'),
    url(r'^contests/tag/(?P<name>[a-z-]+)', include([
        url(r'^$', contests.ContestTagDetail.as_view(), name='contest_tag'),
        url(r'^/ajax$', contests.ContestTagDetailAjax.as_view(), name='contest_tag_ajax'),
    ])),

    url(r'^contest/(?P<contest>\w+)', include([
        url(r'^$', contests.ContestDetail.as_view(), name='contest_view'),
        url(r'^/ranking/$', contests.contest_ranking, name='contest_ranking'),
        url(r'^/ranking/ajax$', contests.contest_ranking_ajax, name='contest_ranking_ajax'),
        url(r'^/join$', contests.ContestJoin.as_view(), name='contest_join'),
        url(r'^/leave$', contests.ContestLeave.as_view(), name='contest_leave'),

        url(r'^/rank/(?P<problem>\w+)/',
            paged_list_view(ranked_submission.ContestRankedSubmission, 'contest_ranked_submissions')),

        url(r'^/submissions/(?P<user>\w+)/(?P<problem>\w+)/',
            paged_list_view(submission.UserContestSubmissions, 'contest_user_submissions')),

        url(r'^/participations$', contests.own_participation_list, name='contest_participation_own'),
        url(r'^/participations/(?P<user>\w+)$', contests.participation_list, name='contest_participation'),

        url(r'^/$', lambda _, contest: HttpResponsePermanentRedirect(reverse('contest_view', args=[contest]))),
    ])),

    url(r'^organizations/$', organization.OrganizationList.as_view(), name='organization_list'),
    url(r'^organization/(?P<key>\w+)', include([
        url(r'^$', organization.OrganizationHome.as_view(), name='organization_home'),
        url(r'^/users$', organization.OrganizationUsers.as_view(), name='organization_users'),
        url(r'^/join$', organization.JoinOrganization.as_view(), name='join_organization'),
        url(r'^/leave$', organization.LeaveOrganization.as_view(), name='leave_organization'),
        url(r'^/edit$', organization.EditOrganization.as_view(), name='edit_organization'),
        url(r'^/kick$', organization.KickUserWidgetView.as_view(), name='organization_user_kick'),

        url(r'^/request$', organization.RequestJoinOrganization.as_view(), name='request_organization'),
        url(r'^/request/(?P<pk>\d+)$', organization.OrganizationRequestDetail.as_view(),
            name='request_organization_detail'),
        url(r'^/requests/', include([
            url(r'^pending$', organization.OrganizationRequestView.as_view(), name='organization_requests_pending'),
            url(r'^log$', organization.OrganizationRequestLog.as_view(), name='organization_requests_log'),
            url(r'^approved$', organization.OrganizationRequestLog.as_view(states=('A',), tab='approved'),
                name='organization_requests_approved'),
            url(r'^rejected$', organization.OrganizationRequestLog.as_view(states=('R',), tab='rejected'),
                name='organization_requests_rejected'),
        ])),

        url(r'^/$', lambda _, key: HttpResponsePermanentRedirect(reverse('organization_home', args=[key]))),
    ])),

    url(r'^runtimes/$', language.LanguageList.as_view(), name='runtime_list'),
    url(r'^runtimes/matrix/$', status.version_matrix, name='version_matrix'),
    url(r'^status/$', status.status_all, name='status_all'),

    url(r'^api/', include([
        url(r'^contest/list$', api.api_v1_contest_list),
        url(r'^contest/info/(\w+)$', api.api_v1_contest_detail),
        url(r'^problem/list$', api.api_v1_problem_list),
        url(r'^problem/info/(\w+)$', api.api_v1_problem_info),
        url(r'^user/list$', api.api_v1_user_list),
        url(r'^user/info/(\w+)$', api.api_v1_user_info),
        url(r'^user/submissions/(\w+)$', api.api_v1_user_submissions),
        url(r'^v2/', include([
            url(r'user-info$', api.api_v2_user_info),
        ])),
    ])),

    url(r'^blog/', paged_list_view(blog.PostList, 'blog_post_list')),
    url(r'^post/(?P<id>\d+)-(?P<slug>.*)$', blog.PostView.as_view(), name='blog_post'),

    url(r'^license/(?P<key>[-\w.]+)$', license.LicenseDetail.as_view(), name='license'),

    url(r'^widgets/', include([
        url(r'^rejudge$', widgets.rejudge_submission, name='submission_rejudge'),
        url(r'^single_submission$', submission.single_submission_query, name='submission_single_query'),
        url(r'^submission_testcases$', submission.SubmissionTestCaseQuery.as_view(), name='submission_testcases_query'),
        url(r'^detect_timezone$', widgets.DetectTimezone.as_view(), name='detect_timezone'),
        url(r'^status-table$', status.status_table, name='status_table'),

        url(r'^template$', problem.LanguageTemplateAjax.as_view(), name='language_template_ajax'),

        url(r'^select2/', include([
            url(r'^user_search$', UserSearchSelect2View.as_view(), name='user_search_select2_ajax'),
            url(r'^contest_users/(?P<contest>\w+)$', ContestUserSearchSelect2View.as_view(),
                name='contest_user_search_select2_ajax'),
            url(r'^ticket_user$', TicketUserSelect2View.as_view(), name='ticket_user_select2_ajax'),
            url(r'^ticket_assignee$', AssigneeSelect2View.as_view(), name='ticket_assignee_select2_ajax'),
        ])),

        url(r'^martor/', include('martor.urls')),
    ])),

    url(r'^feed/', include([
        url(r'^problems/rss/$', ProblemFeed(), name='problem_rss'),
        url(r'^problems/atom/$', AtomProblemFeed(), name='problem_atom'),
        url(r'^comment/rss/$', CommentFeed(), name='comment_rss'),
        url(r'^comment/atom/$', AtomCommentFeed(), name='comment_atom'),
        url(r'^blog/rss/$', BlogFeed(), name='blog_rss'),
        url(r'^blog/atom/$', AtomBlogFeed(), name='blog_atom'),
    ])),

    url(r'^stats/', include([
        url('^language/', include([
            url('^$', stats.language, name='language_stats'),
            url('^data/all/$', stats.language_data, name='language_stats_data_all'),
            url('^data/ac/$', stats.ac_language_data, name='language_stats_data_ac'),
            url('^data/status/$', stats.status_data, name='stats_data_status'),
            url('^data/ac_rate/$', stats.ac_rate, name='language_stats_data_ac_rate'),
        ])),
    ])),

    url(r'^tickets/', include([
        url(r'^$', ticket.TicketList.as_view(), name='ticket_list'),
        url(r'^ajax$', ticket.TicketListDataAjax.as_view(), name='ticket_ajax'),
    ])),

    url(r'^ticket/(?P<pk>\d+)', include([
        url(r'^$', ticket.TicketView.as_view(), name='ticket'),
        url(r'^/open$', ticket.TicketStatusChangeView.as_view(open=True), name='ticket_open'),
        url(r'^/close$', ticket.TicketStatusChangeView.as_view(open=False), name='ticket_close'),
        url(r'^/notes$', ticket.TicketNotesEditView.as_view(), name='ticket_notes'),
    ])),

    url(r'^sitemap\.xml$', sitemap, {'sitemaps': {
        'problem': ProblemSitemap,
        'user': UserSitemap,
        'home': HomePageSitemap,
        'contest': ContestSitemap,
        'organization': OrganizationSitemap,
        'blog': BlogPostSitemap,
        'solutions': SolutionSitemap,
        'pages': UrlSitemap([
            {'location': '/about/', 'priority': 0.9},
        ]),
    }}),

    url(r'^judge-select2/', include([
        url(r'^profile/$', UserSelect2View.as_view(), name='profile_select2'),
        url(r'^organization/$', OrganizationSelect2View.as_view(), name='organization_select2'),
        url(r'^problem/$', ProblemSelect2View.as_view(), name='problem_select2'),
        url(r'^contest/$', ContestSelect2View.as_view(), name='contest_select2'),
        url(r'^comment/$', CommentSelect2View.as_view(), name='comment_select2'),
    ])),

    url(r'^cas/', include('mama_cas.urls')),

]

favicon_paths = ['apple-touch-icon-180x180.png', 'apple-touch-icon-114x114.png', 'android-chrome-72x72.png',
                 'apple-touch-icon-57x57.png', 'apple-touch-icon-72x72.png', 'apple-touch-icon.png', 'mstile-70x70.png',
                 'android-chrome-36x36.png', 'apple-touch-icon-precomposed.png', 'apple-touch-icon-76x76.png',
                 'apple-touch-icon-60x60.png', 'android-chrome-96x96.png', 'mstile-144x144.png', 'mstile-150x150.png',
                 'safari-pinned-tab.svg', 'android-chrome-144x144.png', 'apple-touch-icon-152x152.png',
                 'favicon-96x96.png',
                 'favicon-32x32.png', 'favicon-16x16.png', 'android-chrome-192x192.png', 'android-chrome-48x48.png',
                 'mstile-310x150.png', 'apple-touch-icon-144x144.png', 'browserconfig.xml', 'manifest.json',
                 'apple-touch-icon-120x120.png', 'mstile-310x310.png']

from django.templatetags.static import static
from django.utils.functional import lazystr
from django.views.generic import RedirectView

for favicon in favicon_paths:
    urlpatterns.append(url(r'^%s$' % favicon, RedirectView.as_view(
        url=lazystr(lambda: static('icons/' + favicon))
    )))

handler404 = 'judge.views.error.error404'
handler403 = 'judge.views.error.error403'
handler500 = 'judge.views.error.error500'

if 'newsletter' in settings.INSTALLED_APPS:
    urlpatterns.append(url(r'^newsletter/', include('newsletter.urls')))
if 'impersonate' in settings.INSTALLED_APPS:
    urlpatterns.append(url(r'^impersonate/', include('impersonate.urls')))
