from supabase import * #for connecting supabase and the project
from django.conf import settings
from .views import *

supabase_url=settings.SUPABASE_URL
supabase_key=settings.SUPABASE_KEY
supabase= create_client(supabase_url,supabase_key)

def get_supabase_client(): # to initialize and return supabase client
    
    return supabase

# def sign_up_user(request):
#     try:
#         response=supabase.auth.register({"email":email,"password":password})
#         return response
#     except Exception as e:
#         return {"error":str(e)} 