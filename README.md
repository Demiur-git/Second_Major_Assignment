# 孙旭泽-25361141-第二次人工智能编程作业
仓库链接: https://github.com/Demiur-git/Second_Major_Assignment
## 1. 任务拆解与 AI 协作策略
步骤1：先将代码分为三个文件，student.py，exam_system.py与main.py，分别用于编写Student类、ExamSys类与主函数
步骤2：main.py与student.py的内容相对简单，可以自行编写。将exam_system.py中ExamSys类分成__init__方法和六个要求的函数，共七个部分
步骤3：通过AI帮助编写文件读写，os库中合适的函数调用，以及类中方法定义等内容
步骤4：通过AI辅助进行debug，并且借助AI进行循环结构、具体函数使用等方面的优化
## 2. 核心 Prompt 迭代记录
初代Prompt：请用python代码帮我实现如下功能：程序启动后，应输出如下功能菜单：
===== 学生信息与考场管理系统 ===== 
1. 查询学生信息 
2. 随机点名 
3. 生成考场安排表 
4. 生成准考证文件 
+--------------------------------------------------------------------------
0. 退出系统 
请输入功能编号：
用户输入功能编号后，系统应调用相应功能函数。如果用户输入功能编号不存在，系统需给出友好的错误提示，例如：“功能编号不存在，请正确输入功能编号（0~4）：”

AI生成的问题：1.没有捕获当用户输入的内容前后有空格的异常 2.当功能执行完毕后循环结构会直接再次输出主菜单，使得刚生成的函数调用结果被主菜单顶到上方，阅读起来不方便

优化后的prompt（追问）：请帮我对run函数进行修改：
    要求1.用户输入的内容前后可能带有空格，请将这些空格自动去除
    要求2.当某个功能被执行完毕后，询问用户是否需要使用其他功能，1需要，0不需要，如果用户输入1重新输出系统主菜单，如果输入0就退出程序
## 3. Debug 与异常处理记录
1.报错类型：UnicodeDecodeError
  解决过程：通过自己Traceback加上询问AI该报错类型以及具体报错信息。最后修改了load_student()中读取“人工智能编程语言学生名单.txt”中with open(filename,"r")部分，修改为with open(filename,"r",encoding="utf-8")来匹配文件编码
2.错误描述：输入任何功能编号都会显示“功能编号不存在”
  解决方案：自己检查代码中判断功能编号是否合规的语句，发现是因为将条件逻辑搞错。最后修改了while function_number!='0' or function_number!='1' or function_number!='2' or function_number!='3' or function_number!='4',将所有or改为and
3.错误描述：AttributeError: 'ExamSys' object has no attribute 'exam_arrangement'
  解决方案，通过traceback发现只在generate_exam_arrangement中定义了exam_arrangement，而且没有加入检查一开始根目录中是否存在“考场安排表.txt”，使得直接执行编号4会提示要求先执行3。解决方案是在init方法中定义exam_arrangement并且加入检查一开始根目录中是否存在“考场安排表.txt”的功能，若存在则直接调用该文件中的信息
## 4. 人工代码审查 (Code Review)
```python
#调用os库
import os
def generate_admission_tickets(self):
        #根据已生成的考场安排为每位学生生成准考证文件
        #通过判断列表是否为空的方法，检查是否已经执行过功能3生成了考试安排表
        if self.exam_arrangement is None:
            print("请先生成考场安排表！")
            #如果没有生成过考试安排表那就提示用户并退出函数
            return
        
        #将目标文件夹命名为准考证
        folder = "准考证"
        #调用os库中的makedirs方法，如果不存在名为“准考证”的文件夹就建立文件夹，如果存在就直接正常覆盖该文件夹
        os.makedirs(folder, exist_ok=True)
        
        #对exam_arrangement中已经储存的座位号、姓名与学号进行迭代
        for seat, name, sid in self.exam_arrangement:
            #根据要求把生成的文件文件名定义为“01.txt”“02.txt”……
            filename = os.path.join(folder, f"{seat:02d}.txt")
            #打开刚生成的文件，以utf-8编码对文件进行覆写，并在写入操作结束后自动关闭文件
            with open(filename, "w", encoding="utf-8") as f:
                #按要求将准考证信息写入文件中
                f.write(f"考场座位号:{seat}\n姓名:{name}\n学号:{sid}\n")

        #输出信息，告知用户已经处理完毕
        print(f"已为所有学生生成准考证文件，保存在“{folder}”文件夹中。")
```
