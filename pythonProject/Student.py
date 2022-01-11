from StudentID import StudentID
class Student:
    def __init__(self, *args):

        if len(args) == 5:
            self.firstName = args[0]
            self.lastName = args[1]

            self.studentID = args[2]
            self.transcript = args[3]
            self.advisor = args[4]
            self.semester = 1
            self.completedCredits = 0
            self.courseList = []

        else:
            #firstName, lastName, studentID, transcript, advisor, semester, completedCredits
            self.firstName = args[0]
            self.lastName = args[1]
            studentID = StudentID(args[2])
            self.studentID = studentID
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

    """
    select course function(self):
        get courses according to their semester with student's semester.
        
    """