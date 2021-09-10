from django.db import models

# Create your models here.

class classification_ephyra(models.Model):
    # id_class            = models.CharField(max_length = 10)
    classification          = models.CharField(max_length = 100)
    question_template  = models.CharField(max_length = 100)
    answer                    = models.CharField(max_length = 100)
    
    def __str__(self):
        # return self.classification
        return '%s' % (self.classification)


class question (models.Model):
    id_class        = models.ForeignKey(classification_ephyra, on_delete=models.PROTECT, default='')
    pattern         = models.TextField(blank=True)
    objects = models.Manager()
    
    def __str__(self):
        return self.pattern
