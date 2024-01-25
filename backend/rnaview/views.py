import os
import subprocess
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils.encoding import smart_str
import requests
import time
import re
from urllib.request import urlretrieve
import gzip
import shutil

base_script_path = '/srv/www/rnascape/rnaview/'
python_path = '/home/aricohen/.conda/envs/rnascape/bin/python'

# base_script_path = '/home/aricohen/Desktop/rnaview/'
# python_path = '/home/aricohen/anaconda3/envs/RNAproDB/bin/python'

#base_script_path = '/home/raktim/rnaview/'
#python_path = '/home/raktim/anaconda3/bin/python'

def is_file_served(url):
    try:
        response = requests.head(url)
        return response.status_code == 200
    except requests.RequestException:
        return False

"""
ISSUE PDB File names will be the same
WHAT IF NO CIF
WHAT ABOUT ASSEMBLY
"""
def get_pdb_file(pdb_id):

    pdb_id = pdb_id.strip().upper()
    if not pdb_id.isalnum():
        return 'error', 'Bad PDB ID'
    
    out_gz_path = '{}/backend/media/uploads/{}-assembly1.cif.gz'.format(base_script_path, pdb_id)
    out_cif_path = '{}/backend/media/uploads/{}-assembly1.cif'.format(base_script_path, pdb_id)

    url = 'https://files.rcsb.org/download/{}-assembly1.cif.gz'.format(pdb_id)
    urlretrieve(url, out_gz_path)
    with gzip.open(out_gz_path, 'rb') as f_in:
        with open(out_cif_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    filepath = f'uploads/{pdb_id}-assembly1.cif'
    # if not os.path.exists(filepath): # if path doesn’t exist
    #     return 'error', 'Bad PDB ID'
        # while not is_download_complete():
    #     time.sleep(1)
    os.remove(out_gz_path)
    return filepath, pdb_id


def test_get(request):
    if request.method == "GET":
        return JsonResponse({'success': 'eskeetit'}, status=200)

def get_npz_file(request):
    if request.method == "GET":
        time_string = request.GET.get('timeString')
        re.sub(r'\W+', '', time_string)

        file_location = os.path.join(base_script_path, "backend/media/saved_output", "{}.npz".format(time_string))

        if os.path.exists(file_location):
            with open(file_location, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/npz")
                response['Content-Disposition'] = 'attachment; filename="{}"'.format(smart_str(os.path.basename(file_location)))
                response['Content-Length'] = os.path.getsize(file_location)
                return response
        else:
            return HttpResponse("File not found", status=404)

def get_log_file(request):
    if request.method == "GET":
        time_string = request.GET.get('timeString')
        time_string = re.sub(r'\W+', '', time_string)  # remove unwanted characters

        file_location = os.path.join(base_script_path, "backend/media/saved_output", "{}.log".format(time_string))

        if os.path.exists(file_location):
            with open(file_location, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="text/plain")
                response['Content-Disposition'] = 'attachment; filename="{}"'.format(smart_str(os.path.basename(file_location)))
                response['Content-Length'] = os.path.getsize(file_location)
                return response
        else:
            return HttpResponse("File not found", status=404)



def run_regen_plot(request):
    if request.method == "GET":
        # Define the path to your script
        rotation = request.GET.get('rotation')
        time_string = request.GET.get('timeString')

        re.sub(r'\W+', '', time_string)

        script_path = f'{base_script_path}/regen_plot.py'

        basePairAnnotation = request.GET.get('basePairAnnotation')
        circleSize = request.GET.get('circleSize')
        circleLabelSize = request.GET.get('circleLabelSize')
        arrowSize = request.GET.get('arrowSize')

        # colors
        colorA = request.GET.get('colorA')
        colorC = request.GET.get('colorC')
        colorG = request.GET.get('colorG')
        colorU = request.GET.get('colorU')
        colorX = request.GET.get('colorX')

        counter = str(request.GET.get('counter'))

        # numbers
        showNumberLabels = request.GET.get('showNumberLabels')
        numberSeparation = request.GET.get('numberSeparation')
        numberSize = request.GET.get('numberSize')

        extra_list=[circleSize, circleLabelSize, arrowSize, colorA, colorC, colorG, colorU, colorX,
                showNumberLabels, numberSeparation, numberSize, counter]
        extra_string = ','.join(extra_list)

        try:
            result = subprocess.run(
                        [python_path, script_path, time_string, rotation, basePairAnnotation, extra_string], 
                        capture_output=True, 
                        text=True,
                        check=True
                    )
            image_path = result.stdout.strip().split(',,,')[0]
            image_png_path = result.stdout.strip().split(',,,')[1]

            image_url = request.build_absolute_uri(default_storage.url(image_path))
            image_png_url = request.build_absolute_uri(default_storage.url(image_png_path))

            # Polling to check if the file is being served
            for _ in range(10):  # Number of attempts
                if is_file_served(image_url):
                    return JsonResponse({'image_url': image_url, 'time_string': time_string, 'image_png_url': image_png_url})
                time.sleep(1)  # Wait for 1 second before next attempt
            return JsonResponse({'error': 'File not ready 1'}, status=500)
        except subprocess.CalledProcessError as e:
            # Handle errors in the subprocess
            return JsonResponse({"error": str(e), "output": e.stderr}, status=500)

@csrf_exempt  # Exempting from CSRF for demonstration purposes only
@require_POST
def run_rnascape(request):
    # Get the file from the request
    counter = str(request.POST.get('counter'))
    pdbid = request.POST.get('pdbid')
    pdb_download = False
    if pdbid.strip() != '0':
        pdb_download = True

    file = request.FILES.get('file')
    additionalFile = request.FILES.get('additionalFile')
    basePairAnnotation = request.POST.get('basePairAnnotation')
    loopBulging = request.POST.get('loopBulging')

    circleSize = request.POST.get('circleSize')
    circleLabelSize = request.POST.get('circleLabelSize')
    arrowSize = request.POST.get('arrowSize')

    # colors
    colorA = request.POST.get('colorA')
    colorC = request.POST.get('colorC')
    colorG = request.POST.get('colorG')
    colorU = request.POST.get('colorU')
    colorX = request.POST.get('colorX')

    # numbers
    showNumberLabels = request.POST.get('showNumberLabels')
    numberSeparation = request.POST.get('numberSeparation')
    numberSize = request.POST.get('numberSize')

    extra_list=[circleSize, circleLabelSize, arrowSize, colorA, colorC, colorG, colorU, colorX,
                showNumberLabels, numberSeparation, numberSize, counter]
    extra_string = ','.join(extra_list)

    additional_file_path=""

    # Now you can run your Python script using the saved file
    script_path = f'{base_script_path}/run.py'

    if file or pdb_download:
        # Define file path (you can include a specific path if needed)
        if file:
            file_path = os.path.join('uploads', file.name)

            # CHECK FILE SIZE
            max_file_size = 51 * 1024 * 1024  # 51MB MAX
            if file.size > max_file_size:
                return JsonResponse({'error': 'File size exceeds the allowed limit'}, status=400)

            # Check file type (extension)
            file_extension = os.path.splitext(file.name)[1]
            if file_extension.lower() not in ['.cif', '.pdb']:
                return JsonResponse({'error': 'Invalid file type'}, status=400)


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
        if pdb_download:
            file_path, file_name = get_pdb_file(pdbid)
            if file_path == 'error':
                 return JsonResponse({"error": "Unable to download PDB File"}, status=400)
            
        try:
            # Call your script with the file path as an argument
            result = None
            if file:
                file_name = file.name
            if basePairAnnotation == "rnaview":
                result = subprocess.run(
                    [python_path, script_path, file_path, file_name, loopBulging, basePairAnnotation, extra_string, additional_file_path], 
                    capture_output=True, 
                    text=True,
                    check=True
                )
            else:
                result = subprocess.run(
                   [python_path, script_path, file_path, file_name, loopBulging, basePairAnnotation, extra_string], 
                    capture_output=True, 
                    text=True,
                    check=True
                )

            # You can access result.stdout, result.stderr, result.returncode here
            # No need to save again, just construct the URL

            image_path = result.stdout.split(',,,')[0].strip()
            time_string = result.stdout.split(',,,')[1].strip()
            image_png_path = result.stdout.split(',,,')[2].strip()

            image_url = request.build_absolute_uri(default_storage.url(image_path))
            image_png_url = request.build_absolute_uri(default_storage.url(image_png_path))

            # Polling to check if the file is being served
            for _ in range(10):  # Number of attempts
                if is_file_served(image_url):
                    return JsonResponse({'image_url': image_url, 'time_string': time_string, 'image_png_url': image_png_url})
                time.sleep(1)  # Wait for 1 second before next attempt
            return JsonResponse({'error': 'File not ready 1'}, status=500)
        except subprocess.CalledProcessError as e:
            # Handle errors in the subprocess
            return JsonResponse({"error": str(e), "output": e.stderr}, status=500)
    else:
        return JsonResponse({"error": "No file provided"}, status=400)
