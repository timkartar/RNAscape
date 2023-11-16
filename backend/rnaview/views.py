import os
import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import requests
import time

base_script_path = '/home/aricohen/Desktop/rnaview/'

def is_file_served(url):
    try:
        response = requests.head(url)
        return response.status_code == 200
    except requests.RequestException:
        return False


def run_regen_labels(request):
    if request.method == "GET":
        # Define the path to your script
        rotation = request.GET.get('rotation')
        time_string = request.GET.get('timeString')

        script_path = f'{base_script_path}/regen_labels.py'

        try:
            result = subprocess.run(
                        ['python', script_path, time_string, rotation], 
                        capture_output=True, 
                        text=True,
                        check=True
                    )
            image_path = result.stdout.strip()
            image_url = request.build_absolute_uri(default_storage.url(image_path))
            # Polling to check if the file is being served
            for _ in range(10):  # Number of attempts
                if is_file_served(image_url):
                    return JsonResponse({'image_url': image_url, 'time_string': time_string})
                time.sleep(1)  # Wait for 1 second before next attempt
            return JsonResponse({'error': 'File not ready 1'}, status=500)
        except subprocess.CalledProcessError as e:
            # Handle errors in the subprocess
            return JsonResponse({"error": str(e), "output": e.stderr}, status=500)

@csrf_exempt  # Exempting from CSRF for demonstration purposes only
@require_POST
def run_rnaview(request):
    # Get the file from the request

    file = request.FILES.get('file')
    additionalFile = request.FILES.get('additionalFile')
    basePairAnnotation = request.POST.get('basePairAnnotation')
    loopBulging = request.POST.get('loopBulging')
    additional_file_path=""

    # Now you can run your Python script using the saved file
    script_path = f'{base_script_path}/run.py'

    if file:
        # Define file path (you can include a specific path if needed)
        file_path = os.path.join('uploads', file.name)


        # Write file to disk
        with default_storage.open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        # If RNAView, special case
        if basePairAnnotation == "rnaview":
            # check if a file is provided!
            if additionalFile:
                additional_file_path = os.path.join('uploads', additionalFile.name)
                with default_storage.open(additional_file_path, 'wb+') as destination:
                    for chunk in additionalFile.chunks():
                        destination.write(chunk)
            else:
                return JsonResponse({"error": "No rnaview output file provided"}, status=400)
        try:
            # Call your script with the file path as an argument
            result = None
            if basePairAnnotation == "rnaview":
                result = subprocess.run(
                    ['python', script_path, file_path, file.name, loopBulging, basePairAnnotation, additional_file_path], 
                    capture_output=True, 
                    text=True,
                    check=True
                )
            else:
                result = subprocess.run(
                    ['python', script_path, file_path, file.name, loopBulging, basePairAnnotation], 
                    capture_output=True, 
                    text=True,
                    check=True
                )

            # You can access result.stdout, result.stderr, result.returncode here
            # No need to save again, just construct the URL

            image_path = result.stdout.split(',')[0].strip()
            time_string = result.stdout.split(',')[1].strip()
            

            image_url = request.build_absolute_uri(default_storage.url(image_path))
            # Polling to check if the file is being served
            for _ in range(10):  # Number of attempts
                if is_file_served(image_url):
                    return JsonResponse({'image_url': image_url, 'time_string': time_string})
                time.sleep(1)  # Wait for 1 second before next attempt
            return JsonResponse({'error': 'File not ready 1'}, status=500)
        except subprocess.CalledProcessError as e:
            # Handle errors in the subprocess
            return JsonResponse({"error": str(e), "output": e.stderr}, status=500)
    else:
        return JsonResponse({"error": "No file provided"}, status=400)
