from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth import login, authenticate, logout
from django.views.generic import UpdateView, DeleteView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import MyApi, MyApp
from .forms import ApiForm, RegForm, AppForm, loginform
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

@csrf_exempt
def reg(request):
    if request.method == 'POST':
        form = RegForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            un = form.cleaned_data['username']
            p1 = form.cleaned_data['password']
            p2 = form.cleaned_data['password2']
            if User.objects.filter(username=un).exists():
                return render(request, 'account/reg1.html', context)
            elif p1 != p2 or p1 == '' or p2 == '':
                return render(request, 'account/reg2.html', context)
            else:
                u = User.objects.create_user(username=un, password=p1)
                u.save()
                us = authenticate(username=un, password=p1)
                login(request, us)
                return HttpResponseRedirect(reverse('success'))
    else:
        form = RegForm()
        context = {'form': form}
    return render(request, 'account/reg.html', context)

@csrf_exempt
def log_in(request):
    if request.method == 'POST':
        form = loginform(request.POST)
        context = {'form': form}
        if form.is_valid():
            un = form.cleaned_data['username']
            pw = form.cleaned_data['password']
            us = authenticate(username=un, password=pw)
            if not User.objects.filter(username=un).exists():
                return render(request, 'account/login1.html', context)
            elif us is None:
                return render(request, 'account/login2.html', context)

            login(request, us)
            return HttpResponseRedirect(reverse('success'))
    else:
        form = loginform()
        context = {'form': form}
    return render(request, 'account/login.html', context)

def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('success'))

@login_required(login_url='/login/')
def new_app(request):
    u = request.user
    if request.method == 'POST':
        form = AppForm(request.POST, request.FILES)
        if form.is_valid():
            i = form.save(commit=False)
            i.owner = u
            i.save()
            return HttpResponseRedirect(reverse('success'))
    else: form = AppForm()
    return render(request, 'apitest/newapp.html', {'form': form})

@login_required(login_url='/login/')
def new_api(request, app_name):
    item = MyApp.objects.get(name=app_name)
    u = request.user
    if not item.owner == u:
        raise Http404
    else:
        if request.method == 'POST':
            form = ApiForm(request.POST, request.FILES)
            if form.is_valid():
                i = form.save(commit=False)
                i.app_name = item
                i.owner = u
                i.save()
                return HttpResponseRedirect('/api/%s' % i.id)
        else: form = ApiForm()
        return render(request, 'apitest/newapi.html', {'form': form, 'item': item})

class AppUpdate(UpdateView):
    model = MyApp
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('success')
    fields = ['name']
    def get_object(self, queryset=None):
        obj = super(AppUpdate, self).get_object()
        u = self.request.user
        if not obj.owner == u:
            raise Http404
        return obj

class AppDelete(DeleteView):
    model = MyApp
    success_url = reverse_lazy('success')
    def get_object(self, queryset=None):
        obj = super(AppDelete, self).get_object()
        u = self.request.user
        if not obj.owner == u:
            raise Http404
        return obj

class ApiUpdate(UpdateView):
    model = MyApi
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('success')
    fields = ['url_path', 'method', 'category', 'status_code', 'response_format', 'response_body', 'response_headers', 'description']
    def get_object(self, queryset=None):
        obj = super(ApiUpdate, self).get_object()
        u = self.request.user
        if not obj.owner == u:
            raise Http404
        return obj

class ApiDelete(DeleteView):
    model = MyApi
    success_url = reverse_lazy('success')
    def get_object(self, queryset=None):
        obj = super(ApiDelete, self).get_object()
        u = self.request.user
        if not obj.owner == u:
            raise Http404
        return obj

def app_list(request):
    list1 = MyApp.objects.all()
    paginator = Paginator(list1, 25)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    return render(request, 'apitest/applist.html', {'items': items})

def list_by_app(request, app_id):
    item = get_object_or_404(MyApp, pk=app_id)
    list1 = MyApi.objects.filter(app_name=item)
    paginator = Paginator(list1, 25)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    return render(request, 'apitest/apilist.html', {'items': items, 'item':item})

def detail(request, api_id):
    item = get_object_or_404(MyApi, pk=api_id)
    context = {"item": item}
    return render(request, 'apitest/detail.html', context)

@csrf_exempt
def apiview(request, app_name, url_path):
    old_path = url_path
    if '.' in url_path:
        d = url_path.index('.')
        url_path = old_path[0:d]
    try:
        item = MyApp.objects.get(name=app_name)
    except ObjectDoesNotExist:
        return HttpResponse(content='No such App.', content_type='text/plain', status=404, reason=None)
    try:
        i = MyApi.objects.get(app_name=item, url_path=url_path)
    except ObjectDoesNotExist:
        return HttpResponse(content='No such Api.', content_type='text/plain', status=404, reason=None)
    if not request.method == i.method:
        return HttpResponse(content='No such method.', content_type='text/plain', status=404, reason=None)
    if '.' in old_path:
        d = old_path.index('.')
        f = d + 1
        content_type = old_path[f:].lower()
        if '/' in i.response_format:
            s1 = i.response_format.index('/')
            if '+' in i.response_format:
                s2 = i.response_format.index('+')
                format = i.response_format[s1 + 1:s2]

            else:
                format = i.response_format[s1 + 1:]
        else:
            format = i.response_format
        if not content_type == format:
            return HttpResponse(content='Wrong content-type.', content_type='text/plain', status=404, reason=None)


    response = HttpResponse()
    response.__init__(content=i.response_body, content_type=i.response_format, status=200, reason=None)

    response.__setitem__('User appended header', i.response_headers)
    return response

def success(request):
    return render(request, 'success.html')



