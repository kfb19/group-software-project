"""
Authors: 
    - Michael Hills
"""

from django.apps import AppConfig

# (Michael Hills)
class BaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base'
