class Transcript:
    courseList = []
    numberGradeList = []
    letterGradeList = []

    creditTakenS = None
    creditTakenY = None
    creditCompletedS = None
    creditCompletedY = None
    scoreS = None
    scoreY = None
    gpa = None
    cgpa = None

    def __init__(self, transcriptJsonList, transCriptJsonStudentInfo, type):
        if(type == 0): return
        self.transcriptJsonList = transcriptJsonList
        self.fillLists(self.courseList, self.numberGradeList, self.letterGradeList, self.transcriptJsonList)

        self.ID = transCriptJsonStudentInfo[0]
        self.fName = transCriptJsonStudentInfo[1]
        self.lName = transCriptJsonStudentInfo[2]
        self.currentSemester = transCriptJsonStudentInfo[3]

    def fillLists(self, courseList, numberGradeList, letterGradeList, transcriptJsonList):

        for i in transcriptJsonList:
            letterGradeList.append(i[1])
            numberGradeList.append(i[2])
            # there is something on there.

    def calcCreditTakenS(self):
        print("Credits that taken for current semestre")

    def calcCreditTakenY(self):
        print("Credits that taken for whole year")

    def calcCreditCompletedS(self):
        print("Credits that completed succesfuly for current semestre")

    def calcCreditCompletedY(self):
        print("Credits that completed succesfuly for whole year")

    def calcScoreS(self):
        print("Score for current semestre")

    def calcScoreY(self):
        print("Score for whole year")

    def calcGPA(self):
        print("Grade Point Average for semestre")

    def calcCGPA(self):
        print("Cumulative Grade Point Avarage for whole year")