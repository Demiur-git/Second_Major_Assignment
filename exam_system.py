import os
import random
import student

class ExamSys:
    def __init__(self):
        self.students=[]
        self.exam_arrangement=None
        self.load_students()

    def load_students(self):
        #读取学生名单，支持制表符和空格作为间隔，并且跳过表头
        filename="人工智能编程语言学生名单.txt"
        try:
            with open(filename,'r',encoding='utf-8')as f:
                lines = f.readlines()
        except FileNotFoundError:
            print(f"未找到{filename},请确保该文件存放于文件根目录")
            exit(1)

        if not lines:
            print("错误，文件为空")
            exit(1)
        #去掉没有实际学生信息的第一行
        data_lines=lines[1:] if len(lines)>1 else []
        for line in data_lines:
            line = line.strip()
            if not line:
                continue
            #先按制表符分割，如果没有制表符则使用空格作为分割标准
            if '\t' in line:
                parts = line.split('\t')
            else:
                parts = line.split()
            #检测学生信息是否有欠缺
            if len(parts)<6:
                print(f"警告：此行学生信息有欠缺，已跳过{line}，请之后进行删除或补充")
                continue
            #按表头顺序分配变量
            number = parts[0].strip()
            name = parts[1].strip()
            gender = parts[2].strip()
            class_number = parts[3].strip()
            student_id = parts[4].strip()
            department = parts[5].strip()

            self.students.append(student.Student(number, name, gender, class_number, student_id,department))
        #输出学生总数，便于检测有没有把所有学生信息成功载入
        print(f"[系统]已成功加载{len(self.students)}名学生的信息")

    def run(self):
        #循环输出功能菜单并且进行功能调用，满足用户对于使用多项功能的需求
        while True:
            print("===== 学生信息与考场管理系统 =====")
            print("1. 查询学生信息")
            print("2. 随机点名")
            print("3. 生成考场安排表")
            print("4. 生成准考证文件")
            print("+--------------------------------------------------------------------------")
            print("0. 退出系统")
            function_number=input("请输入功能编号：").strip()
            #如果输入不是正确的编号则要求重新输入
            while function_number!='0' and function_number!='1' and function_number!='2' and function_number!='3' and function_number!='4':
                function_number=input("功能编号不存在，请正确输入功能编号（0~4）：").strip()
            #根据输入的编号调用函数
            if function_number=='0':
                print("感谢使用，系统已退出。再见")
                break
            elif function_number=='1':
                self.find_student()
            elif function_number=='2':
                self.random_roll_call()
            elif function_number=='3':
                self.generate_exam_arrangement()
            else:
                self.generate_admission_tickets()

            #功能执行完毕，询问是否需要再执行其他功能
            while True:
                again=input("功能已执行完毕，请问是否需要再执行其他功能：（1-需要执行，0-不需要执行，退出程序）").strip()
                if again=='0':
                    print("感谢使用，系统已退出。再见")
                    return
                elif again=='1':
                    break
                else:
                    print("输入无效，请输入0或1")

    def find_student(self):
        #根据学生学号来查找学生信息
        target_student_id=input("请输入你想要查找的学生的学号：").strip()
        for student in self.students:
            if student.student_id == target_student_id:
                print("已找到该学生，该学生信息如下：")
                print(f"序号：{student.number} 姓名：{student.name} 性别：{student.gender} 班级：{student.class_number} 学号：{student.student_id} 学院：{student.department}")
                return
        print("未找到该学号对应的学生，请重新检查输入是否正确")

    def random_roll_call(self):
        #根据用户需求随机点名，返回对应数量的不重复随机学生名单
        while True:
            try:
                s=input(f"请输入需要点名的学生数量（共{len(self.students)}名学生）").strip()
                n=int(s)
                if n<=0:
                    print("[输入错误]点名人数必须大于0")
                elif n>len(self.students):
                    print(f"[输入错误]点名人数（{n}）超过学生总人数（{len(self.students)}），请重新输入")
                else:
                    #先建立一个新的列表把原有列表复制过来，然后先打乱一次，再从中截取相应长度的片段再随机排列一次
                    temp_list=self.students
                    random.shuffle(temp_list)
                    chosen_student=random.sample(temp_list,n)
                    print("本次随机点名结果：")
                    #通过enumerate函数同时对序号和抽取到的学生信息进行循环输出
                    for index,student in enumerate(chosen_student,start=1):
                        print(f"{index}.{student.name}  {student.student_id}")
                    return

            except ValueError:
                print(f"[输入错误] invalid literal for int() with base 10:\'{s}\'")

    def generate_exam_arrangement(self):
        #将全班学生顺序打乱并生成考试安排表
        if not self.students:
            print("没有任何学生信息，无法生成考场安排")
            return

        temp_list=self.students
        random.shuffle(temp_list)
        arrangement=[]

        with open('考场安排表.txt','w',encoding='utf-8') as f:
            for index,student in enumerate(temp_list,start=1):
                f.write(f"{index},{student.name},{student.student_id}\n")
                arrangement.append([index,student.name,student.student_id])
        self.exam_arrangement=arrangement
        print("考试安排表已成功生成，请打开\'考试安排表.txt\'进行查看")

    def generate_admission_tickets(self):
        #根据已经生成的考场安排信息生成准考证
        #如果没有执行过3，则会先检查是不是已经存在考场安排表.txt文件
        if not self.exam_arrangement:
            if os.path.exists("考场安排表.txt"):
                print("检测到已有考场安排表，正在读取")
                self.exam_arrangement = []
                with open("考场安排表.txt", "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        index, name, student_id = line.split(',')
                        self.exam_arrangement.append([(int)(index), name, student_id])
                print("考场安排表加载成功")
            else:
                print("没有考试安排表，请先通过功能3生成考试安排表")
                return

        folder='准考证'
        os.makedirs(folder,exist_ok=True)

        for index,name,student_id in self.exam_arrangement:
            filename=os.path.join(folder,f"{index:02d}.txt")
            with open(filename,'w',encoding='utf-8') as f:
                f.write(f"考场座位号：{index}\n姓名：{name}\n学号：{student_id}\n")

        print("已经成功为所有学生生成准考证，请前往\'准考证\'文件夹中查看")