from django.db import models
from django.utils.text import slugify
from PIL import Image
import pillow_avif # it is necessary to image resize


class UserData(models.Model):
    lock = models.CharField(max_length=1, null=False, primary_key=True, default='X')
    name = models.CharField(max_length=250)
    linkedin = models.URLField(max_length=200, blank=True, null=True)
    github = models.URLField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
       self.pk = 'X'
       super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Project(models.Model):
    position = models.IntegerField(default=1, blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    technologies = models.TextField(blank=True, null=True)
    code = models.URLField(blank=True, null=True)
    page = models.URLField(blank=True, null=True)

    images = models.ManyToManyField('ProjectImage', blank=True)
    cov_images = models.ManyToManyField('ProjectCoverImage', blank=True)
    feat_images = models.ManyToManyField('ProjectFeatureImage', blank=True)

    slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)

    def get_images(self):
        imgs = []
        for i in self.images.all():
            i.image.name = i.image.name.replace('media/resized_images/', '')
            imgs.append(i)
        return imgs

    def count_images(self):
        result = []
        for i in range(0, self.images.all().count()):
            result.append(i)
        return result

    def get_cov_images(self):
        imgs = []
        for i in self.cov_images.all():
            i.image.name = i.image.name.replace('media/resized_images/', '')
            imgs.append(i)
        return imgs

    def count_cov_images(self):
        result = []
        for i in range(0, self.cov_images.all().count()):
            result.append(i)
        return result

    def get_feat_images(self):
        imgs = []
        for i in self.feat_images.all():
            i.image.name = i.image.name.replace('media/resized_images/', '')
            imgs.append(i)
        return imgs

    def count_feat_images(self):
        result = []
        for i in range(0, self.feat_images.all().count()):
            result.append(i)
        return result

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Project, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.title) + "-" + str(self.id)
            self.save()


def image_path_storage(instance, filename):
    if instance.proj:
        return './media/resized_images/projects_images/' + str(instance.proj.title.replace(' ', '')) + '/' + filename
    else:
        return './media/resized_images/no_project_defined/' + filename


class ProjectImage(models.Model):
    proj = models.ForeignKey('Project', on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to=image_path_storage)
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        if self.proj:
            return "imageid-" + str(self.id) + " - " + str(self.proj.title)
        else:
            return "imageid-" + str(self.id)

    def save(self, *args, **kwargs):
        if not self.image:
            return

        super(ProjectImage, self).save(*args, **kwargs)
        image = Image.open(self.image)
        # (width, height) = image.size
        size = (1280, 720)
        image = image.resize(size, Image.ANTIALIAS)
        image.save(self.image.path.split('.')[0]+ '.webp', 'WEBP')



class ProjectCoverImage(models.Model):
    proj = models.ForeignKey('Project', on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to=image_path_storage)

    def __str__(self):
        if self.proj:
            return "covimageid-" + str(self.id) + " - " + str(self.proj.title)
        else:
            return "covimageid-" + str(self.id)

    def save(self, *args, **kwargs):
        if not self.image:
            return

        super(ProjectCoverImage, self).save(*args, **kwargs)
        image = Image.open(self.image)
        # (width, height) = image.size
        size = (1000, 600)
        image = image.resize(size, Image.ANTIALIAS)
        image.save(self.image.path.split('.')[0]+ '.webp', 'WEBP')


class ProjectFeatureImage(models.Model):
    proj = models.ForeignKey('Project', on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to=image_path_storage)
    title = models.TextField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        if self.proj:
            return "featimageid-" + str(self.id) + " - " + str(self.proj.title)
        else:
            return "featimageid-" + str(self.id)

    def save(self, *args, **kwargs):
        if not self.image:
            return

        super(ProjectFeatureImage, self).save(*args, **kwargs)
        image = Image.open(self.image)
        # (width, height) = image.size
        size = (1000, 600)
        image = image.resize(size, Image.ANTIALIAS)
        image.save(self.image.path.split('.')[0]+ '.webp', 'WEBP')