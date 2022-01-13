from StudentID import StudentID
import random

class Student:
    def __init__(self, *args):
        self.courseNTEandUE = []
        self.courseFTE = []
        self.courseTE = []
        self.countOfNTEandUEToTake = 0
        self.countOfTEToTake = 0
        self.countOfFTEToTake = 0
        self.availableCourses = []
        self.courseList = []

        if len(args) == 5:
            self.firstName = args[0]
            self.lastName = args[1]
            self.studentID = args[2]
            self.transcript = args[3]
            self.advisor = args[4]
            self.semester = 1
            self.completedCredits = 0

        else:
            # firstName, lastName, studentID, transcript, advisor, semester, completedCredits
            self.firstName = args[0]
            self.lastName = args[1]
            studentID = StudentID(args[2])
            self.studentID = studentID
            self.transcript = args[3]
            self.advisor = args[4]
            self.semester = args[5]
            self.completedCredits = args[6]


    def addToCourses(self, course):
        self.courseList.append(course)

    def removeFromCourses(self, course):
        for i in self.courseList:
            if i.courseID == course.courseID:
                self.courseList.remove(i)

    def enrollToCourses(self):
        if countOfNTEandUEToTake > 0:
            random.choice(courseNTEandUE, countOfNTEandUEToTake)
            # CourseCode: Semester-Count
            # NTE: 2-1, 8-1
            # TE: 7-1, 8-3
            # FTE: 8-1
            # UE: 7-1.
