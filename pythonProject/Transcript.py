#################### düzenlenmiş transcript
class Transcript:
    letterGradeDict = {
        "AA": 4.00,
        "BA": 3.50,
        "BB": 3.00,
        "BC": 2.50,
        "CC": 2.00,
        "DC": 1.50,
        "DD": 1.00,
        "FD": 0.50,
        "FF": 0.00,
    }

    # transcriptList = [
    #       [semester, [taken course objects list], creditTaken , creditCompleted , scoreSemester  , gpa , cgpa ],
    #       [semester, [taken course objects list], creditTaken , creditCompleted , scoreSemester , gpa , cgpa ],
    #                                              ....
    #                                              ....
    #            ] Note = taken course objects list be like = [course obj , lettergrade , taken semester]

    # transcriptTemplate = [ [course , letter grade , taken semester ],
    #                        [course , letter grade , taken semester ],                                        ,
    #                                        ....                    ]

    def __init__(self, transcriptTemplate, transCriptJsonStudentInfo):
        self.ID = transCriptJsonStudentInfo[0]
        self.fName = transCriptJsonStudentInfo[1]
        self.lName = transCriptJsonStudentInfo[2]
        self.currentSemester = transCriptJsonStudentInfo[3]
        self.transcriptList = self.calcSemestersDetails(transcriptTemplate, self.currentSemester)

    # list = [ [semester, [taken course objects], creditTaken , creditCompleted , scoreSemester , gpa , cgpa ],
    def calcSemestersDetails(self, transcriptTemplate, currentSemester):
        tempTranscriptList = []
        tListTemplate = []
        currSemesterCourses = []
        sem = 1
        while sem < currentSemester:
            tListTemplate.insert(0, sem)
            for i in transcriptTemplate:
                if i[2] == str(sem):
                    currSemesterCourses.append(i)
            tListTemplate.insert(1, currSemesterCourses)
            creditTaken = self.calcCreditTaken(currSemesterCourses)
            tListTemplate.insert(2, creditTaken)
            tListTemplate.insert(3, self.calcCreditCompleted(currSemesterCourses))
            score = self.calcScoreSemester(currSemesterCourses)
            tListTemplate.insert(4, score)
            gpa = (self.calcGPA(score, creditTaken))
            gpaStr = str(gpa)[:4]
            gpa = Decimal(gpaStr)
            tListTemplate.insert(5, gpa)
            tListTemplate.insert(6, None)
            tempTranscriptList.append(tListTemplate)

            currSemesterCourses = []
            tListTemplate = []
            sem += 1
        self.calcCGPA(currentSemester, tempTranscriptList)
        return tempTranscriptList

    def calcCreditTaken(self, tempList):
        credit = 0
        for i in tempList:
            credit += int(i[0].credit[0])
        return credit

    def calcCreditCompleted(self, tempList):
        credit = 0
        for i in tempList:
            if i[1] != "FF":
                credit += int(i[0].credit[0])
        return credit

    def calcScoreSemester(self, tempList):
        score = 0
        for i in tempList:
            i1 = Decimal(self.letterGradeDict[i[1]])
            i2 = Decimal(i[0].credit[0])
            i3 = i1 * i2
            score += i3
        return score

    def calcGPA(self, score, creditTaken):
        return score / creditTaken

    def calcCGPA(self, currentSemester, tempTranscriptList):
        n = 1
        cgpa = 0
        while n < currentSemester:
            for i in tempTranscriptList:
                if n >= i[0]:
                    gpa_s = str(i[5])
                    gpa = Decimal(gpa_s)
                    cgpa += gpa
            cgpa = cgpa / n
            cgpa_s = str(cgpa)[:4]
            cgpa = Decimal(cgpa_s)
            tempTranscriptList[n - 1].insert(6, cgpa)
            cgpa = 0
            n += 1

    def show(self):
        for i in self.transcriptList:
            print("*******************************")
            print("Semester : ", i[0])
            print("*******************************")
            for j in i[1]:
                print("Course :", j[0].courseCode, j[0].courseName,
                      "\nCourse Semester:", j[0].semester, "\nTaken Semester:", j[2],
                      "\nCredit:", j[0].credit[0], "\nLetter Grade:", j[1])
                print("........")

            print("Credit Taken = ", i[2])
            print("Credit Completed = ", i[3])
            print("Score Semester = ", i[4])
            print("GPA = ", i[5])
            print("CGPA = ", i[6])


