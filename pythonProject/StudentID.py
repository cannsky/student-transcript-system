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
            self.fullID = args[0]
            self.deptCode = args[0][:4]
            self.entryYear = int(args[0][4:6]) + 2000
            self.rank = int(args[0][6:])