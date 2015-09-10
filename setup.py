import os
from setuptools import setup

current_dir = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
  setup(
    name='Flask-Beanstalk',
    version='0.0.2',
    url='https://github.com/marksteve/flask-beanstalk',
    license='MIT',
    author='Mark Steve Samson',
    author_email='hello@marksteve.com',
    description='Utilities for using Beanstalk with Flask',
    long_description=open(os.path.join(current_dir, 'README.rst')).read(),
    py_modules=['flask_beanstalk'],
    zip_safe=False,
    platforms='any',
    install_requires=open(
      os.path.join(current_dir, 'requirements.txt'),
    ).readlines(),
  )
