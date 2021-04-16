from setuptools import setup


setup(
      name='isis',
      version='0.0.1.dev0',
      description='Python bindings for ISIS',
      url='https://github.com/evindunn/isis_python',
      author='Evin Dunn',
      author_email='edunn@usgs.gov',
      license='Unlicense',
      zip_safe=False,
      packages=['isis'],
      classifiers=[
            'Programming Language :: Python :: 3.6',
            "License :: OSI Approved :: The Unlicense (Unlicense)"
      ],
      python_requires='>3.5, <3.7',
      install_requires=[
            "cppyy>=1.9.5"
      ],
      entry_points={
            "console_scripts": [
                  "isis2std=isis.bin.base.isis2std:main"
            ]
      }
)
