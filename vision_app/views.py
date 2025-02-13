from django.shortcuts import render
from django.http import JsonResponse
from .forms import ImageUploadForm
from google.cloud import vision
from google.cloud.vision_v1 import types

def home(request):
    return render(request, 'vision_app/home.html')

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES['image']
            client = vision.ImageAnnotatorClient()

            content = image_file.read()
            image = types.Image(content=content)

            response = client.label_detection(image=image)
            labels = response.label_annotations

            results = [label.description for label in labels]

            return render(request, 'vision_app/results.html', {'results': results})

    else:
        form = ImageUploadForm()

    return render(request, 'vision_app/upload.html', {'form': form})