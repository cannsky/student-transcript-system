class Student:
    def __init__(self, *args):

        if len(args) == 6:
            self.firstName = args[0]
            self.lastName = args[1]
            self.studentID = args[2]
            self.transcript = args[3]
            self.advisor = args[4]
            self.semester = 1
            self.completedCredits = args[6]
            self.courseList = []

        else:
            #firstName, lastName, studentID, transcript, advisor, semester, completedCredits
            self.firstName = args[0]
            self.lastName = args[1]
            self.studentID = args[2]
            self.transcript = args[3]
            self.advisor = args[4]
            self.semester = args[5]
            self.completedCredits = args[6]
            self.courseList = []

    def addToCourses(self, course):
        self.courseList.append(course)

    def removeFromCourses(self, course):
        for i in self.courseList:
            if i.courseID == course.courseID:
                self.courseList.remove(i)