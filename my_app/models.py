from django.db import models

# Create your models here.
class Search(models.Model):
    search=models.CharField(max_length=500)
    created = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.search
    # the below class make the searchs in admin to Searches
    # if you dont use this then there wiil be a searchs in your admin when you enter the data
    class Meta:
        verbose_name_plural='Searches'

    