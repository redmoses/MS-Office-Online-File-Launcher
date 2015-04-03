from setuptools import setup

setup(name='poom_poom',
      version='0.1',
      description='Open office documents with Microsoft Office Online via Dropbox',
      url='https://github.com/redmoses/poom_poom',
      author='Red Moses',
      author_email='musa@redmoses.me',
      license='MIT',
      packages=['poom_poom'],
      install_requires=['dropbox'],
      entry_points = {
        'console_scripts': ['poom-poom=poom_poom.app:main'],
      },
      include_package_data=True,
      zip_safe=False)
