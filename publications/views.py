
from django.shortcuts import render, redirect
from django.http import JsonResponse,HttpResponseGone,HttpResponse
from supabase import create_client,Client,SupabaseAuthClient
from dotenv import load_dotenv
from django.views.decorators.csrf import csrf_exempt
from paperpublishing.settings import EMAIL_HOST_USER    

from django.core.mail import send_mail
from django.shortcuts import render
from django.http import JsonResponse
from .forms import RequestAccessForm  
import os
import json
import requests

load_dotenv()

SUPABASE_URL = os.getenv("URL")
SUPABASE_KEY = os.getenv("KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# views.py
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        if not email or not password:
            return JsonResponse({"error": "Email and password are required."}, status=400)
        
        # Send the authentication request to Supabase
        headers = {
            "apikey": SUPABASE_KEY,
            "Content-Type": "application/json",
        }
        payload = {
            "email": email,
            "password": password,
        }
        response = requests.post(f"{SUPABASE_URL}/auth/v1/token?grant_type=password", headers=headers, json=payload)

        if response.status_code == 200:
            user_data = response.json()
            # You can store the user's information in the session here if needed
            request.session["user"] = user_data
            return redirect("/add/")
        else:
            error_message = response.json().get("error_description", "Invalid login credentials.")
            return render(request, "publications/login.html", {"error": error_message})
    
    return render(request, "publications/login.html")


@ensure_csrf_cookie
def papers(request):
    if request.method == 'GET':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            response = supabase.table('papers').select('*').execute()
            return JsonResponse({
                'message': 'Success',
                'data': response.data
            })
        elif 'download' in request.GET:
            paper_id = request.GET.get('download')
            try:
                paper = supabase.table('papers').select('*').eq('id', paper_id).execute()
                if paper.data:
                    file_path = paper.data[0]['file_path']  # Assuming this is the path in your bucket
                    file_data = supabase.storage.from_('papers').download(file_path)
                    
                    # Check if file data is returned
                    if not file_data:
                        return HttpResponse("File not found", status=404)

                    response = HttpResponse(file_data, content_type='application/pdf')
                    response['Content-Disposition'] = f'attachment; filename="{paper.data[0]["paper_title"].replace(" ", "_")}.pdf"'
                    return response
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        
    return render(request, 'publications/papers.html')





def request_access(request):
    return render(request,'publications/request_access.html')


def add_paper(request):
    if request.method == "POST":

        try:
            data = request.POST
            file = request.FILES.get("file")

            if not file:
                return render(request, 'publications/addPaper.html', 
                              {"error": "File is required."})

            # Upload the file
            file_url = upload_file(file)
            if not file_url:
                return render(request, 'publications/addPaper.html', 
                              {"error": "File upload failed."})
            print(file,"hehe")
            # Prepare paper data                                                
            paper_data = {
                "author_name": data.get("name", "Anonymous"),
                "paper_title": data.get("title"),
                "paper_type": data.get("type", "journal"),
                "region": data.get("region", "national"),
                "date": data.get("date"),
                "department": data.get("department","cse"),
                "abstract": data.get("abstract"),       
                "file_url": file_url
            }

            # Insert into Supabase
            response = supabase.table("papers").insert(paper_data).execute()
            print(response)
            if not response.data:   
                return render(request, 'publications/addPaper.html', 
                              {"error": "Failed to insert paper into the database."})

            return redirect('/papers/')

        except Exception as e:
            return render(request, 'publications/addPaper.html', 
                          {"error": f"Unexpected error: {str(e)}"})

    return render(request, 'publications/addPaper.html')



def upload_file(file):
    try:
        # Specify the bucket name
        bucket_name = "paper_bucket"  # Make sure this is your bucket name
        file_path = f"papers/{file.name}"  # Specify where the file will be stored

        # Read the file content
        file_content = file.read()
        print("before upload response")

        # Use the storage API to upload the file
        upload_response = supabase.storage.from_(bucket_name).upload(file_path, file_content)
        print("before upload response",upload_response)

        
        
        
        # Check for errors in the response      
        # if upload_response.error is None:
        #     # Generate a public URL for the uploaded file
        #     public_url = supabase.storage.from_(bucket_name).get_public_url()
        #     return public_url
        # else:
        #     print(f"Error during upload: {upload_response.error.message}")
        #     return None
        public_url=supabase.storage.from_(bucket_name).get_public_url(file_path)
        print(public_url)
        return public_url
    
    except Exception as e:
        print(f"Error uploading file: {e}")
        return None
    


def paper_detail(request, id):
    context = {
        'paper_id': id,
        'api_url': os.getenv('BUCKET_URL'),
        'api_key': os,
    }
    return render(request, 'paper-detail.html', context)



def send_request(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')
        institution = data.get('institution')
        role = data.get('role')
        purpose = data.get('purpose')

        if not all([name, email, institution, role, purpose]):
            return JsonResponse({'error': 'All fields are required'}, status=400)

        send_mail(
            'New Access Request',
            f"Name: {name}\nEmail: {email}\nInstitution: {institution}\nRole: {role}\nPurpose: {purpose}",
            os.getenv('EMAIL'),
            [os.getenv('EMAIL')],  
        )

        return JsonResponse({'message': 'Request submitted successfully!'})
    return JsonResponse({'error': 'Invalid request'}, status=400)


from django.core.mail import send_mail

@csrf_exempt
# Assuming you created a form for the request access

def request_access(request):
    if request.method == 'POST':
        form = RequestAccessForm(request.POST)
        
        if form.is_valid():
            # Get the form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            institution = form.cleaned_data['institution']
            role = form.cleaned_data['role']
            purpose = form.cleaned_data['purpose']
            
            # Construct the email body
            subject = f"New Request to Publish Paper from {name}"
            message = f"""
            A new user has requested access to submit a paper.

            Name: {name}
            Email: {email}
            Institution: {institution}
            Role: {role}
            Purpose: {purpose}
            """
            admin_email = os.getenv("email") # Admin's email address
            
            # Send the email to the admin
            send_mail(
                subject,
                message,
                admin_email,  
                [admin_email],  # To email
                fail_silently=False,
            )
            
            return redirect("/papers/")
        else:
            return JsonResponse({'message': 'Invalid form data'}, status=400)
    
    return render(request, 'publications/request_access.html', {'form': RequestAccessForm()})
    