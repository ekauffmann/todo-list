from django.test import TestCase, Client

from models import Task

# Create your tests here.

class TaskTest(TestCase):
    
    def test_create_task(self):
        # arrange
        count = len(Task.objects.all())
        
        # act
        task = Task(text="comprarle comida al perro")
        task.save()
        
        
        # assert
        self.assertEquals(count+1, len(Task.objects.all()))
        self.assertEquals(u"comprarle comida al perro", Task.objects.all().last().text)
        
    def test_reach_url(self):
        # arrange
        client = Client()
        # act
        response = client.get('/showtask')
        # assert
        self.assertEquals(200,response.status_code)
        
    def test_edit_url(self):
        #arrange
        client = Client()
        #act
        response = client.get('/edit-task')
        #assert
        self.assertEquals(302,response.status_code)
        
    def test_delete_url(self):
        #arrange
        client = Client()
        #act
        response = client.get('/delete-task')
        #assert
        self.assertEquals(302,response.status_code)
    
    def test_check_url(self):
        #arrange
        client = Client()
        #act
        response = client.get('/check-task')
        #assert
        self.assertEquals(302,response.status_code)
        
    def test_show_task(self):
        #arrange
        task = Task(text="lavar el auto")
        task.save()
        client = Client()
        
        #act
        response = client.get("/showtask")
        
        #assert
        self.assertContains(response, "lavar el auto")
    
    def test_post_task(self):
        # arrange
        client = Client()
        count = len(Task.objects.all())
        
        # act
        response = client.post('/submit-task', {'text' : "pasear al perro"})
        
        # assert
        self.assertEquals(302, response.status_code)
        self.assertEquals(count+1, len(Task.objects.all()))
        self.assertEquals(u'pasear al perro', Task.objects.all().last().text)
        
    def test_finish_task(self):
        #arrange
        task = Task(text="lavar al perro")
        task.save()
        initial_state = task.state
        #act
        task.state=1
        task.save()
        final_state = task.state
        #assert
        self.assertNotEquals(initial_state,final_state)
        self.assertEquals(initial_state,0)
        self.assertEquals(final_state,1)
        
    def test_check_task(self):
        #arrange
        client = Client()
        #act
        client.post('/submit-task',  {'text' : "pasear al perro"})
        t_id =  Task.objects.all().last().id
        client.post('/check-task', {'id' : t_id })
        task2 = client.get('/showtask')
        
        #assert
        self.assertContains(task2,"<td>&rarr; pasear al perro </td><td>1 </td>")
    
    def test_task_with_priority(self):
        #arrange
        task1 = Task(text="ello")
        task1.save()
        task2 = Task(text="eso")
        task2.save()
        #act
        #no hay act
        #assert
        self.assertTrue(task1.is_before(task2))
        
    def test_show_priority(self):
        #arrange
        task = Task(text="centrifugar al perro")
        task.save()
        client = Client()
        
        #act
        response = client.get("/showtask")
        
        #assert
        self.assertContains(response, "pos: 1")
        
    def test_delete_task(self):
        #arrange
        task = Task(text="lavar al perro")
        task.save()
        task2 = Task.objects.all().last()
        t_id = task2.id
        #act
        task2.delete()
        #assert
        self.assertFalse(Task.objects.all().filter(id=t_id).exists())
    
    def test_edit_task(self):
        #arrange
        task = Task(text = "lavar al perro")
        task.save()
        task2 = Task.objects.all().last()
        t_id = task2.id
        #act
        task2.text="lavar al perro y secarlo"
        task2.save()
        #assert
        self.assertEquals(u'lavar al perro y secarlo', Task.objects.all().last().text)
    def test_edit_task_in_view(self):
        #arrange
        client = Client()
        client.post('/submit-task',  {'text' : "lavar al perro"})
        t_id =  Task.objects.all().last().id
        
        #act
        client.post('/edit-task', {'id' : t_id , 'text' : "lavar y secar al perro"})
        task2 = client.get('/showtask')
        #assert
        self.assertContains(task2,"<td>&rarr; lavar y secar al perro </td>")
        
    def test_keep_priority(self):
        #arrange
        task_1 = Task(text="Lavar al perro")
        task_2 = Task(text="Centrifugar al perro")
        task_3 = Task(text="Colgar al perro")
        task_4 = Task(text="PlancharPlanchar al perro")
        task_1.save()
        task_2.save()
        task_3.save()
        task_4.save()
        #act
        task_1.delete() # c:
        task_2 = Task.objects.filter(pk=task_2.pk)[0]
        task_3 = Task.objects.filter(pk=task_3.pk)[0]
        task_4 = Task.objects.filter(pk=task_4.pk)[0]
        
        
        #assert
         
        
        self.assertEquals(1, task_2.priority)
        self.assertEquals(2, task_3.priority)
        self.assertEquals(3, task_4.priority)
        