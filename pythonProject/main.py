import json
import random
import re
from os import listdir
from os.path import isfile, join
from enum import Enum
from Course import Course, CourseCode, Semester, Schedule
from Student import Student
from StudentID import StudentID
from Transcript import Transcript
from RegisterSystem import RegisterSystem
from Advisor import Advisor



class SystemTests:

    @staticmethod
    def test_course_prerequisites(student_affairs):
        test_courses = StudentAffairs.read_json(JsonSettings(JsonType.COURSE, None))
        for course in test_courses:
            if course.prerequisites is not None:
                print()
        return test_courses

    @staticmethod
    def test_random_student_creation(student_affairs):
        random_students = student_affairs.create_random_student_list(400, 2022)
        for student in random_students:
            StudentAffairs.write_json(JsonSettings(JsonType.STUDENT, student.studentID.fullID), student)
        return random_students


class JsonType(Enum):
    STUDENT = 1,
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
        self.semesters = []
        for i in range(0, 8): self.semesters.append(Semester())
        file1 = open('firstname.txt', 'r', encoding='UTF-8')
        self.firstNameList = file1.readlines()
        file1 = open('lastname.txt', 'r', encoding='UTF-8')
        self.lastNameList = file1.readlines()
        self.courses = StudentAffairs.read_json(JsonSettings(JsonType.COURSE, None), self)

    def get_courses(self):
        return self.courses

    @staticmethod
    def read_lecture_hours():

        with open("lecturehours.json") as input_file:
            data = json.load(input_file)

        return data

    def write_lecture_hours(self):
        courseHourJsonObj = []

        list = [
            [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7], [1, 8],
            [2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6], [2, 7], [2, 8],
            [3, 1], [3, 2], [3, 3], [3, 4], [3, 5], [3, 6], [3, 7], [3, 8],
            [4, 1], [4, 2], [4, 3], [4, 4], [4, 5], [4, 6], [4, 7], [4, 8],
            [5, 1], [5, 2], [5, 3], [5, 4], [5, 5], [5, 6], [5, 7], [5, 8]
        ]
        a = 1
        while a <= 8:
            temp = list.copy()
            for i in self.courses:
                if int(i.semester) == a:
                    if i.courseType == "Mandatory":
                        courseHourJsonObj.append([i.courseCode.code])
                        for j in range(int(i.theoreticalHours)):
                            choice = random.choice(temp)
                            courseHourJsonObj[len(courseHourJsonObj) - 1].append(choice)
                            temp.remove(choice)

            temp = list.copy()
            a += 1

        while a<= 11:
            for i in self.courses:
                if int(i.semester) == a:
                    courseHourJsonObj.append([i.courseCode.code])
                    for j in range(int(i.theoreticalHours)):
                        courseHourJsonObj[len(courseHourJsonObj) - 1].append([random.randint(1, 5), random.randint(1, 8)])
            a += 1

        temp_dict = {
            "Lecture Hours": []
        }

        for course in courseHourJsonObj:
            temp_dict["Lecture Hours"].append(course);

        with open("lecturehours.json", "w+") as output_file:
            json.dump(temp_dict, output_file)

    @staticmethod
    def write_lecture_problems(list1, list2, list3):
            
        temp_dict = [] 
        for item in list1:
            string = str(item[1]) +  " STUDENTS COULDN'T REGISTER FOR A " + item[0]+ " THIS SEMESTER"
            temp_dict.append(string)
        for item in list2:
            string = str(item[1]) +  " STUDENTS COULDN'T REGISTER FOR A " + item[0]+ " THIS SEMESTER DUE TO QUOTA"           
            temp_dict.append(string)
        for item in list3:
            string = str(item[1]) +  " STUDENTS COULDN'T REGISTER FOR A " + item[0]+ " THIS SEMESTER DUE TO SCHEDULE CONFLICT"                      
            temp_dict.append(string)
            
            
        json_object = json.dumps(temp_dict, indent = 1)
        with open("registerlog.json", "w") as outfile:
            outfile.write(json_object)
            
            

    def create_random_student_list(self, count, year):
        students = []
        num = 1
        for i in range(400):

            if((i+1) % 50 == 0):
                s = int(i / 50) + 1
            else:
                s = int(i/50) + 1
            student_id = StudentID(year - int(i/100), num)
            first_name = random.choice(self.firstNameList).strip('\n')
            second_name = random.choice(self.lastNameList).strip('\n')
            student = Student(first_name,
                              second_name,
                              student_id,
                              self.randomTranscript(
                                  self.courses,
                                  [student_id,
                                   first_name,
                                   second_name,
                                   s]
                              ),
                              s)
            students.append(student)
            num+=1
            if num==101:
                num=1
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
                "Semester": obj.semester,
                "AdvisorID": 150118000,
                "Completed Credits": obj.transcript.creditCompleted,
                "Transcript": []
            }
            for semester in obj.transcript.transcriptList:
                for semesterCourses in semester[1]:
                        obj_dict['Transcript'].append([
                            semesterCourses[0].courseCode.code,
                            semesterCourses[1],
                            semesterCourses[2]
                        ])

        return obj_dict

    def get_obj(self, json_type, data_dict):
        if json_type == JsonType.STUDENT:
            for course in data_dict["Transcript"]:
                for available_course in self.courses:
                    if available_course.courseCode.code == course[0]:
                        course[0] = available_course
            obj = Student(data_dict["Name"],
                          data_dict["Surname"],
                          data_dict["StudentID"],
                          Transcript(
                              data_dict["Transcript"],
                              [data_dict["StudentID"],
                               data_dict["Name"],
                               data_dict["Surname"],
                               data_dict["Semester"]]
                          ),
                          data_dict["AdvisorID"],
                          data_dict["Semester"],
                          "schedule",
                          data_dict["Completed Credits"])
        else:
            obj = []
            prerequisites = None
            a = 0
            lecture_hours = StudentAffairs.read_lecture_hours()
            for data in data_dict:
                schedules = []
                if int(data["Semester"]) <= 8:
                    if(data["Lecture Type"] != "Elective"):
                        for i in range(1, len(lecture_hours["Lecture Hours"][a])):
                            schedules.append(Schedule(lecture_hours["Lecture Hours"][a][i][0], lecture_hours["Lecture Hours"][a][i][1]))
                        a += 1
                else:
                    if(data["Lecture Type"] != "Mandatory"):
                        for i in range(1, len(lecture_hours["Lecture Hours"][a])):
                            schedules.append(Schedule(lecture_hours["Lecture Hours"][a][i][0], lecture_hours["Lecture Hours"][a][i][1]))
                        a += 1
                if data["Prerequsite"] is not None:
                    for i in range(len(obj)):
                        for j in range(len(data["Prerequsite"])):
                            if obj[i].courseCode.code == data["Prerequsite"][j]:
                                prerequisites = obj[i]
                str = ""
                integer = 0
                list = re.findall(r'[^0-9]', data["Lecture Code"])
                list2 = re.findall(r'\d+', data["Lecture Code"])
                for i in list: str += i
                for i in list2: integer = i
                obj.append(Course(data["Lecture Name"],
                           CourseCode(
                               str,
                               integer
                           ),
                           data["Lecture Type"],
                           data["Semester"],
                           data["Credit"],
                           prerequisites,
                           100,
                           None,
                           schedules,
                           data["Theoretical Lecture Hours"]))
                prerequisites = None
        return obj

    @staticmethod
    def write_json(json_settings, obj):
        temp_dict = StudentAffairs.get_dict(json_settings.json_type, obj)

        with open(json_settings.file_string, "w+") as output_file:
            json.dump(temp_dict, output_file)

    @staticmethod
    def read_json(json_settings, sa):

        with open(json_settings.file_string) as input_file:
            data = json.load(input_file)

        return sa.get_obj(json_settings.json_type, data)

    @staticmethod
    def read_all_students_json(sa):

        students = []

        onlyfiles = [f for f in listdir("students") if isfile(join("students", f))]

        for filename in onlyfiles:
            with open("students/" + filename) as input_file:
                data = json.load(input_file)
            students.append(sa.get_obj(JsonType.STUDENT, data))

        return students

    def assignCourse(self, transcriptTemplate, currentSemester, letterGradeList):
        failedCourseList = []
        for i in transcriptTemplate:
            if i[1] == "FF":
                failedCourseList.append(i)

        for a in failedCourseList:
            if int(a[0].semester)+2 <= (currentSemester-1):
                takenSemester = int(a[2])
                takenSemester += 2
                tmp = []
                tmp.insert(0, a[0])
                tmp.insert(1, random.choice(letterGradeList))
                tmp.insert(2, str(takenSemester))
                transcriptTemplate.append(tmp)

    def randomTranscript(self, wholeCourseList, transCriptJsonStudentInfo):
        letterGradeList = ["AA", "BA", "BB", "BC", "CC", "DC", "DD", "FD", "FF"]
        currentSemester = transCriptJsonStudentInfo[3]
        semesterLimit = currentSemester - 1
        courseNTEandUE = []
        courseFTE = []
        courseTE = []
        transcriptTemplate = []
        totalCredit = 0
        for i in wholeCourseList:
            if i.semester == "11":
                courseNTEandUE.append(i)
            if i.semester == "10":
                courseFTE.append(i)
            if i.semester == "9":
                courseTE.append(i)

        totalCredit = 0
        tempList = []
        semesterCounter = 1
        while (semesterCounter <= semesterLimit):

            if semesterCounter == 1:
                for i in wholeCourseList:
                    if str(semesterCounter) == i.semester:
                        tempList.insert(0, i)
                        tempList.insert(1, random.choice(letterGradeList))
                        tempList.insert(2, i.semester)
                        transcriptTemplate.append(tempList)
                        tempList = []

            elif semesterCounter > 1:
                for i in wholeCourseList:
                    if str(semesterCounter) == i.semester:

                        if i.courseType == "Mandatory":
                            if i.prerequisites is None:
                                tempList.insert(0, i)
                                tempList.insert(1, random.choice(letterGradeList))
                                tempList.insert(2, semesterCounter)
                                transcriptTemplate.append(tempList)
                                tempList = []
                            else:
                                for j in transcriptTemplate:
                                    if (j[0].courseCode.code == i.prerequisites.courseCode.code and j[1] != "FF"):
                                        tempList.insert(0, i)
                                        tempList.insert(1, random.choice(letterGradeList))
                                        tempList.insert(2, semesterCounter)
                                        transcriptTemplate.append(tempList)
                                        tempList = []

                        else:
                            if i.courseCode.code.split("x", 1)[0] == "NTE" or i.courseCode.code.split("x", 1)[0] == "UE":

                                randomCourse = random.choice(courseNTEandUE)
                                courseNTEandUE.remove(randomCourse)
                                if randomCourse.prerequisites is None:
                                    tempList.insert(0, randomCourse)
                                    tempList.insert(1, random.choice(letterGradeList))
                                    tempList.insert(2, semesterCounter)
                                    transcriptTemplate.append(tempList)
                                    tempList = []
                                else:

                                    for j in transcriptTemplate:
                                        if (j[0].courseCode.code == randomCourse.prerequisites.courseCode.code and j[1] != "FF"):
                                            tempList.insert(0, randomCourse)
                                            tempList.insert(1, random.choice(letterGradeList))
                                            tempList.insert(2, semesterCounter)
                                            transcriptTemplate.append(tempList)
                                            tempList = []

                            elif i.courseCode.code.split("x", 1)[0] == "FTE":

                                randomCourse = random.choice(courseFTE)
                                courseFTE.remove(randomCourse)
                                if randomCourse.prerequisites is None:
                                    tempList.insert(0, randomCourse)
                                    tempList.insert(1, random.choice(letterGradeList))
                                    tempList.insert(2, semesterCounter)
                                    transcriptTemplate.append(tempList)
                                    tempList = []
                                else:

                                    for j in transcriptTemplate:
                                        if (j[0].courseCode.code == randomCourse.prerequisites.courseCode.code and j[1] != "FF"):
                                            tempList.insert(0, randomCourse)
                                            tempList.insert(1, random.choice(letterGradeList))
                                            tempList.insert(2, semesterCounter)
                                            transcriptTemplate.append(tempList)
                                            tempList = []
                            elif i.courseCode.code.split("x", 1)[0] == "TE":

                                randomCourse = random.choice(courseTE)
                                courseTE.remove(randomCourse)

                                if randomCourse.prerequisites is None:
                                    tempList.insert(0, randomCourse)
                                    tempList.insert(1, random.choice(letterGradeList))
                                    tempList.insert(2, semesterCounter)
                                    transcriptTemplate.append(tempList)
                                    tempList = []
                                else:

                                    for j in transcriptTemplate:
                                        if (j[0].courseCode.code == randomCourse.prerequisites.courseCode.code and j[1] != "FF"):
                                            tempList.insert(0, randomCourse)
                                            tempList.insert(1, random.choice(letterGradeList))
                                            tempList.insert(2, semesterCounter)
                                            transcriptTemplate.append(tempList)
                                            tempList = []

            semesterCounter += 1

        self.assignCourse(transcriptTemplate, currentSemester, letterGradeList)
        t = Transcript(transcriptTemplate, transCriptJsonStudentInfo)
        return t

