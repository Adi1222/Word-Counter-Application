from django.db import models


class Record(models.Model):
    url_1 = models.URLField(blank=False,null=False)
    content = models.TextField(max_length=1000000)

    def __str__(self):
        return self.url_1
