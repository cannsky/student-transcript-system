import json
import random
from enum import Enum
from Course import Course
from Student import Student
from StudentID import StudentID
from Transcript import Transcript


class SystemTests:

    @staticmethod
    def test_course_prerequisites():
        student = StudentAffairs()
        test_courses = StudentAffairs.read_json(JsonSettings(JsonType.COURSE, None))
        for course in test_courses:
            print(course.courseName + " " + course.courseCode + " " + (course.semester if int(course.semester) <= 8 else "Elective"))
            if course.prerequisites is not None:
                print("##Preq##" + course.prerequisites.courseName)

    @staticmethod
    def test_random_student_creation():
        student_affairs = StudentAffairs()
        random_students = student_affairs.create_random_student_list(100, 2018)
        for student in random_students:
            print(student.firstName + " " + student.lastName + " " + student.studentID.fullID + " " + "Completed Credits: " + str(student.completedCredits))
            StudentAffairs.write_json(JsonSettings(JsonType.STUDENT, student.studentID.fullID), student)


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
        self.courses = StudentAffairs.read_json(JsonSettings(JsonType.COURSE, None))
        self.write_lecture_hours()

    def write_lecture_hours(self):

        with open("lecturehours.json") as input_file:
            data = json.load(input_file)

        return data

    def write_lecture_hours(self):

        courseHourJsonObj = []
        for course in self.courses:
            courseHourJsonObj.append([course.courseCode, [random.randint(1, 5), random.randint(1, 8)]])

        temp_dict = {
            "Lecture Hours": []
        }

        for course in courseHourJsonObj:
            temp_dict["Lecture Hours"].append(course);

        with open("lecturehours.json", "w+") as output_file:
            json.dump(temp_dict, output_file)

    def create_random_student_list(self, count, year):
        students = []
        for i in range(count):
            student_id = StudentID(year - int(0), i + 1)
            first_name = random.choice(self.firstNameList).strip('\n')
            second_name = random.choice(self.lastNameList).strip('\n')
            student = Student(first_name,
                              second_name,
                              student_id.fullID,
                              self.randomTranscript(
                                  self.courses,
                                  [student_id,
                                   first_name,
                                   second_name,
                                   4]
                              ),
                              "advisor",
                              4,
                              "schedule",
                              0)
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
                "Semester": obj.semester,
                "AdvisorID": 150118000,
                "Completed Credits": obj.completedCredits,
                "Transcript": []
            }
            for i in range(len(obj.transcript.transcriptList)):
                for j in range(len(obj.transcript.transcriptList[i])):
                    for k in range(len(obj.transcript.transcriptList[i][1])):
                        obj_dict['Transcript'].append([
                            obj.transcript.transcriptList[i][1][k][0].courseCode,
                            obj.transcript.transcriptList[i][1][k][1],
                            obj.transcript.transcriptList[i][1][k][2],
                        ])
        return obj_dict

    @staticmethod
    def get_obj(json_type, data_dict):
        if json_type == JsonType.STUDENT:
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
            for data in data_dict:
                if data["Prerequsite"] is not None:
                    for i in range(len(obj)):
                        for j in range(len(data["Prerequsite"])):
                            if obj[i].courseCode == data["Prerequsite"][j]:
                                prerequisites = obj[i]
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
                prerequisites = None
        return obj

    @staticmethod
    def write_json(json_settings, obj):
        temp_dict = StudentAffairs.get_dict(json_settings.json_type, obj)

        with open(json_settings.file_string, "w+") as output_file:
            json.dump(temp_dict, output_file)

    @staticmethod
    def read_json(json_settings):

        with open(json_settings.file_string) as input_file:
            data = json.load(input_file)

        return StudentAffairs.get_obj(json_settings.json_type, data)

    def calculateTotalCredit(self, transcriptTemplate, semesterCounter):
        totalCredit = 0
        for i in transcriptTemplate:
            if i[2] == str(semesterCounter):
                if i[1] != "FF":
                    totalCredit += int(i[0].credit[0])
        return totalCredit

    def createFailedCourseList(self, transcriptTemplate, currentSemester):
        failedCourseList = []
        num = 1
        while num < currentSemester:
            for i in transcriptTemplate:
                if str(num) == i[0].semester:
                    if i[1] == "FF":
                        failedCourseList.append(i)
            num += 1
        return failedCourseList

    def assignCourse(self, transcriptTemplate, currentSemester, letterGradeList):
        retL = []
        failedCourseList = []
        for i in transcriptTemplate:
            if i[1] == "FF":
                failedCourseList.append(i)

        semInfo = []
        n = 1
        while n < currentSemester:
            l = []
            l.insert(0, n)
            l.insert(1, self.calculateTotalCredit(transcriptTemplate, n))
            semInfo.append(l)
            n += 1
        l = []
        for t in semInfo:

            if int(t[1]) < 30 and int(t[0]) > 1:
                for j in failedCourseList:
                    if int(j[2]) < int(t[0]):
                        print("...", j[0].credit[0], j[0].courseCode, j[2], t[0])
                        tmp = []
                        tmp.insert(0, j[0])
                        tmp.insert(1, random.choice(letterGradeList))
                        tmp.insert(2, str(t[0]))
                        transcriptTemplate.append(tmp)
                        failedCourseList.remove(j)

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
                                tempList.insert(2, i.semester)
                                transcriptTemplate.append(tempList)
                                tempList = []
                            else:
                                for j in transcriptTemplate:
                                    if j[0].courseCode == i.prerequisites.courseCode and j[1] != "FF":
                                        tempList.insert(0, i)
                                        tempList.insert(1, random.choice(letterGradeList))
                                        tempList.insert(2, i.semester)
                                        transcriptTemplate.append(tempList)
                                        tempList = []

                        else:
                            if i.courseCode.split("x", 1)[0] == "NTE" or i.courseCode.split("x", 1)[0] == "UE":
                                randomListNTEandUE = []
                                for a in courseNTEandUE:
                                    if (int(a.courseCode[-4]) == int(semesterCounter / 2 + 1)):
                                        randomListNTEandUE.append(a)
                                randomCourse = random.choice(randomListNTEandUE)
                                if randomCourse.prerequisites is None:
                                    tempList.insert(0, randomCourse)
                                    tempList.insert(1, random.choice(letterGradeList))
                                    tempList.insert(2, randomCourse.semester)
                                    transcriptTemplate.append(tempList)

                                    tempList = []
                                    randomListNTEandUE = []
                                else:

                                    for j in transcriptTemplate:
                                        if (j[0].courseCode == randomCourse.prerequisites.courseCode and j[1] != "FF"):
                                            tempList.insert(0, randomCourse)
                                            tempList.insert(1, random.choice(letterGradeList))
                                            tempList.insert(2, randomCourse.semester)
                                            transcriptTemplate.append(tempList)
                                            tempList = []
                                            randomListNTEandUE = []

                            elif i.courseCode.split("x", 1)[0] == "FTE":
                                randomListFTE = []
                                for a in courseFTE:
                                    if (int(a.courseCode[-4]) == int(semesterCounter / 2 + 1)):
                                        randomListFTE.append(a)
                                randomCourse = random.choice(randomListFTE)

                                if randomCourse.prerequisites is None:
                                    tempList.insert(0, randomCourse)
                                    tempList.insert(1, random.choice(letterGradeList))
                                    tempList.insert(2, randomCourse.semester)
                                    transcriptTemplate.append(tempList)
                                    tempList = []
                                    randomListFTE = []

                                else:

                                    for j in transcriptTemplate:
                                        if (j[0].courseCode == randomCourse.prerequisites.courseCode and j[1] != "FF"):
                                            tempList.insert(0, randomCourse)
                                            tempList.insert(1, random.choice(letterGradeList))
                                            tempList.insert(2, randomCourse.semester)
                                            transcriptTemplate.append(tempList)
                                            tempList = []
                                            randomListFTE = []
                            elif i.courseCode.split("x", 1)[0] == "TE":
                                randomListTE = []
                                for a in courseTE:
                                    if (int(a.courseCode[-4]) == int(semesterCounter / 2 + 1)):
                                        randomListTE.append(a)
                                randomCourse = random.choice(randomListTE)

                                if randomCourse.prerequisites is None:
                                    tempList.insert(0, randomCourse)
                                    tempList.insert(1, random.choice(letterGradeList))
                                    tempList.insert(2, randomCourse.semester)
                                    transcriptTemplate.append(tempList)
                                    tempList = []
                                    randomListTE = []
                                else:

                                    for j in transcriptTemplate:
                                        if (j[0].courseCode == randomCourse.prerequisites.courseCode and j[1] != "FF"):
                                            tempList.insert(0, randomCourse)
                                            tempList.insert(1, random.choice(letterGradeList))
                                            tempList.insert(2, randomCourse.semester)
                                            transcriptTemplate.append(tempList)
                                            tempList = []
                                            randomListTE = []

            semesterCounter += 1

        self.assignCourse(transcriptTemplate, currentSemester, letterGradeList)
        t = Transcript(transcriptTemplate, transCriptJsonStudentInfo)
        return t

# StudentAffairs.save_json(x["Name"], x["Surname"])

SystemTests.test_course_prerequisites()