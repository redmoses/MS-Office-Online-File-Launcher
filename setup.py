from setuptools import setup

setup(name='poom-poom',
      version='0.1',
      description='Open office documents with Microsoft Office Online via Dropbox',
      url='https://github.com/redmoses/poom-poom',
      author='Red Moses',
      author_email='musa@redmoses.me',
      license='MIT',
      packages=['poom-poom'],
      install_requires=['dropbox'],
      zip_safe=False)