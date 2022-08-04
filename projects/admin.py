from django.contrib import admin
from projects.models import UserData, Project, ProjectImage, ProjectCoverImage, ProjectFeatureImage

# Register your models here.
admin.site.register(UserData)
admin.site.register(Project)
admin.site.register(ProjectImage)
admin.site.register(ProjectCoverImage)
admin.site.register(ProjectFeatureImage)
