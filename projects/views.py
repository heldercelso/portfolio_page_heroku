from django.shortcuts import render
from projects.models import Project, UserData
from django.core.exceptions import ObjectDoesNotExist


def project_index(request):
    projects = Project.objects.all().order_by("-position")
    try:
        user = UserData.objects.get()
    except ObjectDoesNotExist as e:
        user = None

    context = {
        'user': user,
        'projects': projects,
    }

    return render(request, 'project_index.html', context)

def project_detail(request, slug):
    try:
        project = Project.objects.get(slug=slug)
    except ObjectDoesNotExist:
        project = None
    
    try:
        user = UserData.objects.get()
    except ObjectDoesNotExist as e:
        user = None

    context = {
        'user': user,
        'project': project,
    }

    return render(request, 'project_detail.html', context)
