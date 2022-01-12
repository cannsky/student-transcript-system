"""
advisor
create
    3: advisorID, name, lname
    students

existing
    4: args[3], students
    new students
    delete alumni

add student
    add by id (skipping adv by 1)

remove alumni
    scan studentlist:
        if there are alumni students:
            remove student

overlap check (get courseList by stuID)
    courses in courseList,
        check days:
            if it overlaps, check hours:
                if it also overlaps:
                    remove the course in lower semester
                    start over
"""

class Advisor:
    def __init__(self, *args):

        if len(args) == 3:
            self.advisorID = args[0]
            self.fName = args[1]
            self.lName = args[2]
            self.studentList = []

        if len(args) == 4:
            self.advisorID = args[0]
            self.fName = args[1]
            self.lName = args[2]
            self.studentList = args[3]

    def addToStudents(self, student):
        self.studentList.append(student)

    def removeFromStudents(self, student):
        for i in self.studentList:
            if i.studentID.fullID == student.studentID.fullID:
                self.studentList.remove(i)

    #def checkOverlap(self, student):