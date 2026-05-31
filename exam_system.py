import os
import random
import student

class ExamSys:
    def __init__(self):
        self.students=[]
        self.exam_number=None
        self.load_students()

    def load_students(self):
        #读取学生名单，支持制表符和空格作为间隔，并且跳过表头
        filename="人工智能编程语言学生名单.txt"
        try:
            with open(filename,'r')as f:
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
        print(f"成功加载{len(self.students)}名学生的信息")