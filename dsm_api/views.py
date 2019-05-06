from django.http import HttpRequest
from django.shortcuts import render


def main(request: HttpRequest):
    return render(request, 'main.html')
