from __future__ import absolute_import

from tornado.escape import json_decode, json_encode
from tornado.ioloop import IOLoop
from tornado.log import enable_pretty_logging
from tornado.web import RequestHandler, Application, URLSpec

import tasks

enable_pretty_logging()


class TaskHandler(RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'application/json')
        self.write(json_encode({'message': "This is celery tasks demo, use POST request in order to submit a task"}))

    def post(self):
        post_json = json_decode(self.request.body)
        a = int(post_json['a'])
        b = int(post_json['b'])
        task = tasks.example_task.apply_async((a, b))
        self.set_header('Content-Type', 'application/json')
        self.write(json_encode({'id': task.id}))


class TaskResultHandler(RequestHandler):
    def get(self, id):
        task = tasks.example_task.AsyncResult(id)
        self.set_header('Content-Type', 'application/json')
        self.write(json_encode({'result': task.info}))


app = Application([
    URLSpec(r"/?", TaskHandler),
    URLSpec(r"/([A-Za-z0-9\-]+)", TaskResultHandler)
])

if __name__ == '__main__':
    app.listen(8080)
    IOLoop.instance().start()