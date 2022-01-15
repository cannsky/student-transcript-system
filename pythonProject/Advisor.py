"""
advisor
create
    3: advisorID, name, lname
    students

existing
    4: args[3], students
    new students
    delete alumni

add student
    add by id (skipping adv by 1)

remove alumni
    scan studentlist:
        if there are alumni students:
            remove student

overlap check (get courseList by stuID)
    courses in courseList,
        check days:
            if it overlaps, check hours:
                if it also overlaps:
                    remove the course in lower semester
                    start over
"""

class Advisor:
    def __init__(self, *args):

        if len(args) == 3:
            self.advisorID = args[0]
            self.fName = args[1]
            self.lName = args[2]
            self.studentList = args[3]

        if len(args) == 4:
            self.advisorID = args[0]
            self.fName = args[1]
            self.lName = args[2]
            self.studentList = args[3]

    def addToStudents(self, student):
        list(self.studentList).append(student)

    def removeFromStudents(self, student):
        for i in self.studentList:
            if i.studentID.fullID == student.studentID.fullID:
                self.studentList.remove(i)
                
                
    def compare_2_ScheduleList(schedule1, schedule2):
        
        conflict = 0
        for i in schedule1:
            for j in schedule2:
                if(i.day == j.day):
                    for x in i.hours:
                        for y in j.hours:
                            if(x == y):
                                conflict +=1
        return conflict
                            
                
                
    def checkStudentWishList(self,student):
        
        log_error = []
        
        #(defaultError:0 , quota:1, schdule : 2)        
        for i in student.wishList:
            #print(i.courseCode.code + " " + i.courseType + " " + i.semester)
            if(i.courseType == "Mandatory"):
                
                if(i.courseCode.code == "CSE4197"):  #Proje Dersiyse Grad Kontrolu
                    if(student.transcript.creditCompleted >= 165):
                       
                        if(int(student.currentCredits) + int(i.credit[0]) <= 45): #Credit check
                            student.courseList.append(i)
                            i.currentStudentNum += 1;
                            student.addCourseToSchedule(i.schedule)
                            student.currentCredits += int(i.credit[0])
                        else:
                            print("The Advisor did not approve " + i.courseCode.code + " becauese student can't take no more than 45 credits")
                            log_error.append([student.studentID.fullID, i.courseCode.code, 0])
                        
                    else:
                        print("The Advisor did not approve " + i.courseCode.code + " becauese student can not gradute in this semester.")
                        log_error.append([student.studentID.fullID, i.courseCode.code, 0])
                        
                else:
                    
                    if(int(student.currentCredits) + int(i.credit[0]) <= 45):
                        student.courseList.append(i)
                        i.currentStudentNum += 1;
                        student.addCourseToSchedule(i.schedule)
                        student.currentCredits += int(i.credit[0])
                    else:
                        print("The Advisor did not approve " + i.courseCode.code + " becauese student can't take no more than 45 credits")
                        log_error.append([student.studentID.fullID, i.courseCode.code, 0])
            else:
                
                if(i.semester == "9"):  #TE check
                    #print(i.courseCode.code + " " +  i.courseType)
                    if (student.transcript.creditCompleted >= 155):   #Credit check
                        if(student.countOfTEToTake > 0):  #Availability check
                            if(i.quota > i.currentStudentNum):  #Quota check
                                if(True): #schedule conflict check
                                    if(int(student.currentCredits) + int(i.credit[0]) <= 45):
                                        student.courseList.append(i)
                                        i.currentStudentNum += 1;
                                        student.addCourseToSchedule(i.schedule)
                                        student.currentCredits += int(i.credit[0])
                                        student.countOfTEToTake -= 1
                                    else:
                                        print("The Advisor did not approve " + i.courseCode.code + " becauese student can't take no more than 45 credits")
                                        log_error.append([student.studentID.fullID, i.courseCode.code, 0])
                                else:
                                    print("Advisor didn't approve" + i.courseCode.code + " becauese of ")
                                    log_error.append([student.studentID.fullID, i.courseCode.code, 2])
                            else:
                                print("The Advisor didn't approve " + i.courseCode.code + " becauese quota is full")
                                log_error.append([student.studentID.fullID, i.courseCode.code, 1])
                        else:
                            if(student.semester == 7):
                                print("The Advisor didn't approve TE" + i.courseCode.code + " because student already took a  TE and in Fall semester only 1 TE can be taken")
                            elif(student.semester == 8):
                                print("The Advisor didn't approve TE" + i.courseCode.code + " because student already took 3 TE and in Spring semester only 3 TE can be taken")
                            log_error.append([student.studentID.fullID, i.courseCode.code, 0])
                    else:
                        print("The advisor didn't approve TE "+ i.courseCode.code + " because student completed credits < 155")
                        log_error.append([student.studentID.fullID, i.courseCode.code, 0])
                
                elif(i.semester == "10"): #FTE check
                    if (student.transcript.creditCompleted >= 210):   #Credit check
                        if(student.countOfFTEToTake > 0):  #Availability check
                            if(i.quota > i.currentStudentNum):  #Quota check
                                if(True): #schedule conflict check
                                    if(int(student.currentCredits) + int(i.credit[0]) <= 45):
                                        student.courseList.append(i)
                                        i.currentStudentNum += 1;
                                        student.addCourseToSchedule(i.schedule)
                                        student.currentCredits += int(i.credit[0])
                                        student.countOfFTEToTake -= 1
                                    else:
                                        print("The Advisor did not approve " + i.courseCode.code + " becauese student can't take no more than 45 credits")
                                        log_error.append([student.studentID.fullID, i.courseCode.code, 0])
                                else:
                                    print("Advisor didn't approve" + i.courseCode.code + " becauese of ")
                                    log_error.append([student.studentID.fullID, i.courseCode.code, 2])
                            else:
                                print("The Advisor didn't approve " + i.courseCode.code + " becauese quota is full")
                                log_error.append([student.studentID.fullID, i.courseCode.code, 1])
                        else:
                            print("The Advisor didn't approve " + i.courseCode.code + " because student already take a FTE")
                            log_error.append([student.studentID.fullID, i.courseCode.code, 0])
                    else:
                        print("The advisor didn't approve FTE " + i.courseCode.code + "  because students can't take FTE in FALL semester unless they are graduating this semester")
                        log_error.append([student.studentID.fullID, i.courseCode.code, 0])
                        
                        
                elif(i.semester == "11"): #NTE and UE check
                    #print(i.courseCode.code + " " +  i.courseType)
                    if(student.countOfNTEandUEToTake > 0):   #Credit check
                        if(i.quota > i.currentStudentNum):  #Availability check
                            if(True):  #Quota check
                                if(int(student.currentCredits) + int(i.credit[0]) <= 45): #schedule conflict check
                                        student.courseList.append(i)
                                        i.currentStudentNum += 1;
                                        student.addCourseToSchedule(i.schedule)
                                        student.currentCredits += int(i.credit[0])
                                        student.countOfFTEToTake -= 1
                                else:
                                    print("The Advisor did not approve " + i.courseCode.code + " becauese student can't take no more than 45 credits")
                                    log_error.append([student.studentID.fullID, i.courseCode.code, 0])
                            else:
                                print("Advisor didn't approve" + i.courseCode.code + " becauese of ")
                                log_error.append([student.studentID.fullID, i.courseCode.code, 2])
                        else:
                            print("The Advisor didn't approve " + i.courseCode.code + " becauese quota is full")
                            log_error.append([student.studentID.fullID, i.courseCode.code, 1])
                    else:
                        print("The Advisor didn't approve " + i.courseCode.code + " because student can not take no more NTE or UE")
                        log_error.append([student.studentID.fullID, i.courseCode.code, 0])
       
        return log_error                 
                        
            
                    
                    
                    
                                    
                                
                                
                
                
                
                
                
            
        
        
        
        

    #def checkOverlap(self, student):