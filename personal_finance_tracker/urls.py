"""
URL configuration for personal_finance_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include

urlpatterns = [
    # admin:
    path('admin/', admin.site.urls),

    # Login endpoint:
    path('api/auth/', include('accounts.urls')),
    
    # Apps:
    path('api/transactions/', include('transactions.urls')),
    path('api/dashboard-data/', include('analytics.urls')),
    
    # Frontend:
    path('', include('frontend.urls')),
]


		# <link rel="modulepreload" href="/_app/immutable/entry/start.CNk4m-yS.js">
		# <link rel="modulepreload" href="/_app/immutable/chunks/B6At5cn5.js">
		# <link rel="modulepreload" href="/_app/immutable/chunks/DiOX1np-.js">
		# <link rel="modulepreload" href="/_app/immutable/chunks/CYlZKh32.js">
		# <link rel="modulepreload" href="/_app/immutable/entry/app.BZRGh4Pb.js">
		# <link rel="modulepreload" href="/_app/immutable/chunks/9GPvL92g.js">
		# <link rel="modulepreload" href="/_app/immutable/chunks/Byjy3L_i.js">
		# <link rel="modulepreload" href="/_app/immutable/chunks/Cyrhthi-.js">