===============
Flask-Beanstalk
===============

.. image:: http://img.shields.io/pypi/v/Flask-Beanstalk.png

Utilities for using Beanstalk with Flask

------
Client
------

``flask_beanstalk.Beanstalk`` is a simple wrapper for ``beanstalkc.Connection``
that allows reading configuration from ``app.config``.

::

  from flask import Flask
  from flask_beanstalk import Beanstalk

  app = Flask(__name__)
  beanstalk = Beanstalk(app)  # or beanstalk.init_app(app)

Configuration
=============

::

  app.config['BEANSTALK_HOST']
  app.config['BEANSTALK_PORT']
  app.config['BEANSTALK_PARSE_YAML']
  app.config['BEANSTALK_CONN_TIMEOUT']

------
Worker
------

Define and spawn workers by subclassing from ``flask_beanstalk.Worker``.
``flask_beanstalk.Worker`` inherits from ``gevent.Greenlet`` but ``gevent``
is an optional dependency in case you just want to use the client.

::

  import gevent
  from flask_beanstalk import Worker as _Worker

  class Worker(_Worker):
    def run(self, job):
      self._logger.info('Received: %r' % job.body)
      job.delete()

  workers = Worker.spawn_workers(10)
  try:
    while True:
      gevent.sleep(10000)
  except KeyboardInterrupt:
    Worker.stop_workers(workers)

----------
Try it out
----------

Install and run ``beanstalkd`` if you haven't done so yet.

::

  git clone https://github.com/marksteve/flask-beanstalk.git
  cd flask-beanstalk
  mkvirtualenv flask-beanstalk
  workon flask-beanstalk
  python setup.py develop
  python example_worker.py

On another terminal::

  workon flask-beanstalk
  python example.py

Go to localhost:5000 in your browser to send a job.
The worker should be able to accept and process it.
Try to send multiple jobs before sending a SIGINT
to the worker. Jobs being worked on should be
processed first before the worker shuts down.
