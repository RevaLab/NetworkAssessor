from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request, gene_list):
    return HttpResponse(gene_list)