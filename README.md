SYZOJ Tools [![pipeline status](https://gitlab.com/syzoj/syzoj-tools/badges/master/pipeline.svg)](https://gitlab.com/syzoj/syzoj-tools/commits/master)
===========
一个为 OI 题目设计的方便的命令行工具，实现造题、验题、评测等整个评测流程

## 安装
仅支持 Python3，需要 3.5 及以上版本。评测功能 **不支持** Windows 系统，其他功能可跨系统使用。

运行 `pip3 install syzoj-tools` 即可安装，命令 `syzoj` 包含所有功能。

也可以直接 [在此处下载](https://gitlab.com/syzoj/syzoj-tools/-/jobs/artifacts/master/browse/dist?job=build) 最新的版本（master 分支最后一次成功的编译），用 `pip3 install *.whl` 安装。

需要修改源代码时可以以如下方式安装：
```sh
git clone https://github.com/syzoj/syzoj-tools
cd syzoj-tools
pip3 install -e .
```
这样安装后可以直接修改源代码，所有修改都会反映出来。

## 开始
首先，你需要创建一个文件夹，在文件夹下创建 `problem.yml` 来配置题目内容。

`problem.yml` 是一个 YAML 格式的配置文件。一个完整的配置文件示例可在 [examples/a_plus_b/problem.yml](examples/a_plus_b/problem.yml) 找到。

每道题目包含若干个“测试点”，由一对输入输出组成，是运行程序的单位；还包含若干个“子任务”，每个子任务有一定的得分，表示计分策略。

[examples](examples) 文件夹里包括了一些题目的例子。

配置文件最少应该包含以下内容：
```yaml
type: traditional
cases: 20
cases-global:
  time-limit: 1s
  memory-limit: 512MB
```
其中，`time-limit` 表示时间限制，`memory-limit` 表示空间限制，`cases` 表示测试点的配置，此处为数字 20，表示创建 20 个使用默认配置的测试点。使用默认配置时，你需要创建 `data` 目录并在下面放置 20 组测试点，编号从 1 到 20，名称为 `data/{i}.in` 与 `data/{i}.out`。

一些常用的附加选项包括 `input-file`，表示输入文件名；以及 `output-file`，表示输出文件名，在使用文件输入输出时会很有用。

你也可以指定一个数据生成器：
```yaml
build:
  input-gen: gen.cpp
  answer-gen: std.cpp
cases-global:
  gen: true
```
其中 `input-gen` 表示输入数据生成器。默认情况下这个生成器会接受一个参数，表示测试点的编号（从 1 开始），并需要向 stdout 输出该测试点的输入数据。你也可以为每个测试点指定 `args` 选项，表示传给生成器的参数。

`answer-gen` 表示输出数据生成器。该生成器从 stdin 读入输入数据，并向 stdout 输出该测试点的输出数据。如果该题目使用标准输入输出，就可以将同样的程序用作标程。

配置数据生成器后，运行 `syzoj build` 即自动生成所有测试点的数据。

另外一个常用的选项是 [checker](#checker)，表示自定义比较器（即 Special Judge）。

你还可以配置子任务：
```yaml
subtasks:
  - score: 40
    testcases: [1, 2, 3, 4, 5, 6, 7, 8]
  - score: 60
    testcases: [9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
```
每个子任务由两项组成：`score` 与 `testcases`，分别表示该子任务的分数与包含的测试点。子任务的分数是所有测试点分数的最小值，并标准化为该子任务的分数（例如，如果测试点的分数是 60 分，而子任务的分数是 40 分，则该子任务得 24 分）。不配置子任务时，总分为 100 分，按每个测试点平均分配分数。

最后可以添加几个标程或部分分算法：
```yaml
assertions:
  - prog: std.cpp
    score: 100
  - prog: partial.cpp
    subtasks:
      - id: 0
        passed: true
      - id: 1
        passed: false
```
具体的意义见 [assertions](#assertions)。配置后用 `syzoj test` 命令即可自动测试所有的程序是否符合断言。

## 评测
配置完 `problem.yml` 后即可进行评测。命令为：`syzoj judge {file}`，其中 {file} 为待评测的文件名。第一行会显示该程序的得分，后面会显示测评的详细信息（目前比较乱）。

## 比赛
工具还支持比赛评测功能。创建一个文件夹，并创建 `contest.yml`，包含一个 `problems` 键，表示题目列表。例子可在 [examples/contest.yml](examples/contest.yml) 找到。

将选手程序放入 `players` 文件夹中，每个文件夹内应包含和题目名称相同的文件，表示源文件。

使用 `syzoj contest judge` 评测所有程序（默认不会重复评测已经评测过的选手；加 `--force` 选项强制评测所有选手）。使用 `syzoj contest export <filename>` 将选手成绩导出为 csv 格式，其中 \<filename\> 为文件名，默认为 `result.csv`。

目录下 `contest.dat` 存储比赛评测数据。如果该文件损坏，可以删除该文件解决。

## 题目配置文件
此处为所有支持的配置文件选项。

### type
表示题目的类型，默认为 `traditional`。目前仅支持 `traditional`，表示传统题。

### cases
可以是一个数，也可以是一个数组，表示测试点的配置。如果是一个数，则表示测试点的数量，所有测试点均使用默认配置。否则每个测试点包含以下项：
* `name` 可选，表示该测试点的名称。默认为该测试点的编号（从 1 开始）。
* `input-data` 可选，表示测试点的输入数据文件名，其中 `{name}` 会被替换为测试点的名称，相对于题目目录（即 `problem.yml` 所在的位置）。默认为 `data/{name}.in`。
* `answer-data` 可选，表示测试点的输出数据文件名，其中 `{name}` 会被替换为测试点的名称，相对于题目目录。默认为 `data/{name}.out`.
* `time-limit` 必选，表示时间限制。支持的单位有 `s`（秒）、`ms`（毫秒）、`us`（微秒）。例：`1000ms`
* `memory-limit` 必选，表示内存限制。支持的单位有 `KB`、`MB`、`GB`（大小写敏感）。例：`256MB`
* `input-file` 可选，表示输入文件的名称。默认使用标准输入。
* `output-file` 可选，表示输出文件的名称。默认使用标准输出。
* `gen` 可选，表示是否使用测试数据生成器生成数据，为布尔值 `true` 或 `false`。默认为 `false`。该值仅作为 `gen-input` 和 `gen-answer` 的默认值使用。
* `gen-input` 可选，表示是否使用测试数据生成器生成输入数据，为布尔值 `true` 或 `false`。默认与 `gen` 相同。
* `gen-answer` 可选，表示是否使用测试数据生成器生成输出数据，为布尔值 `true` 或 `false`。默认与 `gen` 相同。
* `args` 可选，只在需要自动生成测试点时使用，表示传递给测试数据生成器的参数。必须是一个**数组**，其中 `{name}` 会被替换为测试点的名称。默认为 `["{name}"]`。

### cases-global
表示应用于所有测试点的全局配置。和 `cases` 的配置相同，当 `cases` 内没有配置项时会使用在此处指定的相应配置项。

### subtasks
子任务配置，表示评测策略。该配置项可省略，省略时，每个测试点得分相同，总分为 100 分；否则该项是一个数组，表示若干个子任务。每个子任务包含以下项：
* `score` 必选，表示该子任务的得分；
* `testcases` 必选，表示该子任务依赖的测试点列表，用测试点的名称表示（即 `name` 项）。子任务的分数为所有测试点得分的最小值。

### checker
比较器配置，相当于 Special Judge，用于判断选手输出的得分。该配置项可省略，省略时使用内置的 `default` 比较器。否则应该包含以下项:
* `type` 表示比较器类型。目前支持 `default`、`builtin`、`testlib`、`loj`、`lemon`、`cena` 六种类型。

当比较器类型为 `default` 时配置项如下：
* 目前没有配置。

当比较器类型为 `builtin` 时配置项如下：
* `name` 表示选择的内置比较器，来自 <https://github.com/MikeMirzayanov/testlib/tree/master/checkers>. 支持的比较器有 "acmp", "caseicmp", "casencmp", "casewcmp", "dcmp", "fcmp", "hcmp", "icmp", "lcmp", "ncmp", "pointscmp", "rcmp", "rcmp4", "rcmp6", "rcmp9", "rncmp", "uncmp", "wcmp", "yesno".

当比较器类型为 `testlib` 时配置项如下：
* `checker` 表示比较器的文件名，后缀名必须是受支持的语言。应该使用标准的 `testlib.h` 接口（前三个参数分别表示输入文件、输出文件、答案文件，如果有第四个参数，则表示报告文件）。

当比较器类型为 `loj` 时配置项如下：
* `checker` 表示比较器的文件名，后缀名必须是受支持的语言。应该使用 LOJ 的比较器接口。

当比较器类型为 `lemon` 时配置项如下:
* `checker` 表示比较器的文件名，后缀名必须是受支持的语言。应该使用 lemon 的比较器接口。

当比较器类型为 `cena` 时配置项如下：
* `checker` 表示比较器的文件名，后缀名必须是受支持的语言。应该使用 Cena 的比较器接口。
* `filename` 表示文件名。用于传递输入、输出文件。

### languages
针对各编程语言的配置。编程语言取决于提交的源文件的后缀名。该配置项可省略，省略时启用所有编程语言并使用对应的默认配置。否则应该为每个后缀名编写一项。
* `.cpp` 表示针对 C++ 语言的选手程序的配置。
* * `flags` 可选，表示额外传给编译器的选项，必须是一个**数组**，例如 ['-O2'].
* `.c` 表示针对 C 语言的选手程序的配置。
* * `flags` 可选，表示额外传给编译器的选项，必须是一个**数组**，例如 ['-O2'].
* `.pas` 表示针对 Pascal 语言的选手程序的配置。
* * `flags` 可选，表示额外传给编译器的选项，必须是一个**数组**，例如 ['-O2'].

### assertions
可选，表示断言。在此处放置若干个部分分程序或满分程序，就可以用 `syzoj test` 指令检查程序是否得到期望分数。是一个数组，配置如下：
* `prog` 必选，表示程序相对于题目目录的位置。
* `score` 可选，表示程序期望得到的分数。可以是一个整数，表示分数必须等于某个值；也可以以 `>=` 或 `<=` 开头后接一个数，表示分数必须满足对应条件。
* `subtasks` 可选，是一个数组，表示检验程序的每个子任务。
* * `id` 必选，表示子任务的编号，从 `0` 开始。
* * `score` 可选，表示子任务的期望得分。
* * `passed` 可选，表示子任务是否通过。**注意：只有子任务测评被中断才算不通过，`Wrong Answer` 会中断测评，但 `Partially Correct`（即便是 0 分）不会。**
* * `last-message` 可选，表示中断子任务测评的测试点的错误信息。隐含了子任务测评被中断。
* `testcases` 可选，是一个数组，表示检验程序的每个测试点。
* * `name` 必选，表示测试点的名称。
* * `score` 可选，表示测试点的期望得分（注意要换算成 0~1 之间的小数）。

### build
可选，表示生成数据的配置。配置如下：
* `input-gen` 可选，表示生成输入数据的程序，为一个源程序文件。该程序会收到测试点 `args` 配置中指定的参数，需要向标准输出写入该测试点的输入文件。
* `answer-gen` 可选，表示生成输出数据的程序，为一个源程序文件。该程序会收到测试点 `args` 配置中指定的参数，并从标准输入读入输入数据，需要向标准输出写入该测试点的输出文件。

## 比赛配置文件
此处为所有支持的比赛配置文件选项。

### problems
必选，表示一道比赛题目，配置项如下：
* `name` 必选，表示题目名称。
* `path` 必选，表示题目路径（包含 `problem.yml` 的路径）。

### mode
可选，有两种选项，为 `subfolder` 或 `plain`。`subfolder` 表示要求建立子文件夹，每个选手提交的文件名为 `{problem.name}/{problem.name}.*`；`plain` 表示不需要建立子文件夹，文件名为 `{problem.name}.*`。默认为 `plain`。
