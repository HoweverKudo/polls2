from django.urls import path
from django.conf import settings
from django.views.decorators.cache import cache_page as view_cach_page

def cache_page(view, timeouts=800):
    # キャッシュする用のmethod
    return view_cach_page(timeouts)(view)