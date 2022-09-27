import os.path
from django.contrib import messages
from django.contrib.messages import constants as messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from .forms import UserRegistrationForm, CreateDesignForm
from .models import *
from django.views.generic import DeleteView
import os

@login_required
def profile_bb_delete(request, pk):
   bb = get_object_or_404(Bb, pk=pk, status='Новая')
   if not request.user.is_author(bb):
       return redirect('main:profile')
   if request.method == 'POST':
       bb.delete()
       return redirect('main:profile')
   else:
       context = {'bb': bb}
       return render(request, 'main/profile_bb_delete.html', context)


def superAdmin(request):
    bbs = Bb.objects.all().order_by('-created')
    count = Bb.objects.filter(status='Принято в работу').count()
    context = {'bb': bbs, 'count': count}
    return render(request, 'main/superadmin.html', context)


def index(request):
   bbs = Bb.objects.all()
   count = Bb.objects.filter().count()
   context = {'bb': bbs, 'count': count}
   return render(request, 'main/index.html', context)


def other_page(request, page):
   try:
       template = get_template('main/' + page + '.html')
   except TemplateDoesNotExist:
       raise Http404
   return HttpResponse(template.render(request=request))


class RLogin(LoginView):
    template_name = 'main/login.html'


class RLogout(LogoutView, LoginRequiredMixin):
    template_name = 'main/logout.html'


@login_required
def profile(request):
   bbs = Bb.objects.filter(author=request.user.pk).order_by('-created')
   context = {'bbs': bbs}
   return render(request, 'main/profile.html', context)


@login_required
def profiledone(request):
   fil = Bb.objects.filter(author=request.user.pk).order_by('-created')
   context = {'fil': fil}
   return render(request, 'main/profilefilterobrabotka.html', context)


@login_required
def profileiw(request):
   iw = Bb.objects.filter(author=request.user.pk).order_by('-created')
   context = {'iw': iw}
   return render(request, 'main/profileiw.html', context)


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'main/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'main/register.html', {'user_form': user_form})


def application(request):
    if request.method == 'POST':
        form = CreateDesignForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('main:profile')

    else:
        form = CreateDesignForm(initial={'author': request.user.pk})
    return render(request, 'main/creating_an_application_for_the_development.html', {'application_form': form})