##########################################yardımcı method
def calculateTotalCredit(transcriptTemplate, semesterCounter):
    totalCredit = 0
    for i in transcriptTemplate:
        if i[2] == str(semesterCounter):
            if i[1] != "FF":
                totalCredit += int(i[0].credit[0])
    return totalCredit


#################################################yardımcı method
def createFailedCourseList(transcriptTemplate, currentSemester):
    failedCourseList = []
    num = 1
    while num < currentSemester:
        for i in transcriptTemplate:
            if str(num) == i[0].semester:
                if i[1] == "FF":
                    failedCourseList.append(i)
        num += 1
    return failedCourseList


# yardımcı method
def assignCourse(transcriptTemplate, currentSemester, letterGradeList):
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
        l.insert(1, calculateTotalCredit(transcriptTemplate, n))
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


############################################### transcripti oluşturan random method
def randomTranscript(wholeCourseList, transCriptJsonStudentInfo):
    letterGradeList = ["AA", "BA", "BB", "BC", "CC", "DC", "DD", "FD", "FF"]
    currentSemester = transCriptJsonStudentInfo[3]
    semesterLimit = currentSemester - 1
    courseNTEandUE = []
    courseFTE = []
    courseTE = []
    transcriptTemplate = []
    totalCredit = 0
    for i in allCourses:
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
                                if (j[0].courseCode == i.prerequisites.courseCode and j[1] != "FF"):
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
                                randomCourse.semester = randomCourse.courseCode[-4]
                                tempList.insert(0, randomCourse)
                                tempList.insert(1, random.choice(letterGradeList))
                                tempList.insert(2, randomCourse.semester)
                                transcriptTemplate.append(tempList)

                                tempList = []
                                randomListNTEandUE = []
                            else:

                                for j in transcriptTemplate:
                                    if (j[0].courseCode == randomCourse.prerequisites.courseCode and j[1] != "FF"):
                                        randomCourse.semester = randomCourse.courseCode[-4]
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
                                randomCourse.semester = randomCourse.courseCode[-4]
                                tempList.insert(0, randomCourse)
                                tempList.insert(1, random.choice(letterGradeList))
                                tempList.insert(2, randomCourse.semester)
                                transcriptTemplate.append(tempList)
                                tempList = []
                                randomListFTE = []

                            else:

                                for j in transcriptTemplate:
                                    if (j[0].courseCode == randomCourse.prerequisites.courseCode and j[1] != "FF"):
                                        randomCourse.semester = randomCourse.courseCode[-4]
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
                                randomCourse.semester = randomCourse.courseCode[-4]
                                tempList.insert(0, randomCourse)
                                tempList.insert(1, random.choice(letterGradeList))
                                tempList.insert(2, randomCourse.semester)
                                transcriptTemplate.append(tempList)
                                tempList = []
                                randomListTE = []
                            else:

                                for j in transcriptTemplate:
                                    if (j[0].courseCode == randomCourse.prerequisites.courseCode and j[1] != "FF"):
                                        randomCourse.semester = randomCourse.courseCode[-4]
                                        tempList.insert(0, randomCourse)
                                        tempList.insert(1, random.choice(letterGradeList))
                                        tempList.insert(2, randomCourse.semester)
                                        transcriptTemplate.append(tempList)
                                        tempList = []
                                        randomListTE = []

        semesterCounter += 1

    assignCourse(transcriptTemplate, currentSemester, letterGradeList)
    t = Transcript(transcriptTemplate, transCriptJsonStudentInfo)
    return t

########################33#transcript oluşturulma şekli
# taylanID = StudentID(2018,44) --> student ID for student
# transCriptJsonStudentInfo=[taylanID,"Özgür","Taylan",4] ---> random transcript methodu için gerekli parametreler
# t = randomTranscript(realAllCourses,transCriptJsonStudentInfo) ---> verilen öğrenci için transcriptin oluşturulması
# t.show() ---> oluşturulan transcript in detayları
#
#
#
#
#