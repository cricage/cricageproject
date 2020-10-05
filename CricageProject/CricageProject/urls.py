"""CricageProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,  re_path
from django.conf import settings
from django.conf.urls.static import static
from blogapp import views as blogview
from myScore import views as scoreview
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', blogview.homepageview,name='home'),
    path('news/', blogview.all_post),
    path('post/<int:id>', blogview.post_detail,name="post_detail"),
    path('accounts/',include('django.contrib.auth.urls')),
    path('signup/', blogview.sign_up_view),
    path('academy/', blogview.academy_view),
    path('jobs/', blogview.jobs_view),
    #MYscore App Urls#
    path('postsign', scoreview.postsign),
    path('createteam', scoreview.create_team, name="Create"),
    path('addplayer', scoreview.add_player, name="AddPlayer"),
    path('match', scoreview.matching, name="matching"),
    path('logout', scoreview.logout, name="logout"),
    path('score', scoreview.score, name="score"),
    # MYscore App Urls#

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
