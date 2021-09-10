"""skripsi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
# from django.contrib import admin
# from django.urls import path

# from QA import views as appview

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path(r'^$',appview.skripsi),
#     path(r'^skripsi/',appview.skripsi),
# ]

from django.conf.urls import url
from django.contrib import admin

from QA import views as appview

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'$',appview.skripsi), # kurang tangda pangkat
    url(r'^$',appview.skripsi),
    url(r'^skripsi/',appview.skripsi),
    url(r'^semua/',appview.semua),
    url(r'^proses/',appview.proses),
    url(r'^get_title/',appview.get_title),
    url(r'^get_topic/',appview.get_topic),
    url(r'^preprocessing/',appview.preprocessing),
    url(r'^word_graph_babelnet/',appview.word_graph_babelnet),
    url(r'^cnn/',appview.cnn),
    url(r'^title_wikipedia/',appview.title_wikipedia),
    url(r'^check_answer_sparql/',appview.check_answer_sparql),
    url(r'^sparql_dbpedia/',appview.sparql_dbpedia),
    url(r'^crawl_artikel/',appview.crawl_artikel),
]