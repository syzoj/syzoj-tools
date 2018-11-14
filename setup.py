from setuptools import setup, Command
from distutils.command.build import build
from wheel.bdist_wheel import bdist_wheel
from setuptools.command.build_py import build_py
import os
import subprocess

SETUP_DIR = os.path.dirname(os.path.abspath(__file__))
builtin_checkers = ["acmp", "caseicmp", "casencmp", "casewcmp", "dcmp", "fcmp", "hcmp", "icmp", "lcmp", "ncmp", "pointscmp", "rcmp", "rcmp4", "rcmp6", "rcmp9", "rncmp", "uncmp", "wcmp", "yesno"]
builtin_files = ['include/testlib.h']
for checker in builtin_checkers:
    builtin_files.append("checkers/%s.cpp" % checker)
    builtin_files.append("checkers/%s" % checker)

class build_cpps(Command):
    description = 'build built-in cpps'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        setup_dir = self.get_finalized_command('build_py').build_lib
        for checker in builtin_checkers:
            subprocess.run(["g++", "-I", os.path.join(setup_dir, "syzoj_tools", "include"), os.path.join(setup_dir, "syzoj_tools", "checkers", "%s.cpp" % checker), "-o", os.path.join(setup_dir, "syzoj_tools", "checkers", checker), "-O2"], check=True)

class custom_bdist_wheel(bdist_wheel):
    def finalize_options(self):
        bdist_wheel.finalize_options(self)
        self.root_is_pure = False

    def get_tag(self):
        python, abi, plat = bdist_wheel.get_tag(self)
        python, abi = "py3", "none"
        if plat == "linux_x86_64":
            plat = "manylinux1_x86_64"
        elif plat == "linux_i686":
            plat = "manylinux1_i686"
        return python, abi, plat

class custom_build_py(build_py):
    def run(self):
        build_py.run(self)
        self.run_command("build_cpps")

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
        'syzoj_tools': builtin_files
      },
      entry_points={
        'console_scripts': ['syzoj=syzoj_tools:main']
      },
	  install_requires=[
	  	'ruamel.yaml'
	  ],
      python_requires='>=3.5',
      zip_safe=False,
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3 :: Only'
      ],
      cmdclass={
        'build_cpps': build_cpps,
        'build': custom_build,
        'build_py': custom_build_py,
        'bdist_wheel': custom_bdist_wheel
      }
)
