from django.contrib import admin
from .models import StudentUser , Recruiter , Jobs , Apply

# Register your models here.
admin.site.site_header="Job Portal Admin"
admin.site.register(StudentUser)
admin.site.register(Recruiter)
admin.site.register(Jobs)
admin.site.register(Apply)

