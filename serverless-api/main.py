import requests
import falcon
import json
import time

def container_status(container_id):
    res = requests.get(f'http://docker.api:3000/containers/{container_id}/json')
    body = json.loads(res.content)
    return body['State']['Status']

def container_create(python_code):
    res = requests.post('http://docker.api:3000/containers/create', json={
        'Image': 'python:3.7.4-slim',
        'Cmd': ['python', '-c', python_code]
    })
    return json.loads(res.content)['Id']

def container_start(container_id):
    return requests.post(f'http://docker.api:3000/containers/{container_id}/start')

def container_remove(container_id):
    return requests.delete(f'http://docker.api:3000/containers/{container_id}')

def container_logs(container_id):
    while container_status(container_id) in ['created', 'running']:
        time.sleep(1) 
    res = requests.get(f'http://docker.api:3000/containers/{container_id}/logs?stdout=true&stderr=true')
    return res.content.decode()

class Serverless:
    def on_post(self, req, res):
        python_code = req.bounded_stream.read().decode()
        container_id = container_create(python_code)
        start_res = container_start(container_id)
        res.body = container_logs(container_id)
        container_remove(container_id)

    def on_get(self, req, res):
        response = requests.get('http://docker.api:3000/containers/json', params=req.params)
        containers = json.loads(response.content)
        keys_of_interest = ['Id', 'Image', 'Names', 'State']
        res.media = [ {key: container[key] for key in keys_of_interest} for container in containers ]


api = falcon.API()
api.add_route('/api/serverless', Serverless())