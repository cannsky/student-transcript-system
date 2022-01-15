from StudentID import StudentID
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
        
            
    
            
            
            
            
            # CourseCode: Semester-Count
            # NTE: 2-1, 8-1
            # TE: 7-1, 8-3
            # FTE: 8-1
            # UE: 7-1.
