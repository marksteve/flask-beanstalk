from setuptools import setup


if __name__ == '__main__':
  setup(
    name='Flask-Beanstalk',
    version='0.0.1',
    url='https://github.com/marksteve/flask-beanstalk',
    license='MIT',
    author='Mark Steve Samson',
    author_email='hello@marksteve.com',
    description='Utilities for using Beanstalk with Flask',
    long_description=open('README.rst').read(),
    py_modules=['flask_beanstalk'],
    zip_safe=False,
    platforms='any',
    install_requires=open('requirements.txt').readlines(),
  )
