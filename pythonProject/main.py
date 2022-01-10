import json
import random
from enum import Enum
from Course import Course
from Student import Student
from StudentID import StudentID
from Transcript import Transcript


class JsonType(Enum):
    STUDENT = 1
    COURSE = 2


class JsonSettings:

    def __init__(self, json_type, s_id):
        self.json_type = json_type
        if self.json_type == JsonType.STUDENT:
            self.file_string = "students/" + s_id + ".json"
        else:
            self.file_string = "courses.json"


class StudentAffairs:

    def __init__(self):
        file1 = open('firstname.txt', 'r', encoding='UTF-8')
        self.firstNameList = file1.readlines()
        file1 = open('lastname.txt', 'r', encoding='UTF-8')
        self.lastNameList = file1.readlines()

    def create_random_student_list(self, count, year):
        students = []
        for i in range(count):
            student_id = StudentID(year - int(0), i + 1)
            student = Student(random.choice(self.firstNameList).strip('\n'), random.choice(self.lastNameList).strip('\n'),
                              student_id,
                              Transcript([],[], 0), "advisor", "semester", "schedule", 0)
            students.append(student)
        return students

    @staticmethod
    def create_existing_student(first_name, last_name, full_id, transcript, advisor, semester, schedule):
        student_id = StudentID(full_id)
        student = Student(first_name, last_name, student_id, transcript, advisor, semester, schedule)
        return student

    @staticmethod
    def get_dict(json_type, obj):
        obj_dict = {}
        if json_type == JsonType.STUDENT:
            obj_dict = {
                "Name": obj.firstName,
                "Surname": obj.lastName,
                "StudentID": obj.studentID.fullID,
                "AdvisorID": 150118000,
                "Completed Credits": obj.completedCredits,
                "Transcript": []
            }
            for i in range(len(obj.transcript.courseList)):
                obj_dict["Transcript"].append({
                    obj.transcript.courseList[i]: obj.transcript.letterGradeList[i]
                })
                obj_dict["Completed Credits"] += obj.transcript.courseList[i].credit
        return obj_dict

    @staticmethod
    def get_obj(json_type, data_dict):
        if json_type == JsonType.STUDENT:
            obj = Student(data_dict.name, data_dict.surname)
        else:
            obj = []
            prerequisites = []
            a = 0
            for data in data_dict:
                if data["Prerequsite"] is not None:
                    for i in range(len(obj)):
                        for j in range(len(data["Prerequsite"])):
                            if obj[i].courseCode == data["Prerequsite"][j]:
                                prerequisites.append(obj[i])
                obj.append(Course(data["Lecture Name"],
                           data["Lecture Code"],
                           data["Lecture Type"],
                           data["Semester"],
                           data["Credit"],
                           prerequisites,
                           100,
                           5,
                           None,
                           None))
                prerequisites = []
        return obj

    @staticmethod
    def write_json(json_settings, obj):
        temp_dict = StudentAffairs.get_dict(json_settings.json_type, obj)

        with open(json_settings.file_string, "x") as output_file:
            json.dump(temp_dict, output_file)

    @staticmethod
    def read_json(json_settings):

        with open(json_settings.file_string) as input_file:
            data = json.load(input_file)

        return StudentAffairs.get_obj(json_settings.json_type, data)

# StudentAffairs.save_json(x["Name"], x["Surname"])

test_courses = StudentAffairs.read_json(JsonSettings(JsonType.COURSE, None))
student_affairs = StudentAffairs()
random_students = student_affairs.create_random_student_list(100, 2018)
for student in random_students:
    StudentAffairs.write_json(JsonSettings(JsonType.STUDENT, student.studentID.fullID), student)
print(len(random_students))
