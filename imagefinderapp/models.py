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