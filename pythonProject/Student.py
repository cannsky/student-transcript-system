class Student:
    def __init__(self, firstName, lastName, studentID, transcript, advisor, semester, schedule, completedCredits):
        self.firstName = firstName
        self.lastName = lastName
        self.studentID = studentID
        self.transcript = transcript
        self.advisor = advisor
        self.semester = semester
        self.schedule = schedule
        self.completedCredits = completedCredits
        self.courseList = []

    def addToCourses(self, course):
        self.courseList.append(course)

    def removeFromCourses(self, course):
        for i in self.courseList:
            if i.courseID == course.courseID:
                self.courseList.remove(i)