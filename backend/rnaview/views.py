import os
import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

@csrf_exempt  # Exempting from CSRF for demonstration purposes only
@require_POST
def run_rnaview(request):
    # Get the file from the request
    file = request.FILES.get('file')
    if file:
        # Define file path (you can include a specific path if needed)
        file_path = os.path.join('uploads', file.name)

        # Write file to disk
        with default_storage.open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        # Now you can run your Python script using the saved file
        script_path = '/home/aricohen/Desktop/rnaview/run.py'

        try:
            # Call your script with the file path as an argument
            result = subprocess.run(
                ['python', script_path, file_path, file.name], 
                capture_output=True, 
                text=True,
                check=True
            )
            # You can access result.stdout, result.stderr, result.returncode here
            # No need to save again, just construct the URL
            image_path = result.stdout.strip()
            image_url = request.build_absolute_uri(default_storage.url(image_path))
            return JsonResponse({'image_url': image_url})


            # return JsonResponse({"message": "File processed", "output": result.stdout})
        except subprocess.CalledProcessError as e:
            # Handle errors in the subprocess
            return JsonResponse({"error": str(e), "output": e.stderr}, status=500)
    else:
        return JsonResponse({"error": "No file provided"}, status=400)