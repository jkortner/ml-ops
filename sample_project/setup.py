from setuptools import setup, find_packages
with open("README.md", "r") as fh:
    long_description = fh.read()
setup(name="SampleProject",
      version="0.1",
      packages=find_packages(),
      test_suite='tests',
      scripts=['bin/sampleproject'],
      setup_requires=['wheel'],
      install_requires=['nose',
                        'coverage',
                        'bandit',
                        'pylint',
                        'autopep8',
                        'flake8'
                        ],

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
      classifiers=[
          "Programming Language :: Python :: 3",
          #  "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ]

      # could also include url, project_urls, keywords etc.
      )
