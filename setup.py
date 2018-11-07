from setuptools import setup, Command
from distutils.command.build import build
from setuptools.command.install import install
from setuptools.command.bdist_egg import bdist_egg
import os
import subprocess

SETUP_DIR = os.path.dirname(os.path.abspath(__file__))
builtin_checkers = ["acmp", "caseicmp", "casencmp", "casewcmp", "dcmp", "fcmp", "hcmp", "icmp", "lcmp", "ncmp", "pointscmp", "rcmp", "rcmp4", "rcmp6", "rcmp9", "rncmp", "uncmp", "wcmp", "yesno"]
builtin_validators = ["bipartite-graph-validator", "ival", "nval", "sval", "undirected-graph-validator", "undirected-tree-validator"]
builtin_files = []
for checker in builtin_checkers:
    builtin_files.append("checkers/%s.cpp" % checker)
    builtin_files.append("checkers/%s" % checker)
for validator in builtin_validators:
    builtin_files.append("validators/%s.cpp" % validator)
    builtin_files.append("validators/%s" % validator)

class build_cpps(Command):
    description = 'build built-in cpps'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        for checker in builtin_checkers:
            subprocess.run(["g++", "-I", os.path.join(SETUP_DIR, "syzoj_tools", "include"), os.path.join(SETUP_DIR, "syzoj_tools", "checkers", "%s.cpp" % checker), "-o", os.path.join(SETUP_DIR, "syzoj_tools", "checkers", checker), "-O2"], check=True)
        for validator in builtin_validators:
            subprocess.run(["g++", "-I", os.path.join(SETUP_DIR, "syzoj_tools", "include"), os.path.join(SETUP_DIR, "syzoj_tools", "validators", "%s.cpp" % validator), "-o", os.path.join(SETUP_DIR, "syzoj_tools", "validators", validator), "-O2"], check=True)

class custom_bdist_egg(bdist_egg):
    def run(self):
        self.run_command('build_cpps')
        bdist_egg.run(self)

class custom_build(build):
    sub_commands = build.sub_commands + [('build_cpps', None)]

setup(name='syzoj-tools',
      version='0.2',
      description='The SYZOJ tools',
      long_description='一个为 OI 题目设计的方便的命令行工具，实现造题、验题、评测等整个评测流程',
      url='http://github.com/syzoj/syzoj-tools',
      author='vincent163',
      author_email='479258741@qq.com',
      packages=['syzoj_tools', 'syzoj_tools/languages', 'syzoj_tools/types', 'syzoj_tools/checkers', 'syzoj_tools/validators'],
      package_data={
        'syzoj_tools': ['include/testlib.h', *builtin_files]
      },
      scripts=['bin/syzoj'],
	  install_requires=[
	  	'ruamel.yaml'
	  ],
      python_requires='>=3',
      zip_safe=False,
      classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'Operating System :: Unix',
        'License :: OSI Approved :: MIT License'
      ],
      cmdclass={
        'bdist_egg': custom_bdist_egg,
        'build_cpps': build_cpps,
        'build': custom_build
      }
)
