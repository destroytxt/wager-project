from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.views.generic import TemplateView


class AboutPage(TemplateView):
    template_name = 'pages/about.html'


class RulesPage(TemplateView):
    template_name = 'pages/rules.html'


def homepage(request):
    return render(request, 'pages/homepage.html')


def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, exception):
    return render(request, 'pages/403csrf.html', status=403)


def server_error(request):
    return render(request, 'pages/500.html', status=500)


def logout_view(request):
    logout(request)
    return redirect('login')
