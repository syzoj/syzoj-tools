# SYZOJ Tools
一个为 OI 题目设计的方便的命令行工具，实现造题、验题、评测等整个评测流程

## 安装
仅支持 Python3。评测功能 **不支持** Windows 系统，其他功能可跨系统使用。
安装后运行 `pip3 install syzoj-tools` 即可安装，命令 `syzoj` 包含所有功能。

## 开始
首先，你需要创建一个文件夹，在文件夹下创建 `problem.yml` 来配置题目内容。

`problem.yml` 是一个 YAML 格式的配置文件。一个完整的配置文件示例可在 [examples/a_plus_b/problem.yml](examples/a_plus_b/problem.yml) 找到。

每道题目包含若干个“测试点”，由一对输入输出组成，是运行程序的单位；还包含若干个“子任务”，每个子任务有一定的得分，表示计分策略。

最小的配置文件示例可在 [examples/minimal/problem.yml](examples/minimal/problem.yml) 找到。[examples](examples) 文件夹里还包括了许多例子。

配置文件应该包括以下内容：

### type
表示题目的类型，默认为 `traditional`。目前仅支持 `traditional`，表示传统题。

### cases
可以是一个数，也可以是一个数组，表示测试点的配置。如果是一个数，则表示测试点的数量，所有测试点均使用默认配置。否则每个测试点包含以下项：
* `name` 可选，表示该测试点的名称。默认为该测试点的编号（从 1 开始）。
* `input-data` 可选，表示测试点的输入数据文件名，相对于题目目录（即 `problem.yml` 所在的位置）。默认为 `data/#{name}.in`。
* `answer-data` 可选，表示测试点的输出数据文件名，相对于题目目录。默认为 `data/#{name}.out`.
* `time-limit` 必选，表示时间限制。支持的单位有 `s`（秒）、`ms`（毫秒）、`us`（微秒）。例：`1000ms`
* `memory-limit` 必选，表示内存限制。支持的单位有 `KB`、`MB`、`GB`（大小写敏感）。例：`256MB`
* `input-file` 可选，表示输入文件的名称。默认使用标准输入。
* `output-file` 可选，表示输出文件的名称。默认使用标准输出。

### cases-global
表示应用于所有测试点的全局配置。和 `cases` 的配置相同，当 `cases` 内没有配置项时会使用在此处指定的相应配置项。

### subtasks
子任务配置，表示评测策略。该配置项可省略，省略时，每个测试点得分相同，总分为 100 分；否则该项是一个数组，表示若干个子任务。每个子任务包含以下项：
* `score` 必选，表示该子任务的得分；
* `testcases` 必选，表示该子任务依赖的测试点列表，用测试点的名称表示（即 `name` 项）。子任务的分数为所有测试点得分的最小值。

### checker
比较器配置，相当于 Special Judge，用于判断选手输出的得分。该配置项可省略，省略时使用内置的 `wcmp` 比较器。否则应该包含以下项:
* `type` 表示比较器类型。目前支持 `builtin`、`testlib`、`loj` 三种类型。

当比较器类型为 `builtin` 时配置项如下：
* `name` 表示选择的内置比较器，来自 <https://github.com/MikeMirzayanov/testlib/tree/master/checkers>. 支持的比较器有 "acmp", "caseicmp", "casencmp", "casewcmp", "dcmp", "fcmp", "hcmp", "icmp", "lcmp", "ncmp", "pointscmp", "rcmp", "rcmp4", "rcmp6", "rcmp9", "rncmp", "uncmp", "wcmp", "yesno".

当比较器类型为 `testlib` 时配置项如下：
* `checker` 表示比较器的文件名，后缀名必须是 `.c` 或 `.cpp`。应该使用标准的 `testlib.h` 接口。

当比较器类型为 `loj` 时配置项如下：
* `checker` 表示比较器的文件名，后缀名必须是 `.c` 或 `.cpp`。应该使用 LOJ 的比较器接口。

### languages
针对各编程语言的配置。编程语言取决于提交的源文件的后缀名。该配置项可省略，省略时启用所有编程语言并使用对应的默认配置。否则应该为每个后缀名编写一项。
* `.cpp` 表示针对 C++ 语言的选手程序的配置。
* * `flags` 可选，表示额外传给编译器的选项，必须是一个**数组**，例如 ['-O2'].
* `.c` 表示针对 C 语言的选手程序的配置。
* * `flags` 可选，表示额外传给编译器的选项，必须是一个**数组**，例如 ['-O2'].
* `.pas` 表示针对 Pascal 语言的选手程序的配置。
* * `flags` 可选，表示额外传给编译器的选项，必须是一个**数组**，例如 ['-O2'].

## 评测
配置完 `problem.yml` 后即可进行评测。命令为：`syzoj judge {file}`，其中 {file} 为待评测的文件名。
