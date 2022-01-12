import random
class RegisterSystem:

    def __init__(self, offeredCourses):
        self.offeredCourses = offeredCourses

    def getAvailableCourses(self, student):
        #öğrenci semestera dahil kurslar
        #öğrenci transkripti
        allTakenCourses =[]

        for i in range(len(student.transcript.transcriptList)):
            for j in range(len(student.transcript.transcriptList[i][1])):
                allTakenCourses.append(student.transcript.transcriptList[i][1][j][0])

        passedCourses = []
        failedCourses = []
        for i in reversed(student.transcript.transcriptList):
            for j in i[1]:
                if 'F' in j[1] and j[0] not in passedCourses:
                    failedCourses.append(j[0])
                else:
                    passedCourses.append(j[0])

        semesterCourses = []

        mandatoryCourses = []
        for i in self.offeredCourses:
            if i.semester <= '8':
                mandatoryCourses.append(i)

        courseNTEandUE = []
        courseFTE = []
        courseTE = []
        for i in self.offeredCourses:
            if i.semester == "11":
                courseNTEandUE.append(i)
            elif i.semester == "10":
                courseFTE.append(i)
            elif i.semester == "9":
                courseTE.append(i)

        #NTE: 2-1, 8-1
        #TE: 7-1, 8-3
        #FTE: 8-1
        #UE: 7-1

        for i in mandatoryCourses:
            if i.semester == str(student.semester):
                semesterCourses.append(i)

        if int(student.semester) == 2:
            while true:
                course = random.choice(courseNTEandUE)
                if course not in allTakenCourses:
                    semesterCourses.append(course)
                    break

        if int(student.semester) == 8:
            while true:
                courseNTE = random.choice(courseNTEandUE)
                courseFT = random.choice(courseFTE)
                if courseNTE not in allTakenCourses and courseFT not in allTakenCourses:
                    semesterCourses.append(courseNTE)
                    semesterCourses.append(courseFT)
                    break
            while true:
                course1 = random.choice(courseTE)
                course2 = random.choice(courseTE)
                course3 = random.choice(courseTE)
                if course1 != course2 and course2 != course3\
                        and course1 not in allTakenCourses\
                        and course2 not in allTakenCourses\
                        and course3 not in allTakenCourses:
                    semesterCourses.append(course1)
                    semesterCourses.append(course2)
                    semesterCourses.append(course3)
                    break

        if int(student.semester) == 7:
            while true:
                course = random.choice(courseTE)
                if course not in allTakenCourses:
                    semesterCourses.append(random.choice(courseNTEandUE))
                    break


        """
        #### TEST LOOP FOR PREREQ CHECK ####    
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
        """

        for i in semesterCourses:
            if i.prerequisites:
                for j in i.prerequisites:
                    for k in failedCourses:
                        if j.courseCode == k.courseCode:
                            semesterCourses.remove(i)
                            semesterCourses.append(k)
                            print("Student " + student.studentID.fullID + " couldn't pick " + i.courseCode +
                                  " course because it requires " + k.courseCode + " course.")

        for i in failedCourses:
            if i not in semesterCourses:
                semesterCourses.append(i)

        return semesterCourses
    