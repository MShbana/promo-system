"""promo_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import include, path
from django.http import HttpResponse

github_project_url = 'https://github.com/MShbana/promo-system#endpoints'

urlpatterns = [
    path(
        '',
        lambda request: HttpResponse(
            f"""
            <h1>You can find all the avaialble endpoints in
            <a href="{github_project_url}">GitHub</a></h1>
            """
        )
    ),
    path(
        'admin/',
        admin.site.urls
    ),
    path(
        'accounts/',
        include('accounts.urls')
    ),
    path(
        'promos/',
        include('promos.urls')
    ),
]
