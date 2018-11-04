from setuptools import setup

setup(name='syzoj-tools',
      version='0.1',
      description='The SYZOJ tools',
      url='http://github.com/syzoj/syzoj-tools',
      author='vincent163',
      author_email='479258741@qq.com',
      packages=['syzoj_tools', 'syzoj_tools/languages', 'syzoj_tools/types'],
      package_data={
        'syzoj_tools': ['checkers/*.cpp', 'checkers/testlib.h']
      },
      scripts=['bin/syzoj'],
	  install_requires=[
	  	'pyyaml'
	  ],
      python_requires='>=3',
      zip_safe=False,
      classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'Operating System :: Unix',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
      ]
)
