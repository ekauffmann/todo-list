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