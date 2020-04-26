from setuptools import setup, find_packages
with open("README.md", "r") as fh:
    long_description = fh.read()
setup(name="sampleproject",
      version="0.1",
      # exclude all subpackages that contain 'tests'
      # note: top-level tests dir requires directive in MANIFEST.in
      packages=find_packages(exclude=['tests', '*.tests', '*.tests.*']),
      # test_suite='tests',
      scripts=['bin/sampleproject'],
      # generate start script automatically
      # entry_points={'console_scripts':
      #               ['sampleproject=sampleproject.sample:main']},
      setup_requires=['wheel'],
      # define package dependencies
      # install_requires=[],
      # defines def environment containing additional dependencies
      # (for linting, testing)
      extras_require={'dev': ['nose',
                              'coverage',
                              'bandit',
                              'pylint',
                              'autopep8',
                              'flake8']
                      },

      # package_data={
      #     # If any package contains *.txt or *.rst files, include them:
      #     "": ["*.txt", "*.rst"],
      #     # And include any *.msg files found in the "hello" package, too:
      #     "hello": ["*.msg"],
      # },

      # metadata to display on PyPI
      author="Leonard Rothacker",
      author_email="leonard.rothacker@googlemail.com",
      description="This is an Example Package",
      long_description=long_description,
      long_description_content_type='text/markdown',
      # keywords="hello world example examples",
      # url="http://example.com/HelloWorld/",   # project home page, if any
      # project_urls={
      #     "Bug Tracker": "https://bugs.example.com/HelloWorld/",
      #     "Documentation": "https://docs.example.com/HelloWorld/",
      #     "Source Code": "https://code.example.com/HelloWorld/",
      # },
      platforms=['any'],
      license='None',
      classifiers=["Programming Language :: Python :: 3",
                   #  "License :: OSI Approved :: MIT License",
                   #  "License :: Other/Proprietary License",
                   "Operating System :: OS Independent",
                   ]

      # could also include url, project_urls, keywords etc.
      )
