from django.http import HttpResponse
from django.http.response import HttpResponseNotAllowed, HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError

from .models import Edge, Node

@csrf_exempt
def create(req, name):
    if req.method not in  ['POST', 'OPTIONS']:
        return HttpResponseNotAllowed(permitted_methods=['POST', 'OPTIONS'])
    try:
        node = Node(name=name)
        node.save()
    except IntegrityError:
        return HttpResponse(status=409, content='already exists')
    return JsonResponse({'name': node.name, 'id': node.id}, status=201)

@csrf_exempt
def connect(req, from_, to):
    if req.method not in  ['POST', 'OPTIONS']:
        return HttpResponseNotAllowed(permitted_methods=['POST', 'OPTIONS'])
    
    try:
        from_ = Node.objects.get(name=from_)
    except Node.DoesNotExist:
        return HttpResponseNotFound(from_)

    try:
        to = Node.objects.get(name=to)
    except Node.DoesNotExist:
        return HttpResponseNotFound(to)
    
    res = True
    try:
        Edge(start=from_.name, end=to.name).save()
    except IntegrityError:
        res = True
    except:
        res = False
    
    return JsonResponse(res, safe=False)
    

def shortestpath(req, start, end):
    if req.method != 'GET':
        return HttpResponseNotAllowed(permitted_methods=['GET'])
    try:
        start = Node.objects.get(name=start)
    except Node.DoesNotExist:
        return HttpResponseNotFound(start)

    try:
        end = Node.objects.get(name=end)
    except Node.DoesNotExist:
        return HttpResponseNotFound(end)

    res = Edge.get_shortestpath(start.name, end.name)

    if len(res) == 0:
        return HttpResponseNotFound()
    return JsonResponse({'Path': res[0].path.replace('->', ',')})
