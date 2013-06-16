import logging

try:
  from gevent import Greenlet
  from gevent.event import Event
  import gevent
  has_gevent = True
except ImportError:
  has_gevent = False

import beanstalkc


RESERVING = 1
WORKING = 2


class Beanstalk(beanstalkc.Connection, object):

  def __init__(self, app=None):
    if app:
      self.init_app(app)
      self.app = app

  def init_app(self, app):
    conn_kwargs = {}
    for n in ('host', 'port', 'parse_yaml', 'conn_timeout'):
      v = app.config.get('BEANSTALK_' + n.upper())
      if v:
        conn_kwargs[n] = v
    super(Beanstalk, self).__init__(**conn_kwargs)


if has_gevent:

  class Worker(Greenlet):

    def __init__(self, id, tubes=(), job_timeout=60, job_max_retries=5,
                 logger=None, **kwargs):
      Greenlet.__init__(self)
      self.id = id
      self._beanstalk = beanstalkc.Connection(**kwargs)
      for tube in tubes:
        self._beanstalk.watch(tube)
      self._job_timeout = job_timeout
      self._job_max_retries = job_max_retries
      if not logger:
        logger = logging.getLogger(repr(self))
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setFormatter(
          logging.Formatter(fmt=('[%r] ' % self) + '%(message)s'),
        )
        logger.addHandler(handler)
      self._logger = logger
      self._stop_evt = Event()
      self.start()

    def __repr__(self):
      return "worker%s" % self.id

    @classmethod
    def spawn_workers(cls, count, id_func=lambda x: x, **kwargs):
      return [cls(id_func(x), **kwargs) for x in range(count)]

    @classmethod
    def stop_workers(cls, workers):
      for worker in workers:
        gevent.spawn(worker.stop)
      gevent.joinall(workers)

    def _run(self):
      self._logger.debug('started')
      while True:
        self.state = RESERVING
        job = self._beanstalk.reserve()
        self.state = WORKING
        self.work(job)
        if self._stop_evt.is_set():
          break

    def work(self, job):
      raise NotImplemented

    def stop(self):
      self._logger.debug('stopping')
      if self.state == RESERVING:
        self.kill()
      else:
        self._stop_evt.set()
        self.join(timeout=self._job_timeout)
        if not self.dead:
          self.kill()
      self._logger.debug('stopped')
