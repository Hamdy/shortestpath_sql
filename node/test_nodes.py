from django.test import Client
from django.test.testcases import TransactionTestCase

from .models import Edge, Node

class NodeTestCase(TransactionTestCase):
    def setUp(self):
        Node.objects.all().delete()
        Edge.objects.all().delete()
        self.client = Client()


    def test_create(self):
        """
        Test Node creations
        """
        # Test other http methods
        assert len(Node.objects.all()) == 0
        assert len(Node.objects.filter(name='a')) == 0

        response = self.client.get('/node/create/a')
        assert response.status_code == 405

        response = self.client.put('/node/create/a')
        assert response.status_code == 405

        response = self.client.head('/node/create/a')
        assert response.status_code == 405

        response = self.client.delete('/node/create/a')
        assert response.status_code == 405

        assert len(Node.objects.all()) == 0
        assert len(Node.objects.filter(name='a')) == 0

        # Test API end point
        response = self.client.post('/node/create/a')
        assert response.status_code == 201
        response = response.json()
        assert 'name' in response and response['name'] == 'a'

        response = self.client.post('/node/create/b')
        assert response.status_code == 201
        response = response.json()
        assert 'name' in response and response['name'] == 'b'

        response = self.client.post('/node/create/c')
        assert response.status_code == 201
        response = response.json()
        assert 'name' in response and response['name'] == 'c'

        response = self.client.post('/node/create/d')
        assert response.status_code == 201
        response = response.json()
        assert 'name' in response and response['name'] == 'd'

        ## Verify on actual DB
        assert len(Node.objects.all()) == 4
        assert Node.objects.get(name='a').name == 'a'
        assert Node.objects.get(name='b').name == 'b'
        assert Node.objects.get(name='c').name == 'c'
        assert Node.objects.get(name='d').name == 'd'

         ## Test duplication
        response = self.client.post('/node/create/d')
        assert response.status_code == 409
        assert len(Node.objects.all()) == 4
        assert len(Node.objects.filter(name='d')) == 1

    def test_connect(self):
        """
        Test Node connections
        """
        
        a = Node.objects.create(name='a')
        b = Node.objects.create(name='b')
        c = Node.objects.create(name='c')
        d = Node.objects.create(name='d')
        e = Node.objects.create(name='e')
        f = Node.objects.create(name='f')

        assert Edge.objects.filter(start='a').count() == 0
        assert Edge.objects.filter(end='a').count() == 0

        assert Edge.objects.filter(start='b').count() == 0
        assert Edge.objects.filter(end='b').count() == 0

        assert Edge.objects.filter(start='c').count() == 0
        assert Edge.objects.filter(end='c').count() == 0

        assert Edge.objects.filter(start='d').count() == 0
        assert Edge.objects.filter(end='d').count() == 0

        assert Edge.objects.filter(start='e').count() == 0
        assert Edge.objects.filter(end='e').count() == 0

        assert Edge.objects.filter(start='f').count() == 0
        assert Edge.objects.filter(end='f').count() == 0

        # Test other http methods
        assert len(Node.objects.all()) == 6
        assert len(Node.objects.filter(name='a')) == 1
        assert len(Node.objects.filter(name='b')) == 1
        assert len(Node.objects.filter(name='c')) == 1
        assert len(Node.objects.filter(name='d')) == 1
        assert len(Node.objects.filter(name='e')) == 1
        assert len(Node.objects.filter(name='f')) == 1

        response = self.client.get('/node/connect/a/b')
        assert response.status_code == 405

        response = self.client.put('/node/connect/a/b')
        assert response.status_code == 405

        response = self.client.head('/node/connect/a/b')
        assert response.status_code == 405

        response = self.client.delete('/node/connect/a/b')
        assert response.status_code == 405

        assert len(Node.objects.all()) == 6
        assert len(Node.objects.filter(name='a')) == 1
        assert len(Node.objects.filter(name='b')) == 1
        assert len(Node.objects.filter(name='c')) == 1
        assert len(Node.objects.filter(name='d')) == 1
        assert len(Node.objects.filter(name='e')) == 1
        assert len(Node.objects.filter(name='f')) == 1
        
        assert Edge.objects.filter(start='a').count() == 0
        assert Edge.objects.filter(end='a').count() == 0

        assert Edge.objects.filter(start='b').count() == 0
        assert Edge.objects.filter(end='b').count() == 0

        assert Edge.objects.filter(start='c').count() == 0
        assert Edge.objects.filter(end='c').count() == 0

        assert Edge.objects.filter(start='d').count() == 0
        assert Edge.objects.filter(end='d').count() == 0

        assert Edge.objects.filter(start='e').count() == 0
        assert Edge.objects.filter(end='e').count() == 0

        assert Edge.objects.filter(start='f').count() == 0
        assert Edge.objects.filter(end='f').count() == 0

        # Test API end point
        response = self.client.post('/node/connect/a/b')
        assert response.status_code == 200
        response = response.json()
        assert response is True
        
        assert len(Node.objects.all()) == 6
        assert len(Node.objects.filter(name='a')) == 1
        assert len(Node.objects.filter(name='b')) == 1
        assert len(Node.objects.filter(name='c')) == 1
        assert len(Node.objects.filter(name='d')) == 1
        assert len(Node.objects.filter(name='e')) == 1
        assert len(Node.objects.filter(name='f')) == 1
        
        a = Node.objects.get(name='a')
        b = Node.objects.get(name='b')
        c = Node.objects.get(name='c')
        d = Node.objects.get(name='d')
        e = Node.objects.get(name='e')
        f = Node.objects.get(name='f')

        assert Edge.objects.filter(start='a').count() == 1
        assert Edge.objects.filter(end='a').count() == 0

        assert Edge.objects.filter(start='b').count() == 0
        assert Edge.objects.filter(end='b').count() == 1

        assert Edge.objects.filter(start='c').count() == 0
        assert Edge.objects.filter(end='c').count() == 0

        assert Edge.objects.filter(start='d').count() == 0
        assert Edge.objects.filter(end='d').count() == 0

        assert Edge.objects.filter(start='e').count() == 0
        assert Edge.objects.filter(end='e').count() == 0

        assert Edge.objects.filter(start='f').count() == 0
        assert Edge.objects.filter(end='f').count() == 0

        # b to a
        response = self.client.post('/node/connect/b/a')
        assert response.status_code == 200
        response = response.json()
        assert response is True

        assert len(Node.objects.all()) == 6
        assert len(Node.objects.filter(name='a')) == 1
        assert len(Node.objects.filter(name='b')) == 1
        assert len(Node.objects.filter(name='c')) == 1
        assert len(Node.objects.filter(name='d')) == 1
        assert len(Node.objects.filter(name='e')) == 1
        assert len(Node.objects.filter(name='f')) == 1
        
        assert Edge.objects.filter(start='a').count() == 1
        assert Edge.objects.filter(end='a').count() == 1

        assert Edge.objects.filter(start='b').count() == 1
        assert Edge.objects.filter(end='b').count() == 1

        assert Edge.objects.filter(start='c').count() == 0
        assert Edge.objects.filter(end='c').count() == 0

        assert Edge.objects.filter(start='d').count() == 0
        assert Edge.objects.filter(end='d').count() == 0

        assert Edge.objects.filter(start='e').count() == 0
        assert Edge.objects.filter(end='e').count() == 0

        assert Edge.objects.filter(start='f').count() == 0
        assert Edge.objects.filter(end='f').count() == 0


        # Test not found
        response = self.client.post('/node/connect/g/a')
        assert response.status_code == 404
        response = response.content
        assert response == b'g'

        response = self.client.post('/node/connect/a/h')
        assert response.status_code == 404
        response = response.content
        assert response == b'h'

        assert len(Node.objects.all()) == 6
        assert len(Node.objects.filter(name='a')) == 1
        assert len(Node.objects.filter(name='b')) == 1
        assert len(Node.objects.filter(name='c')) == 1
        assert len(Node.objects.filter(name='d')) == 1
        assert len(Node.objects.filter(name='e')) == 1
        assert len(Node.objects.filter(name='f')) == 1
        
        assert Edge.objects.filter(start='a').count() == 1
        assert Edge.objects.filter(end='a').count() == 1

        assert Edge.objects.filter(start='b').count() == 1
        assert Edge.objects.filter(end='b').count() == 1

        assert Edge.objects.filter(start='c').count() == 0
        assert Edge.objects.filter(end='c').count() == 0

        assert Edge.objects.filter(start='d').count() == 0
        assert Edge.objects.filter(end='d').count() == 0

        assert Edge.objects.filter(start='e').count() == 0
        assert Edge.objects.filter(end='e').count() == 0

        assert Edge.objects.filter(start='f').count() == 0
        assert Edge.objects.filter(end='f').count() == 0


        # one more time a to b
        response = self.client.post('/node/connect/a/b')
        assert response.status_code == 200
        response = response.json()
        assert response is True

        assert len(Node.objects.all()) == 6
        assert len(Node.objects.filter(name='a')) == 1
        assert len(Node.objects.filter(name='b')) == 1
        assert len(Node.objects.filter(name='c')) == 1
        assert len(Node.objects.filter(name='d')) == 1
        assert len(Node.objects.filter(name='e')) == 1
        assert len(Node.objects.filter(name='f')) == 1
        
        assert Edge.objects.filter(start='a').count() == 1
        assert Edge.objects.filter(end='a').count() == 1

        assert Edge.objects.filter(start='b').count() == 1
        assert Edge.objects.filter(end='b').count() == 1

        assert Edge.objects.filter(start='c').count() == 0
        assert Edge.objects.filter(end='c').count() == 0

        assert Edge.objects.filter(start='d').count() == 0
        assert Edge.objects.filter(end='d').count() == 0

        assert Edge.objects.filter(start='e').count() == 0
        assert Edge.objects.filter(end='e').count() == 0

        assert Edge.objects.filter(start='f').count() == 0
        assert Edge.objects.filter(end='f').count() == 0

    def test_path(self):
        """
        Test Shortest path
        """
        # create nodes

        a = Node.objects.create(name='a')
        b = Node.objects.create(name='b')
        c = Node.objects.create(name='c')
        d = Node.objects.create(name='d')
        e = Node.objects.create(name='e')
        f = Node.objects.create(name='f')
        g = Node.objects.create(name='g')
        h = Node.objects.create(name='h')
        i = Node.objects.create(name='i')
        j = Node.objects.create(name='j')
        k = Node.objects.create(name='k')
        l = Node.objects.create(name='l')
        m = Node.objects.create(name='m')
        n = Node.objects.create(name='n')
        

        # a -> b -> c -> d -> e -> f -> g -> h -> i
        # longest path
        Edge(start='a', end='b').save()
        Edge(start='b', end='c').save()
        Edge(start='c', end='d').save()
        Edge(start='d', end='e').save()
        Edge(start='e', end='f').save()
        Edge(start='f', end='g').save()
        Edge(start='g', end='h').save()
        Edge(start='h', end='i').save()

        # a -> j -> k -> l -> m -> i
        # another long path

        Edge(start='a', end='j').save()
        Edge(start='j', end='k').save()
        Edge(start='k', end='l').save()
        Edge(start='l', end='m').save()
        Edge(start='m', end='i').save()
        
        # a -> b -> c -> n -> i
        # shortest path
        Edge(start='c', end='n').save()
        Edge(start='n', end='i').save()

        # we should get 'A,B,C,N,I'
        response = self.client.get('/node/path/a/i')

        assert response.status_code == 200
        response = response.json()
        assert 'Path' in response
        path = response['Path']
        assert path.lower() == 'a,b,c,n,i'

        # disconnect c & n now we should get  a -> j -> k -> l -> m -> i
        Edge.objects.filter(start='c', end='n').delete()
        response = self.client.get('/node/path/a/i')
        assert response.status_code == 200
        response = response.json()
        assert 'Path' in response
        path = response['Path']
        assert path.lower() == 'a,j,k,l,m,i'

        # connect n to e : # a -> b -> c -> d -> e -> n -> i
        # we still obtain previous result
        Edge(start='e', end='n').save()
        response = self.client.get('/node/path/a/i')
        assert response.status_code == 200
        response = response.json()
        assert 'Path' in response
        path = response['Path']
        assert path.lower() == 'a,j,k,l,m,i'

        # disconnect n & e 
        # connect n to d 
        # a -> b -> c -> d -> n -> i
        # now we have 2 shortest paths 
        # a -> b -> c -> d -> n -> i  &
        # a -> j -> k -> l -> m -> i
        
        Edge.objects.filter(start='e', end='n').delete()
        Edge(start='d', end='n').save()
        response = self.client.get('/node/path/a/i')
        assert response.status_code == 200
        response = response.json()
        assert 'Path' in response
        path = response['Path']

        assert path.lower() == 'a,j,k,l,m,i'or path.lower() == 'a,b,c,d,n,i'
        # disconect k, l
        # now a -> b -> c -> d -> n -> i is the shortest
        Edge.objects.filter(start='k', end='l').delete()
        response = self.client.get('/node/path/a/i')
        assert response.status_code == 200
        response = response.json()
        assert 'Path' in response
        path = response['Path']
        assert path.lower() == 'a,b,c,d,n,i'

        # no shortest path when start and end are the same
        response = self.client.get('/node/path/a/a')
        assert response.status_code == 404

        # no shortest path when start/end does not exist
        response = self.client.get('/node/path/a/x')
        assert response.status_code == 404
        response = self.client.get('/node/path/x/a')
        assert response.status_code == 404
        response = self.client.get('/node/path/x/z')
        assert response.status_code == 404
        
        # only get method is allowed

        response = self.client.post('/node/path/a/i')
        assert response.status_code == 405

        response = self.client.head('/node/path/a/i')
        assert response.status_code == 405

        response = self.client.put('/node/path/a/i')
        assert response.status_code == 405

        