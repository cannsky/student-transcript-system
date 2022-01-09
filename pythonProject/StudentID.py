class StudentID:

    def __init__(self, *args):

        if len(args)==2:
            entryYear = args[0]
            rank = args[1]

            self.deptCode = "1501"
            self.entryYear = entryYear
            self.rank = rank
            self.fullID = str(self.deptCode + str(self.entryYear % 100) + str("%.3f" % (self.rank / 1000))[2:])

        else:
            fullID = args[0]
            self.deptCode = fullID[:4]
            self.entryYear = int(fullID[4:6]) + 2000
            self.rank = int(fullID[6:])