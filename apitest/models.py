from django.db import models
from django.contrib.auth.models import User

class MyApp(models.Model):
    name = models.CharField(max_length=50, unique=True)
    owner = models.ForeignKey(User)
    def __unicode__(self):
        return self.name

class MyApi(models.Model):
    name = models.CharField(max_length=100)
    app_name = models.ForeignKey(MyApp)
    url_path = models.CharField(max_length=100)
    methods = (
              ('GET', 'GET'),
              ('HEAD', "HEAD"),
              ('POST', 'POST'),
              ('DELETE', 'DELETE'),
              ('PATCH', "PATCH"),
              ('PUT', 'PUT'),
              ('OPTIONS', 'OPTIONS'),
               )
    method = models.CharField(max_length=20, choices=methods, default='GET', blank=True, null=True)
    category = models.CharField(max_length=50, null=True, blank=True)
    status_code = models.CharField(default='200', max_length=5)
    formats = (
              ('application/xml', 'xml'),
              ('md', 'md'),
              ('application/json', 'json'),
              ('text/html', 'html'),
              ('application/atom+xml', 'atom'),
              ('txt', 'txt'),
              ('text/csv', 'csv'),
              ('application/rss+xml', 'rss'),
              )
    response_format = models.CharField(max_length=20, choices=formats, default='application/json', blank=True, null=True)
    response_body = models.TextField()
    response_headers = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User)
    def __unicode__(self):
        return self.name

class Log(models.Model):
    log_time = models.DateTimeField(auto_now=True)
    app = models.ForeignKey(MyApp)
    header = models.TextField()
    data_posted = models.TextField(null=True, blank=True)
    body = models.TextField()
    # Create your models here.
