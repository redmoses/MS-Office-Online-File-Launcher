from setuptools import setup

setup(name='poom_poom',
      version='0.1',
      description='Open office documents with Microsoft Office Online',
      long_description='Open office documents with Microsoft Office Online using Dropbox.',
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Editors :: Word Processors',
        'Environment :: Console',
        'Operating System :: Linux',
        'Natural Language :: English'
      ],
      keywords='dropbox, microsoft office, office online',
      url='http://redmoses.github.io/poom-poom/',
      author='Red Moses',
      author_email='musa@redmoses.me',
      license='MIT',
      packages=['poom_poom'],
      install_requires=['dropbox'],
      entry_points = {
        'console_scripts': ['poom-poom=poom_poom.app:run'],
      },
      include_package_data=True,
      zip_safe=False)
