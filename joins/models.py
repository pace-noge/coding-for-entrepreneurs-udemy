from django.db import models

# Create your models here.

class Join(models.Model):
    email = models.EmailField()
    ref_id = models.CharField(max_length=120, default="ABC", unique=True)
    ip_address = models.CharField(max_length=120, default="ABC")
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __unicode__(self):
        return self.email


    class Meta:
        unique_together = ["email", "ref_id"]


# 1) Install south and add south to settings.py in INSTALLED_APPS
# 2) Ensure Models is synced with database
# 3) Convert the model to south with: ./manage.py convert_to_south appname
# 4) Make changes to model
# 5) Run schemamigrations: ./manage.py schemigration appname --auto
# 6) Run migrate: ./manage.py migrate