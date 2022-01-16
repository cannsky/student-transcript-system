from StudentID import StudentID
from Transcript import Transcript
import random

class Student:
    def __init__(self, *args):
        self.courseNTEandUE = []
        self.courseFTE = []
        self.courseTE = []
        self.countOfNTEandUEToTake = 0
        self.countOfTEToTake = 0
        self.countOfFTEToTake = 0
        self.availableCourses = []
        self.schedule = []
        self.currentCredits = 0;
        self.courseList = []
        self.wishList = [];


       

        if len(args) == 4:
            self.firstName = args[0]
            self.lastName = args[1]
            self.studentID = args[2]
            self.transcript = args[3]
            self.semester = 1
            self.completedCredits = self.transcript.calcCreditCompleted(self.transcript.transcriptList)

        else:
            # firstName, lastName, studentID, transcript, advisor, semester, completedCredits
            self.firstName = args[0]
            self.lastName = args[1]
            self.studentID = args[2]
            self.transcript = args[3]
            self.semester = args[4]
            self.completedCredits = self.transcript.calcCreditCompleted(self.transcript.transcriptList)
         


    def addToCourses(self, course):
        self.courseList.append(course)

    def removeFromCourses(self, course):
        for i in self.courseList:
            if i.courseID == course.courseID:
                self.courseList.remove(i)

    def enrollToCourses(self):
    
        
        course_num_nteandue=self.countOfNTEandUEToTake 
        course_num_te=self.countOfTEToTake 
        course_num_fte=self.countOfFTEToTake 
        print("Semester :", self.semester, course_num_nteandue,course_num_te,course_num_fte)
        
        for i in self.availableCourses:
            self.wishList.append(i);
        random.shuffle(self.courseTE)
        for i in range(course_num_te):
            self.wishList.append(self.courseTE[i])
        random.shuffle(self.courseFTE)
        for i in range(course_num_fte):
            self.wishList.append(self.courseFTE[i])
        random.shuffle(self.courseNTEandUE)
        for i in range(course_num_nteandue):
            self.wishList.append(self.courseNTEandUE[i])
            
            
    def showWishList(self):
        for i in self.wishList:
            print(i.courseCode.code)
            
            
   
    
    def addCourseToSchedule(self, schedule):
        
        self.schedule.append(schedule)






    def updateTranscript(self):
        tempList = []
        for i in self.courseList:
            tempList.append([i,None,self.semester])

        if(self.semester == 1):
            self.transcript.transcriptList=self.transcript.calcSemestersDetails(tempList,self.semester)
        else:
            if(len(self.transcript.transcriptTemplate) != 0 and self.semester >1):
                listTemp = []
                for i in self.transcript.transcriptTemplate:
                    listTemp.append(i)
                for j in tempList:
                    listTemp.append(j)
                self.transcript.transcriptList=self.transcript.calcSemestersDetails(listTemp,self.semester)
