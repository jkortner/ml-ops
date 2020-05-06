from setuptools import setup, find_packages
with open("README.md", "r") as fh:
    long_description = fh.read()
# ATTENTION: the name must match the name of the top-level import package
# see Makefile variable MODULE
# naming the project as the top-level import package is also consistent with
# conventions.
setup(name="sampleproject",
      version="0.1",
      # Exclude all subpackages that contain 'tests'
      # Note: top-level tests dir requires directive in MANIFEST.in
      packages=find_packages(exclude=['tests', '*.tests', '*.tests.*']),
      # test_suite='tests',
      # Include scripts/executables for application from 'scripts' directory
      # scripts=['scripts/entrypoint'],
      # Generate start script automatically
      entry_points={'console_scripts':
                    ['entrypoint=sampleproject.sample:main']},
      setup_requires=['wheel'],
      # Define package dependencies
      # install_requires=[],
      # Defines def environment containing additional dependencies
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

      # Metadata to display on PyPI
      author="Full Name",
      # author_email="",
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
                   "License :: OSI Approved :: MIT License",
                   #  "License :: Other/Proprietary License",
                   "Operating System :: OS Independent",
                   ]
      )
