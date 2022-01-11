from decimal import Decimal

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

############################################### transcripti oluşturan random method