"""
WSGI config for crowdfunding project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# set up required for the Django to know how the project will function correctly. 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crowdfunding.settings')

application = get_wsgi_application()
