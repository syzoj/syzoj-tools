from setuptools import setup, Command
from distutils.command.build import build
from setuptools.command.install import install
from setuptools.command.bdist_egg import bdist_egg
import os
import subprocess

SETUP_DIR = os.path.dirname(os.path.abspath(__file__))
builtin_checkers = ["acmp", "caseicmp", "casencmp", "casewcmp", "dcmp", "fcmp", "hcmp", "icmp", "lcmp", "ncmp", "pointscmp", "rcmp", "rcmp4", "rcmp6", "rcmp9", "rncmp", "uncmp", "wcmp", "yesno"]
builtin_checker_files = []
for checker in builtin_checkers:
    builtin_checker_files.append("checkers/%s.cpp" % checker)
    builtin_checker_files.append("checkers/%s" % checker)

class build_checkers(Command):
    description = 'build built-in checkers'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        for checker in builtin_checkers:
            subprocess.run(["g++", os.path.join(SETUP_DIR, "syzoj_tools", "checkers", "%s.cpp" % checker), "-o", os.path.join(SETUP_DIR, "syzoj_tools", "checkers", checker), "-O2"], check=True)

class custom_bdist_egg(bdist_egg):
    def run(self):
        self.run_command('build_checkers')
        bdist_egg.run(self)

class custom_build(build):
    sub_commands = build.sub_commands + [('build_checkers', None)]

setup(name='syzoj-tools',
      version='0.1',
      description='The SYZOJ tools',
      url='http://github.com/syzoj/syzoj-tools',
      author='vincent163',
      author_email='479258741@qq.com',
      packages=['syzoj_tools', 'syzoj_tools/languages', 'syzoj_tools/types', 'syzoj_tools/checkers'],
      package_data={
        'syzoj_tools': ['checkers/testlib.h', *builtin_checker_files]
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
      ],
      cmdclass={
        'bdist_egg': custom_bdist_egg,
        'build_checkers': build_checkers,
        'build': custom_build
      }
)
