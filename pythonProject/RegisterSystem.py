class RegisterSystem:

    def __init__(self, offeredCourses):
        self.offeredCourses = offeredCourses

    def getAvailableCourses(self, student):
        #öğrenci semestera dahil kurslar
        #öğrenci transkripti

        semesterCourses = []
        for i in self.offeredCourses:
            if i.semester == str(student.semester):
                semesterCourses.append(i)



        for i in semesterCourses:
            if i.prerequisites:
                for j in student.transcript.transcriptList:
                    for k in student.transcript.transcriptList[1]:
                        for l in i.prerequisites:
                            if k[0].courseCode == l.courseCode:
                                if 'F' in k[1]:
                                    semesterCourses.remove(i)
                                    semesterCourses.append(k[0])
                                    print("Student " + student.studentID.fullID + " couldn't pick " + i.courseCode +
                                          " course because it requires " + k[0].courseCode + " course.")

        return semesterCourses

