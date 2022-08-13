## Introduction

Portfolio page for developers to showcase their projects. It was mainly implemented in Django (Python) adapted to run on the free version of Heroku.


## Technologies

The implementation was carried out using Python version `3.10.6` with the following main libraries:

 - Django 4.1 (back-end)
 - Whitenoise (static files)
 - Gunicorn (WSGI)
 - Pillow (images resize)
 - Bootstrap 5.2 - HTML/CSS (front-end)

### Structure

```shell
.
├── media                                                                 # product image storage
├── requirements.txt                                                      # libraries
├── portfolio_project                                                     # django project
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── projects                                                              # main django application
│   ├── migrations.py
│   │   └── 0001_initial.py
│   ├── static
│   │   ├── css
│   │   │   ├── project_detail_boot.css
│   │   │   └── project_index_boot.css
│   │   └── favicon.png
│   ├── templates
│   │   ├── base.html
│   │   ├── navbar.html
│   │   ├── project_detail.html
│   │   └── project_index.html
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── static                                                                # it is generated after run collectstatic django command
├── db.sqlite3                                                            # this db is used only for debug purpose (running locally)
├── manage.py
├── Procfile                                                              # Heroku requirement to find wsgi (gunicorn in this case)
├── README.md
├── requirements.txt
└── runtime.txt                                                           # Heroku requirement to set python version
```


## Running the project

To run locally:

```shell
# Create virtual environment inside the project folder:
$ pip install virtualenv
$ python -m virtualenv venv

# Activate venv
$ source venv/Scripts/activate

# Install libs inside venv
$ pip install -r requirements.txt

# Create database tables
$ python manage.py migrate

# Run the server
$ python manage.py runserver
```

To access the application, just open the address `http://localhost:8000` in your browser.


## Handling the project

### Project data

1. Each project contains the following fields to be filled:

 * Position: You can define the order of the projects using this variable (highest value goes to the top);
 * Title (required): It appears in the main page above project cover images;
 * Description: It appears in the main page below project cover images;
 * Technologies: It appears inside project details below project images;
 * Cover images: Four images used in the main page to show the project;
 * Images: It is used inside project details to show all details about the project;
 * Feature images: It is used inside project details to show specific features.

2. Take pictures of the project:

These pictures will be used as cover images, project images and feature images according explained and should be placed inside `media/projects/<project_name>`.
Don't forget to rename the files accordingly:
 * Cover: cover1.png, cover2.png, cover3.png, cover4.png
 * Project: image1.png, image2.png, ...
 * Feature: feature1.png, feature2.png, ...

That said, you can populate the DB using django admin page or using shell commands. More details ahead.

### User data

In addition to project information, you can fill in the author's name, linkedin and github profiles link. It will appear at the top of the navigation bar.
NOTE: You can only add one user, so to add another one you need to delete the previous one or just edit it.


## Database

* If `DEBUG==True` a SqLite database will be created when running the project. The migrations are already created so you need to run `python manage.py migrate` only to execute them.
* If `DEBUG==False` the Heroku-PostgreSQL database will be used.

NOTE: if environment variable `DJANGO_DEBUG` is not created, `DEBUG` is set to `True` by default.

### Populate DB using django admin

1. Create a superuser:
```shell
# Create superuser (admin), run the command and fill username, email and password:
$ python manage.py createsuperuser
```

2. Open the browser and go to `localhost:8000/admin`, then login with the user created earlier.

3. Once logged into the admin panel, go to Projects and fill in the fields.

### Populate DB using shell commands

1. Enter django shell:
```shell
$ python manage.py shell
```

2. Run the commands:

* Adding project:
```shell
# Needed imports
from django.core.files.images import ImageFile
from projects.models import Project, ProjectImage, ProjectCoverImage, ProjectFeatureImage

# Creating the project
p = Project(
    position=1,
    title='project title here',
    description='project description here',
    technologies='technologies used in the project here',
)
p.save()

# Adding project cover images
p.cov_images.add(*[
    ProjectCoverImage.objects.create(proj=p, image=ImageFile(open('./media/projects/ExampleParkingSoftware/cover1.png', 'rb'), name='cover1.webp')),
    ProjectCoverImage.objects.create(proj=p, image=ImageFile(open('./media/projects/ExampleParkingSoftware/cover2.png', 'rb'), name='cover2.webp')),
])

# Adding project images
p.images.add(*[
    ProjectImage.objects.create(proj=p, image=ImageFile(open('./media/projects/ExampleParkingSoftware/image1.png', 'rb'), name='image1.webp'), text='Text for image1'),
])

# Adding project feature images
p.feat_images.add(*[
    ProjectFeatureImage.objects.create(proj=p, image=ImageFile(open('./media/projects/ExampleParkingSoftware/feature1.png', 'rb'), name='feature1.webp'), title='Title for feature1', text='Text for feature1'),
])
```

These commands will upload and resize the images to `media/resized_images/project_images/ExampleParkingSoftware`. If you've already done this upload process and just want to attach the image directly, replace the part of the image with:
 * Remove it: `image=ImageFile(open('./media/projects/ExampleParkingSoftware/feature1.png', 'rb'), name='feature1.webp')`
 * Replace with: `image='./media/resized_images/projects_images/ExampleParkingSoftware/feature1.webp'`

NOTE: In the free version of Heroku, you cannot upload images, so you need to include the already resized images in the commit.

* Adding user:

```shell
from projects.models import UserData
u = UserData(
    name='`<author_name>`',
    linkedin='`http://www.linkedin.com/in/<author_linkedin>`',
    github='`https://github.com/<author_github>`',
)
u.save()
```

## Deploying to Heroku

1. Create a Heroku free app;
2. In `Resources`, add a Heroku-PostgreSQL database;
3. In `Settings`, click in `Reveal Config Vars` and add:
    * DATABASE_URL: Paste the `URI` of the database created earlier (get it in: `Resources > Open Heroku Postgres > Settings > Database Credentials > View Database Credentials`);
    * DJANGO_DEBUG: False;
    * DJANGO_SECRET_KEY: `your django secret-key`.
4. In `Deploy` choose one method to upload the project.
