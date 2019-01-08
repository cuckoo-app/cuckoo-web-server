from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateView, DetailsView, UserView, UserDetailsView, Logout
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = {
    path('jobs/', CreateView.as_view(), name="create"),
    path('jobs/by-job/<pk>',
         DetailsView.as_view(), name="details"),
    # path('jobs/by-user/<pk>',
    #      UserJobView.as_view(), name="user_jobs"),
    path('auth/', include('rest_framework.urls',
                          namespace='rest_framework')),
    path('users/', UserView.as_view(), name="users"),
    path('users/<pk>',
         UserDetailsView.as_view(), name="user_details"),
    path('get-token/', obtain_auth_token),
    path('logout/', Logout.as_view()),
}

urlpatterns = format_suffix_patterns(urlpatterns)
