## How to Create an Image Finder Application with Python Django and Pexels API

This guide describes how to build an image finder application using Django and the Pexels API. This integration allows users to search for relevant images directly within your application. 

We'll guide you through the development process, from project setup to displaying search results. This guide is accessible for developers with a basic understanding of Python and Django.

## About the author - André Gervásio

20+ years of experience in software development. Bachelor's degree in Computer Science. Fullstack Software Engineer and Tech Lead in Java, Python, JS, PHP applications. Certified in Front-End, Back-End and DevOps technologies. Experienced in Scrum and Agile Methodologies. Solid knowledge in Databases and ORMs. Practical skills in Cloud Computing Services.

[Visit my LinkedIn](https://www.linkedin.com/in/andregervasio/)

## 1. Install Python and Django

Before diving into code, ensure you have the necessary tools:

* Verify Python installation using the following command in your terminal:

```bash
python3 --version #or python --version
```

* If it's installed, you should see the version number. Otherwise, download it from [https://www.python.org/downloads/](https://www.python.org/downloads/).

* Create a directory for your project. In this article, we'll use the name **imagefinder-django-pexels**. Navigate to it and create a virtual environment to isolate project dependencies:

```bash
mkdir imagefinder-django-pexels
cd imagefinder-django-pexels
python3 -m venv venv
```

* Activate the virtual environment:

```bash
source venv/bin/activate
```

* Install Django using pip:

```bash
pip install django
```

* The **requests** library allows us to make HTTP requests to the Pexels API. Install it using pip:

```bash
pip install requests
```

## 2. Create a Django Project

A Django project serves as the foundation for your image finder application.

* Open your terminal and navigate to your desired project directory.
* Execute the following command to create a new Django project named **imagefinder** in the current directory:

```bash
django-admin startproject imagefinder .
```

## 3. Create a Django App

Django apps organize functionalities. We'll create one for our image finder logic:

* Within your **imagefinder** project directory, run this command:

```bash
python3 manage.py startapp imagefinderapp
```

## 4. Generate Pexels API Key

Pexels offers a free API that allows developers to search for and download images. We'll be using the Pexels API within our Django app to retrieve image data.

* Sign up for a Pexels API key at [https://www.pexels.com/api](https://www.pexels.com/api).

* Store your API key securely. One way to achieve this is by creating a `.env` file in your project's root directory and adding the following line:

```
PEXELS_API_KEY=YOUR_API_KEY_HERE
```

**Important:** Never store your API key directly in your code. The `.env` file is a common practice for storing sensitive information in Django projects.

## 5. Configure Django Settings

Now, let's configure Django to work with our image finder app and API key.

* Django projects are organized by individual applications, each focusing on specific functionalities. In step 3, you created a Django app named **imagefinderapp** to encapsulate the logic behind your image finder. Here's why we need to add it to `INSTALLED_APPS`:

    * Modular Project Structure: Django projects promote a modular approach. By creating separate apps, you can organize your codebase efficiently and maintain a clean separation of concerns. Each app can have its own models, views, templates, and other components specific to its functionality.
    * App Recognition: When you add `imagefinderapp` to `INSTALLED_APPS`, you essentially tell Django: "Hey, this `imagefinderapp` exists, and it's part of this project. Recognize it and include its functionalities when running the project."
    * Component Discovery: Including `imagefinderapp` in `INSTALLED_APPS` allows Django to discover the components (models, views, templates) within your `imagefinderapp`. These components are crucial for building the image finder's features.

* Open your project's `imagefinder/settings.py` file.
* Inside the `INSTALLED_APPS` list, add `'imagefinderapp'`.

## 6. Create the Pexels Image Model

In your `imagefinderapp/models.py` file, define a model named `PexelsImage`.

This model will handle interacting with the Pexels API and storing the retrieved image data.

```python
from django.db import models
import requests, os

class PexelsImage(models.Model):
  url = models.URLField(max_length=2048)
  previewURL = models.URLField(max_length=2048)
  photographer = models.CharField(max_length=255)

  @classmethod
  def search(cls, query):
    pexels_api_key = os.environ.get('PEXELS_API_KEY')
    headers = {'Authorization': f'{pexels_api_key}'}
    url = f'https://api.pexels.com/v1/search?query={query}'
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for non-200 status codes

    data = response.json()
    images = [
      PexelsImage(
        url=photo['url'],
        previewURL=photo['src']['tiny'],
        photographer=photo['photographer']
      )
      for photo in data['photos']
    ]
    return images
```

This model defines a `PexelsImage` class with fields for the image URL, preview URL, and photographer's name.

We'll leverage the `@classmethod` decorator to define a method named `search` that interacts with the Pexels API.

The `search` class method takes a search query as input and interacts with the Pexels API using the provided API key. It parses the JSON response and returns a list of `PexelsImage` objects containing the retrieved image data.

## 7. Create the Search Form

In the `imagefinderapp/forms.py` file, create a simple form to allow users to enter their search query:

```python
from django import forms

class PexelsSearchForm(forms.Form):
    query = forms.CharField(label="Search Images", max_length=100)
```

## 8. Create the Search View

Create a view in `imagefinderapp/views.py`.

The view function will handle displaying the search form and processing the user's search query.

```python
from django.shortcuts import render
from .models import PexelsImage
from .forms import PexelsSearchForm

def search(request):
    if request.method == 'POST':
        form = PexelsSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            images = PexelsImage.search(query)
    else:
        form = PexelsSearchForm()
        images = []

    context = {'form': form, 'images': images}
    return render(request, 'imagefinder/search.html', context)
```

## 9. Configure Routes

In Django, URLs map user requests to specific views. This step involves defining routes within your image finder app and including them in your main project's URL configuration.

* Create a new file `imagefinderapp/urls.py`. This file will define URL patterns specific to your image finder app.

```python
from django.urls import path
from .views import search

urlpatterns = [
    path('', search, name='search'),
]
```

* Now, you need to include the image finder app's URL patterns within your main project's URL configuration file `imagefinder/urls.py`.

```python
from django.urls import path, include  # Don't forget to import include function
from adminsite import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('imagefinder/', include('imagefinderapp.urls')),  # Include the imagefinder app's URL patterns
]
```

## 10. Create the Search Template

Templates define the structure and presentation of your image finder's user interface.

* Create a template in `templates/imagefinder/search.html`.

This template will display the search form and the retrieved images.

```html
<!DOCTYPE html>
<html>
<head>
    <title>Image Finder</title>
</head>
<body>
    <h1>Image Finder</h1>
    <form method="POST">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Search</button>
    </form>

    {% if images %}
        <h2>Search Results</h2>
        {% for image in images %}
        <span>
            <a href="{{ image.url }}" target="_blank">
                <img src="{{ image.previewURL }}" alt="{{ image.photographer }} - Pexels">
            </a>
        </span>
        {% endfor %}
    {% else %}
        <p>No results found.</p>
    {% endif %}
</body>
</html>
```

* To ensure Django recognizes your template directory, you need to update the `TEMPLATES` setting in your `imagefinder/settings.py` file.

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Update DIRS path. Don't forget to include os package.
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [],
        },
    },
]
```

## 11. Run Migrations and Start the Development Server

Django automatically creates tables based on your models as a best practice and to provide a foundation for potential future functionalities that involve data persistence. While our current image finder app doesn't require a database at its core, the model and its table structure offer flexibility for future development.

In your terminal, run the following commands to create the database and start the Django development server:

```bash
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```

This will typically launch the server on port 8000 by default.

Open your web browser and visit the chatbot URL defined in your project's URL configuration (http://127.0.0.1:8000/imagefinder). This should render your image finder interface.

## Conclusion

We've successfully built a functional image finder application using Django and the Pexels API. This app empowers you to seamlessly search for and discover royalty-free images directly within your development environment, saving you valuable time and effort.

While this basic implementation focuses on retrieving images from Pexels, you can extend it further to incorporate features like:

* **Image filtering:** Allow users to filter search results based on specific criteria like color, orientation, or size.
* **Pagination:** Implement pagination to handle large result sets and improve user experience.
* **User authentication:** Integrate user authentication to enable users to save their favorite searches or create personalized image collections.

This image finder application serves as a solid foundation. With your creativity and programming skills, you can customize and enhance it to cater to your specific needs and project requirements. Explore the vast capabilities of Django and the Pexels API to unlock the full potential of this image finder tool!
