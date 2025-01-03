from django.db import models
from django.contrib.auth.models import User
from supabase import create_client
import os
from django.conf import settings

class Paper(models.Model):
    author_name = models.ForeignKey(User, on_delete=models.SET_NULL, blank=False, null=True)
    paper_title = models.TextField(max_length=100, blank=False, null=False)
    abstract = models.TextField(blank=False, null=False)

    type_of_paper_choices = [
        ('journal', 'Journal'),
        ('conference', 'Conference'),
        ('book', 'Book Chapter'),
    ]
    paper_type = models.CharField(choices=type_of_paper_choices, default="Journal", max_length=20)

    region_choices = [
        ('national', 'National'),
        ('international', 'International'),
    ]
    region = models.CharField(choices=region_choices, max_length=20, default="national")

    date = models.DateField(blank=False)

    department_choice = [
        ("cse", 'Computer Science And Engineering'),
        ("ece", 'Electronics And Communication Engineering'),
        ("mech", 'Mechanical Engineering'),
        ("civil", 'Civil Engineering'),
        ("aiml", 'Artificial Intelligence & Machine Learning'),
                ("aids", 'Artificial Intelligence & Data science'),
                ("Information Science and Engineering", 'Information Science and Engineering'),



    ]
    department = models.CharField(choices=department_choice, max_length=100, default="cse")

    file = models.FileField(upload_to='local_files', blank=False, null=False)
    file_url = models.URLField(blank=True, null=True)  # Store Supabase file URL

    def upload_to_supabase(self):
        """
        Separate method to handle Supabase upload
        """
        if not self.file:
            return False

        try:
            supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
            file_path = self.file.path
            
            with open(file_path, 'rb') as file_data:
                response = supabase.storage.from_('papers').upload(f"{self.file.name}", file_data)

            if response:
                # Get public URL
                self.file_url = supabase.storage.from_('papers').get_public_url(f"{self.file.name}")
                
                # Optional: Remove local file
                os.remove(file_path)
                return True
            return False
        except Exception as e:
            print(f"Supabase upload error: {e}")
            return False

    def save(self, *args, **kwargs):
        # First save to local storage
        super().save(*args, **kwargs)
        
        # Then upload to Supabase
        self.upload_to_supabase()
        
        # Save again to update file_url
        super().save(*args, **kwargs)




        
#     # from django.db import models
#     # from django.contrib.auth.models import User
#     # from django.core.validators import FileExtensionValidator

#     # # Create your models here.

#     # class Paper(models.Model):
#     #     author_name=models.ForeignKey(User,on_delete=models.SET_NULL,blank=False,null=True)
#     #     paper_title=models.CharField(max_length=100,blank=False,null=False)
#     #     abstract=models.TextField(blank=False,null=False)
        
#     #     type_of_paper_choices=[('journal', 'Journal'),
#     #         ('conference', 'Conference'),
#     #         ('book', 'Book Chapter'),
#     #         ]
#     #     paper_type=models.CharField(choices=type_of_paper_choices,default="Journal", max_length=20)

#     #     reigion_choices=[{
#     #         "national":"National",
#     #         "international":"International"
#     #     }]

#     #     reigion=models.CharField(choices=reigion_choices,max_length=20,default="national")


#     #     date=models.DateField(blank=False)

        

#     #     department_choice=[
#     #         ("cse", 'Computer Science And Engineering'),
#     #         ("ece", 'Electronics And Communication Engineering'),
#     #         ("mech", 'Mechanical Engineering'),
#     #         ("civil", 'Civil Engineering'),
#     #     ]

#     #     department=models.TextField(choices=department_choice,max_length=30,default="cse")

#     #     # only pdf allowed

#     #     file = models.FileField(upload_to='papers',blank=False,null=False)
#     #     # validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
# from django.db import models
# from django.contrib.auth.models import User
# from supabase import create_client
# import os
# from django.conf import settings

# class Paper(models.Model):
#     author_name = models.ForeignKey(User, on_delete=models.SET_NULL, blank=False, null=True)
#     paper_title = models.TextField(max_length=100, blank=False, null=False)
#     abstract = models.TextField(blank=False, null=False)

#     type_of_paper_choices = [
#         ('journal', 'Journal'),
#         ('conference', 'Conference'),
#         ('book', 'Book Chapter'),
#     ]
#     paper_type = models.CharField(choices=type_of_paper_choices, default="Journal", max_length=20)

#     region_choices = [
#         ('national', 'National'),
#         ('international', 'International'),
#     ]
#     region = models.CharField(choices=region_choices, max_length=20, default="national")

#     date = models.DateField(blank=False)

#     department_choice = [
#         ("cse", 'Computer Science And Engineering'),
#         ("ece", 'Electronics And Communication Engineering'),
#         ("mech", 'Mechanical Engineering'),
#         ("civil", 'Civil Engineering'),
#     ]
#     department = models.CharField(choices=department_choice, max_length=30, default="cse")

#     file = models.FileField(upload_to='local_files', blank=False, null=False)

#     def save(self, *args, **kwargs):
#         # Save the file locally first
#         super().save(*args, **kwargs)
#         if self.file:
#             file_path = self.file.path
#             supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
#             with open(file_path, 'rb') as file_data:
#                 response = supabase.storage.from_('papers').upload(f"{self.file.name}", file_data)

#             # Check the response
#             if response.status_code == 200:
#                 os.remove(file_path)  # Remove the local file if successfully uploaded
#             else:
#                 raise Exception("File upload to Supabase failed")

# def save(self, *args, **kwargs):
#     # Save the file locally first
#     super().save(*args, **kwargs)
#     if self.file:
#         file_path = self.file.path
#         supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
#         with open(file_path, 'rb') as file_data:
#             response = supabase.storage.from_('papers').upload(f"{self.file.name}", file_data)

#         # Check the response
#         if response.status_code == 200:
#             # Get the public URL of the uploaded file
#             file_url = supabase.storage.from_('papers').get_public_url(f"{self.file.name}")
            
#             # Insert metadata into the Supabase database
#             supabase.table('papers').insert({
#                 "author_name": self.author_name.username,
#                 "paper_title": self.paper_title,
#                 "abstract": self.abstract,
#                 "paper_type": self.paper_type,
#                 "region": self.region,
#                 "date": str(self.date),
#                 "department": self.department,
#                 "file_url": file_url,
#             }).execute()

#             # Remove the local file if successfully uploaded
#             os.remove(file_path)
#         else:
#             raise Exception("File upload to Supabase failed")
