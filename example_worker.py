from gevent import monkey
monkey.patch_all()

from flask_beanstalk import Worker
import gevent


class ExampleWorker(Worker):

  def work(self, job):
    self._logger.info("got job: sleep for %r seconds" % job.body)
    gevent.sleep(int(job.body))
    self._logger.info("finished job")
    job.delete()


if __name__ == '__main__':
  print "Spawn 5 workers"
  workers = ExampleWorker.spawn_workers(5)
  try:
    while True:
      gevent.sleep(10000)
  except KeyboardInterrupt:
    ExampleWorker.stop_workers(workers)
