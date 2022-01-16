class Semester:

    def __init__(self):
        self.mandatoryCourses = []
        for i in range(0,5):
            self.mandatoryCourses.append([None, None, None, None, None, None, None, None])




class Schedule:
    
    global hoursDict
    hoursDict = {"09:30-10:20":1,
                "10:30-11:20":2,
                "11:30-12:20":3,
                "14:00-14:50":4,
                "15:00-15:50":5,
                "16:00-16:50":6,
                "17:00-17:50":7,
                "18:00-18:50":8}
    

    
    def __init__(self, day, hour):   #Mon:1,Tue:2,Thu:3,Wed:4,Fri:5
        
        self.day = day
        self.hour = hour

        
    def parseHours(self, hoursDict):
        alist = []
        for i in range(self.hour):
            if i in hoursDict.keys():
                alist.append(hoursDict.get(i))
        return alist
                
    
    
class CourseCode:
    
    
    def __init__(self, courseType, courseNum): #CSE3033
        
        self.courseType = courseType
        self.courseNum = courseNum
        self.code = self.combineCode()
        


    
    def combineCode(self):
        return self.courseType + str(self.courseNum)

        
        
        

        
        


class Course:

    
    def __init__(self, courseName, courseCode, courseType, semester,
                 credit, prerequisites, quota, registeredStudents, schedule, theoreticalHours):
            self.courseName = courseName
            self.courseCode = courseCode
            self.semester = semester
            self.courseType = courseType
            self.credit = credit
            self.prerequisites = prerequisites
            self.quota = quota
            self.schedule = schedule
            self.registeredStudents = registeredStudents
            self.theoreticalHours = theoreticalHours
            self.currentStudentNum = 0;
            
            
            
if __name__ == "__main__":
    
    sampleCode = CourseCode("CSE",1011,1)
    sampleSchedule = Schedule([1,2], ["16:00-16:50","17:00-17:50","18:00-18:50"])
    sampleCourse = Course("Sample",sampleCode,"CSE",4,4,None,220,sampleSchedule,None)
    
    print(sampleCode.code) 
    print(sampleSchedule.hoursCode)
    print(sampleCourse.courseName)

    
    dbCode = CourseCode("CSE", 3055,0)
    dbSchedule = Schedule([1,2], ["10:30-11:20","14:00-14:50","15:00-15:50"])
    dbCourse = Course("Database Systems", dbCode, "CSE", 6, 7, sampleCourse, 220, dbSchedule, None)

    print(dbCode.code) 
    print(dbSchedule.hoursCode)
    print(dbCourse.courseName)
    print(dbCourse.prerequisites.courseName)
   