# StudentAffairs.save_json(x["Name"], x["Surname"])

student_affairs = StudentAffairs()

studentList = SystemTests.test_random_student_creation(student_affairs)

sms =input("ENTER THE SEMESTER (FALL/SPRING)")


advisor = Advisor("1501180000","Borahan","Tümer",studentList);
regSys = RegisterSystem(StudentAffairs.read_json(JsonSettings(JsonType.COURSE, None), student_affairs), sms,advisor)
regSys.getAvailableCourses(studentList[0])



all_logs = []
for i in range(len(studentList)):
    if(regSys.currentSemester=="fall" and studentList[i].semester % 2 == 1):
        regSys.getAvailableCourses(studentList[i])
        studentList[i].enrollToCourses();
    elif(regSys.currentSemester=="spring" and studentList[i].semester % 2 == 0):
        regSys.getAvailableCourses(studentList[i])
        studentList[i].enrollToCourses();   
    all_logs.append(regSys.advisor.checkStudentWishList(regSys.advisor.studentList[i]))


print("********************************************************************************************************************************************************************************")

total_non_registered_0 = []
total_non_registered_1 = []
course_list_0 = []
course_list_1 = []
total_non_registered_2 = []
course_list_2 = []
for i in all_logs:
    for j in i:
        if(j[2] == 0):
            total_non_registered_0.append([j[0],j[1]])
            course_list_0.append(j[1])
        elif(j[2] == 1):
            total_non_registered_1.append([j[0],j[1]])
            course_list_1.append(j[1]) 
        elif(j[2] == 2):
            total_non_registered_2.append([j[0],j[1]])
            course_list_2.append(j[1])          
            

temp_0 = set(course_list_0)
temp_1 = set(course_list_1)
temp_2 = set(course_list_2)

new_list_0 = []   #Can't Registered
new_list_1 = []   #Due to quota
new_list_2 = []   #Due to scheduling

for j in temp_0:
    count = 0
    for i in total_non_registered_0:
        if j == i[1]:
            count +=1
    new_list_0.append([j,count])
    
    
for j in temp_1:
    count = 0
    for i in total_non_registered_1:
        if j == i[1]:
            count +=1
    new_list_1.append([j,count])

for j in temp_2:
    count = 0
    for i in total_non_registered_2:
        if j == i[1]:
            count +=1
    new_list_2.append([j,count])
    

for i in studentList:
    i.updateTranscript()
    StudentAffairs.write_json(JsonSettings(JsonType.STUDENT, i.studentID.fullID), i)


student_affairs.write_lecture_problems(new_list_0, new_list_1, new_list_2)


