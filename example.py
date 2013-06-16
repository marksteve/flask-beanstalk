import random

from gevent import monkey
monkey.patch_all()

from flask import Flask
from flask_beanstalk import Beanstalk


app = Flask(__name__)
beanstalk = Beanstalk(app)


@app.route('/')
def index():
  secs = random.randint(0, 10)
  beanstalk.put(str(secs))
  return "placed job that sleeps for %d seconds" % secs


if __name__ == '__main__':
  app.run(debug=True)
