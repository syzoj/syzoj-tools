from setuptools import setup

setup(name='syzoj_tools',
      version='0.1',
      description='The SYZOJ tools',
      url='http://github.com/syzoj/syzoj-tools',
      author='vincent163',
      author_email='479258741@qq.com',
      license='MIT',
      packages=['syzoj_tools'],
      scripts=['bin/syzoj'],
	  install_requires=[
	  	'pyyaml'
	  ],
      zip_safe=False)
