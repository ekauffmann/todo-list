from __future__ import unicode_literals

from django.db import models


# Create your models here.

class Task(models.Model):
            
    text = models.TextField()
    state = models.IntegerField(default=0)
    priority = models.IntegerField(default=0, unique=True)
    
    def save(self, *args, **kwargs):
        if self.priority == 0:
            max_priority = Task.objects.aggregate(models.Max('priority'))['priority__max']
            if max_priority is None:
                max_priority = 0
            self.priority = max_priority+1
        super(Task, self).save(*args, **kwargs)
        
    def is_before(self, other_task):
        return self.priority < other_task.priority
        