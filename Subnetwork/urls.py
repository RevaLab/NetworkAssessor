from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('submit_genes/<str:gene_list>', views.index, name='index'),
    path('select_pathways/<str:query_genes_pw_data>', views.pathway_graph, name='pathway_graph'),
    # url(r'^(?P<gene_list>[\w|\W]+)', views.index),
]