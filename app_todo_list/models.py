from __future__ import unicode_literals

from django.db import models
from django.db.models import F

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
    
    #def my_super_save(self, *args, **kwargs):
     #   super(Task, self).save(*args, **kwargs)

        
    
    def delete(self, *args, **kwargs):
        old_priority = self.priority
        super(Task, self).delete(*args, **kwargs)
        Task.objects.filter(priority__gt=old_priority).update(priority=F('priority')-1)
            
    def is_before(self, other_task):
        return self.priority < other_task.priority
        