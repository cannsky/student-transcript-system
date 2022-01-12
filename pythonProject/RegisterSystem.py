import random
class RegisterSystem:

    def __init__(self, offeredCourses):
        self.offeredCourses = offeredCourses

    def getAvailableCourses(self, student):

        #get all taken courses by the student whether it is passed or failed.
        allTakenCourses = []
        allTakenCoursesCodes = []
        for i in student.transcript.transcriptList:
            for j in i[1]:
                allTakenCourses.append(j[0])
                allTakenCoursesCodes.append(j[0].courseCode.code)

        #passed Courses and their code versions for easier use.
        passedCourses = []
        passedCoursesCodes = []

        #failed Courses and their code versions for easier use.
        failedCourses = []
        failedCoursesCodes = []

        #reason for reverse operation: if a student takes x course in 1st semester and fails,
        #takes the same x course in 2nd semester and passes, transcript will record it as
        #1st sem: FF, 2nd sem: Pass. Therefore we read the transcript reversed so we find out
        #if student passed the course at last.
        for i in reversed(student.transcript.transcriptList):
            for j in i[1]:
                if 'F' in j[1] and j[0].courseCode.code not in passedCoursesCodes:
                    failedCourses.append(j[0])
                    failedCoursesCodes.append(j[0].courseCode.code)
                else:
                    passedCourses.append(j[0])
                    passedCoursesCodes.append(j[0].courseCode.code)

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
                if course.courseCode.code not in allTakenCoursesCodes:
                    semesterCourses.append(course)
                    break

        if int(student.semester) == 8:
            while true:
                courseNTE = random.choice(courseNTEandUE)
                courseFT = random.choice(courseFTE)
                if courseNTE.courseCode.code not in allTakenCoursesCodes and courseFT.courseCode.code not in allTakenCoursesCodes:
                    semesterCourses.append(courseNTE)
                    semesterCourses.append(courseFT)
                    break
            while true:
                course1 = random.choice(courseTE)
                course2 = random.choice(courseTE)
                course3 = random.choice(courseTE)
                if course1.courseCode.code != course2.courseCode.code\
                        and course2.courseCode.code != course3.courseCode.code\
                        and course1 not in allTakenCoursesCodes\
                        and course2 not in allTakenCoursesCodes\
                        and course3 not in allTakenCoursesCodes:
                    semesterCourses.append(course1)
                    semesterCourses.append(course2)
                    semesterCourses.append(course3)
                    break

        if int(student.semester) == 7:
            while true:
                course = random.choice(courseTE)
                if course.courseCode.code not in allTakenCoursesCodes:
                    semesterCourses.append(course)
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
                for k in failedCourses:
                    if i.prerequisites.courseCode.code == k.courseCode.code:
                        semesterCourses.remove(i)
                        semesterCourses.append(k)
                        print("Student " + student.studentID.fullID + " couldn't pick " + i.courseCode.code +
                              " course because it requires " + k.courseCode.code + " course.")

        semesterCoursesCodes = []
        for i in semesterCourses:
            semesterCoursesCodes.append(i.courseCode.code)

        for i in failedCourses:
            if i.courseCode.code not in semesterCoursesCodes:
                semesterCourses.append(i)
                semesterCoursesCodes.append(i.courseCode.code)

        return semesterCourses
    