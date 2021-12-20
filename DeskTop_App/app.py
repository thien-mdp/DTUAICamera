import tkinter as tk
from tkinter import ttk,messagebox
from tkinter import font
from tkinter.constants import CENTER, LEFT
from PIL import ImageTk, Image
import cv2
from random import randrange
import os
from camera import MyVideoCapture
import trainning_model_auto
from datetime import datetime
from threading import Thread
from database import get_number_of_violation,del_all_violation,students,engine,metadata,check_student,update_student,del_student,add_student,get_student,del_all_students,get_one_student,get_violator_list,check_true_violation, get_account
from gtts import gTTS
import shutil
import pygame
#Folder Dataset
FOLDER = "dataset/"
import time

def get_time():
    now = datetime.now()

    now = str(now).split(" ")
    key1 = "".join(now[0].split("-"))
    key2 = "".join(now[1].split(":")).split(".")[0]
    key = key1 + key2
    return key

class Login(tk.Tk):
    def __init__(master):
        super().__init__()
        master.logins = None
        w = 350
        h = 500
        ws = master.winfo_screenwidth()
        hs = master.winfo_screenheight()
        x = int(ws/2 - (w/2))
        y = int(hs/2 - (h/2))
        master.geometry('%dx%d+%d+%d' % (w,h,x,y))
        master.title(' L O G I N ')
        master.resizable(0, 0)
        master.get__frame_login()
    def get__frame_login(self):
        j = 0
        r = 10
        for i in range(100):
            c = str(222222 + r)
            self.login = tk.Frame(self, width=10, height=500, bg="#" + c).place(x=j, y=0)
            j = j + 10
            r = r + 1
        self.login2 = tk.Frame(self,width=250,height=400,bg='white').place(x=50,y=50)
        self.l1 = tk.Label(self, text='Username', bg='white')
        l = ('Consolas', 13)
        self.l1.config(font=l)
        self.l1.place(x=80, y=200)

        # e1 entry for username entry
        self.e1 = tk.Entry(self, width=20, border=0)
        l = ('Consolas', 13)
        self.e1.config(font=l)
        self.e1.place(x=80, y=230)

        # e2 entry for password entry
        self.e2 = tk.Entry(self, width=20, border=0, show='*')
        self.e2.config(font=l)
        self.e2.place(x=80, y=310)

        self.l2 = tk.Label(self, text='Password', bg='white')
        l = ('Consolas', 13)
        self.l2.config(font=l)
        self.l2.place(x=80, y=280)
        ###lineframe on entry

        self.frame3 = tk.Frame(self, width=180, height=2, bg='#141414').place(x=80, y=332)
        self.frame4 = tk.Frame(self, width=180, height=2, bg='#141414').place(x=80, y=252)


        self.imageLogo = ImageTk.PhotoImage(file='./images-logo/LOGIN.PNG')

        self.label1 = tk.Label(image=self.imageLogo,
                       border=0,
                       justify=tk.CENTER)

        self.label1.place(x=80, y=110)
        self.bttn(100, 375, 'L O G I N', 'white', '#994422')

    #     # Command
    def cmd(self):
        global app
        if get_account(self.e1.get(),self.e2.get()) == True:
            messagebox.showinfo("LOGIN SUCCESSFULLY", "         W E L C O M E !!!       ")
            app.destroy()
            app = APPMAIN()
            app.mainloop()

        else:
            messagebox.showwarning("LOGIN FAILED", "        PLEASE TRY AGAIN        ")

        # Button_with hover effect
    def bttn(self,x, y, text, ecolor, lcolor):
        def on_entera(e):
            myButton1['background'] = ecolor  # ffcc66
            myButton1['foreground'] = lcolor  # 000d33

        def on_leavea(e):
            myButton1['background'] = lcolor
            myButton1['foreground'] = ecolor

        myButton1 = tk.Button(self, text=text,
                           width=20,
                           height=2,
                           fg=ecolor,
                           border=0,
                           bg=lcolor,
                           activeforeground=lcolor,
                           activebackground=ecolor,
                           command=self.cmd)

        myButton1.bind("<Enter>", on_entera)
        myButton1.bind("<Leave>", on_leavea)

        myButton1.place(x=x, y=y)

#ham check id == INT ??

def check_id(id):
    try:
        id = int(id)
        return True
    except:
        return False
#ham check phone_number
def check_PhoneNumber(phone_number):
    if len(phone_number) < 10 or len(phone_number) > 16:
        return False
    return True
    
def open_add_students_form():
    app2 = App()
    luong_add = Thread(target=app2.mainloop())
    luong_add.start()


class APPMAIN(tk.Tk):
    def __init__(self):
        super().__init__()
        self.Students = None
        self.contacts = []
        self.title("DTU AI CAMERA")
        self.configure(bg='#f7e8c0')
        self.geometry("1600x800")
        self.label_nameApplication = tk.Label(self, text="DETECTION AND WARNING APPLICATION ABOUT WEARING FACE MASKS", font=('Times New Roman', 24,'bold'), bg = '#f7e8c0', fg='red')
        self.label_nameApplication.grid(row=0, column=0, pady=30, padx=100)
        self.create_table_students()

        self.create_find_()
        self.label_Result = None
        self.form_update = None
        self.create_frame_show_results_detect()

    #ham update thong tin 1 sinh vien

    def update_one_student(self):
        check = messagebox.askquestion("Question","Are you sure to update information of this student ? ")
        if check == 'yes':
            name = self.entry_update_name.get()
            if len(name) == 0 :
                messagebox.showwarning("WARNING", "Fail !!! Name is Empty !!!")
                return False
            student_class = self.entry_update_class.get()
            if len(student_class) == 0 :
                messagebox.showwarning("WARNING", "Fail !!! Class is Empty !!!")
                return False
            phone_number = self.entry_update_phoneNumber.get()
            if len(phone_number) > 0 :  
                if check_PhoneNumber(phone_number) == False:
                    messagebox.showwarning("WARNING", "Fail !!! Phone is Empty or Wrong!!!")
                    return False
            update_student(self.id_find,name=name,student_class=student_class,phone_number=phone_number)
            messagebox.showinfo("Congratulation !!!","Update successful !!! Please Re-Load Information List")
    def create_frame_show_results_detect(self):
        # add style into FORM
        s = ttk.Style()
        s.theme_use('clam')
        s.configure('new.TFrame', background='#f7e8c0')
        self.show_results_detect = ttk.Frame(self,style='new.TFrame')
        self.label_Result_detect = tk.Label(self.show_results_detect, text="",font=('Times New Roman', 16),bg = '#f7e8c0')
        self.label_Result_detect.grid(row=0, column=0)
        text_show = ""
        self.show_results = tk.Label(self.show_results_detect, text=text_show,font=('Times New Roman', 12),bg = '#f7e8c0')
        self.show_results.grid(row=1, column=0) 
        self.show_results_detect.grid(row=4, column=0)
    def Face_Mask_Detection(self):
        luong_detect = Thread(target=self.detect_mask)
        luong_detect.start()
    #ham nhan dien
    def detect_mask(self):
        video_frame = MyVideoCapture()
        try:
            os.mkdir("violator_images")
        except:
            pass
        while True:
            list_id, list_result, ret, frame = video_frame.get_frame_detect()
            cv2.imshow("CAMERA ( WEBCAM )", frame)
            text_show = ""
            for i in range(len(list_id)):
                text_show = text_show + "ID: {0} =>> {1}\n".format(list_id[i],list_result[i])
                if list_result[i] == "No mask" or list_result[i] == "Wrong":
                    name_img = str(get_time())+".jpg"
                    check = check_true_violation(list_id[i],name_img=name_img)
                    if check:
                        cv2.imwrite("violator_images/" + name_img, frame)
                        in4 = get_one_student(list_id[i])
                        name = str(in4[1])
                        text_read ="Bạn" + name + "vui lòng hãy đeo khẩu trang"
                        tts = gTTS(text_read,lang='vi')
                        tts.save('temp_audio/temp.mp3')
                       
                        pygame.mixer.init()
                        pygame.mixer.music.load('temp_audio/temp.mp3')
                        pygame.mixer.music.play()
                        time.sleep(3)
                         #mp3 english
                        text_read1 ="Please wearing face mask"
                        tts1 = gTTS(text_read1,lang='en')
                        tts1.save('temp_audio/temp-english.mp3')
                        pygame.mixer.init()
                        pygame.mixer.music.load('temp_audio/temp-english.mp3')
                        pygame.mixer.music.play()
                        
                        
            self.show_results['text'] = text_show
            self.label_Result_detect['text'] = "STUDENT LIST"
            self.show_results_detect.update()
            if cv2.waitKey(20) == 27:
                self.show_results_detect.destroy()
                break
        cv2.destroyAllWindows()


    #ham hien noi dung update
    def show_form_update(self):
        # add style into FORM
        s = ttk.Style()
        s.theme_use('clam')
        s.configure('new.TFrame', background='#f7e8c0')
        self.form_update = ttk.Frame(self, style ='new.TFrame')
        self.update_lbFrame = tk.LabelFrame(self, text = 'Frame Update',font=('Times New Roman', 14),fg='blue',bg = '#f7e8c0')
        self.update_lbFrame.grid(row=4, column=0 )
        self.label_update_information = tk.Label(self.update_lbFrame,text="          Update Information of Student have Student ID : {0}".format(self.id_find),font=('Times New Roman', 12),bg = '#f7e8c0')
        self.label_update_information.grid(row=0,column=0,pady=5)
        self.label = tk.Label(self.update_lbFrame,text='',bg='#f7e8c0')
        self.label.grid(row=0,column=2,padx=30)
        
        #name
        self.label_update_name = tk.Label(self.update_lbFrame,text="              Full Name : ",bg = '#f7e8c0',font=('Times New Roman', 9))
        self.label_update_name.grid(row=2,column=0,sticky=tk.W)
        self.entry_update_name = tk.StringVar()
        self.entry_update_name = ttk.Entry(self.update_lbFrame)
        self.entry_update_name.grid(row=2,column=0,ipadx=45,sticky=tk.E,padx=10)
        
        #student_class
        self.label_update_class = tk.Label(self.update_lbFrame, text="\t      Class :",bg = '#f7e8c0',font=('Times New Roman', 9))
        self.label_update_class.grid(row=3, column=0, sticky=tk.W)
        self.entry_update_class = tk.StringVar()
        self.entry_update_class = ttk.Entry(self.update_lbFrame)
        self.entry_update_class.grid(row=3, column=0,ipadx=45,sticky=tk.E,padx=10, pady=10)
      
        #phone_number
        self.label_update_phoneNumber = tk.Label(self.update_lbFrame, text="     Phone Number : ",bg = '#f7e8c0',font=('Times New Roman', 9))
        self.label_update_phoneNumber.grid(row=4, column=0, sticky=tk.W)
        self.entry_update_phoneNumber = tk.StringVar()
        self.entry_update_phoneNumber = ttk.Entry(self.update_lbFrame)
        self.entry_update_phoneNumber.grid(row=4, column=0,ipadx=45,sticky=tk.E,padx=10)
        

        #button update
        self.photoComfirmUpdate = ImageTk.PhotoImage(file='./images-logo/Confirm-update.png')
        self.button_update_one_student = tk.Button(self.update_lbFrame,text= "Update Information",font=('Times New Roman', 10),image = self.photoComfirmUpdate,borderwidth=1.5,width=140,height=30,relief="solid",bg='#fff',compound=LEFT, command=self.update_one_student)
        self.button_update_one_student.grid(row=5,column=0,pady=10)
        self.update_lbFrame.grid(row=4, column=0, sticky=tk.W, padx=110,pady=10)
    
    def train_after_del(self):
        if self.form_update != None:
            self.form_update.destroy()
        list_data = os.listdir(FOLDER)
        if len(list_data)==0:
            self.label_Result['text'] = "Delete successfully !!! Please Re-Load Information List!!!"
            self.find_lbFrame.update()
            return False
        verbose = True
        tic = time.perf_counter()
        print("Training KNN classifier...")
        # Creates Classifier
        classifier = trainning_model_auto.train(FOLDER, model_save_path="trained_knn_model.clf", verbose=verbose)
        print("Training complete!")
        self.label_Result['text'] = "Delete successfully !!! Please Re-Load Information List!!!"
        self.find_lbFrame.update()
    #ham xoa 1 sinh vien
    def delete_inforOfStudent(self):
        check = messagebox.askquestion("DANGER !!! ", "Are you sure to delete this student ???")
        if check == "yes":
            messagebox.showinfo("CONGRATULATION !!!","DELETE SUCCESSFUL !!! PLEASE RE-LOAD INFORMATION LIST !!!")
            del_student(self.id_find)
            shutil.rmtree('dataset/'+str(self.id_find))
            luong_train_lai = Thread(target=self.train_after_del)
            luong_train_lai.start()
    
    #tao khung tim kiem
    def create_find_(self):
        # add style into FORM
        s = ttk.Style()
        s.theme_use('clam')
        s.configure('new.TFrame', background='#f7e8c0')
        self.find_frame = ttk.Frame(self, style ='new.TFrame')
        self.find_lbFrame = tk.LabelFrame(self, text = 'Frame Search',font=('Times New Roman', 14),fg='blue',bg = '#f7e8c0')
        self.label = tk.Label(self.find_lbFrame,text='',bg='#f7e8c0')
        self.label.grid(row=0,column=0)
        self.label_find = tk.Label(self.find_lbFrame,text="Enter Student ID : ",font=('Times New Roman', 10),bg = '#f7e8c0')
        self.label_find.grid(row=0,column=1)
        self.id_find_entry = tk.StringVar()
        self.id_find_entry = ttk.Entry(self.find_lbFrame,width = 40)
        self.id_find_entry.grid(row = 0,column=2,padx=15)
        self.photoSearch = ImageTk.PhotoImage(file='./images-logo/Search.png')
        self.button_find = tk.Button(self.find_lbFrame,text=" Search",image=self.photoSearch, borderwidth=1.5,relief="solid",width=80,height=30,bg='#fff',font=('Times New Roman', 10), compound=LEFT,command=self.find_student)
        self.button_find.grid(row=0,column=3)
        self.label = tk.Label(self.find_lbFrame,text='',bg='#f7e8c0')
        self.label.grid(row=0,column=4,padx=10)
        self.find_lbFrame.grid(row=2,column=0)

    #ham tim kiem sinh vien va show ket qua
    def find_student(self):
        if self.form_update != None:
            self.form_update.destroy()
        self.id_find = self.id_find_entry.get()
        if check_id(self.id_find) == False: 
            messagebox.showwarning(
                "WARNING", "ID REQUIRED IS INTEGER !!! YOU ENTERED IN THE WRONG ID!!! PLEASE TRY AGAIN !!!")
            return False
        # Check sinh vien da ton tai trong db
        self.student_had = get_one_student(self.id_find)
        if self.label_Result != None:
            self.label_Result.destroy()
        if self.student_had == False:
            self.label_Result = tk.Label(self.find_lbFrame,text="Can't search the student you are looking for !!! Please Try Again !!!",font=('Times New Roman', 13),bg = '#f7e8c0')
            self.label_Result.grid(row = 0,column=5)
            return False
        text_show = "||Student ID|| : {0}    ||Full Name|| : {1}      ||Class|| : {2}     ||Phone Number|| : {3}\t".format(self.student_had[0],self.student_had[1],self.student_had[2],self.student_had[3])
        self.label_Result = tk.Label(self.find_lbFrame, text=text_show,font=('Times New Roman',11,'bold'),bg = '#f7e8c0')
        self.label_Result.grid(row=0, column=5,columnspan=2)
        self.photoDeleteStudent = ImageTk.PhotoImage(file='./images-logo/Delete-Student.png')
        self.button_delete_this_student = tk.Button(self.find_lbFrame,text = "  Delete This Student",image=self.photoDeleteStudent, borderwidth=1.5,relief="solid",width=150,height=26,bg='#fff',font=('Times New Roman', 10), compound=LEFT,command = self.delete_inforOfStudent)
        self.button_delete_this_student.grid(row=1,column = 5)
        self.photoUpdate = ImageTk.PhotoImage(file='./images-logo/Update-student.png')
        self.button_update_this_student = tk.Button(self.find_lbFrame,text = "  Update This Student",image=self.photoUpdate, borderwidth=1.5,relief="solid",width=150,height=26,bg='#fff',font=('Times New Roman', 10), compound=LEFT,command=self.show_form_update)
        self.button_update_this_student.grid(row=1,column = 6,pady=6)
        # self.label = tk.Label(self.find_lbFrame,text='',bg='#f7e8c0')
        # self.label.grid(row=2,column=0)

    # adding data to the treeview
    def create_table_students(self):
        # add style into FORM
        s = ttk.Style()
        s.theme_use('clam')
        s.configure('new.TFrame', background='#f7e8c0')
        self.table = ttk.Frame(self, style='new.TFrame')
        self.labelFrameTable = tk.LabelFrame(self.table, text = 'Information Of Students',font=('Times New Roman', 14),fg='blue',bg = '#f7e8c0')
        self.labelFrameTable.grid(column = 0, row = 0, padx = 60)
        self.label = tk.Label(self.labelFrameTable,text='',bg='#f7e8c0')
        self.label.grid(padx=100)
        style = ttk.Style()
        style.configure('Treeview',rowheight = 20,font=('Times New Roman', 11))
        style.configure('Treeview.Heading', background="#D3D3D3", foreground="black",rowheight = 20,font=('Times New Roman', 12))
        self.tree = ttk.Treeview(self.labelFrameTable,style='Treeview', column=("#1", "#2", "#3","#4"), show='headings',height=8)
    
        self.tree.heading("#1", text="Student ID")
        self.tree.column("#1", anchor=tk.CENTER)
    

        self.tree.heading("#2", text="Full Name")
        self.tree.column("#2", anchor=tk.CENTER)
        

        self.tree.heading("#3", text="Class")
        self.tree.column("#3", anchor=tk.CENTER)


        self.tree.heading("#4", text="Phone Number")
        self.tree.column("#4", anchor=tk.CENTER)
        self.rows = get_student()
        # self.tree.tag_configure('oddrow',background='white')
        # self.tree.tag_configure('evenrow',background="#f7e8c0")
        for row in self.rows:
            self.tree.insert('', tk.END, values=[row[0],row[1],row[2],row[3]])

        # bind the select event
        def item_selected(event):
            for selected_item in self.tree.selection():
                # dictionary
                item = self.tree.item(selected_item)
                # list
                record = item['values']
                #
                text_title = "Student ID : {0} \n" \
                             "Full Name : {1}\n" \
                             "Class : {2}\n" \
                             "Phone Number {3}\n".format(str(record[0]),record[1],record[2],"0"+str(record[3]))
                messagebox.showinfo(title='Student Information',
                         message=text_title)

        self.tree.bind('<<TreeviewSelect>>', item_selected)
        self.tree.grid(row=2, column=0, sticky='nsew',rowspan=5,columnspan=3)
        self.scrollbar = ttk.Scrollbar(self.labelFrameTable, orient=tk.VERTICAL, command=self.tree.  yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=2, column=4, sticky='ns',rowspan=4)
        self.label = tk.Label(self.labelFrameTable,text='',bg='#f7e8c0')
        self.label.grid(padx=100)
        self.label = tk.Label(self.labelFrameTable,text='',bg='#f7e8c0')
        self.label.grid(padx=100)
        self.label = tk.Label(self.labelFrameTable,text='',bg='#f7e8c0')
        self.label.grid(padx=100)
        self.labelFrameActivate = tk.LabelFrame(self.table, text = 'Activate',borderwidth=2,relief="groove", font=('Times New Roman', 14),fg='blue',bg='#f7e8c0')
        self.labelFrameActivate.grid(column = 5, row = 0, padx = 50)
        self.photoAdd = ImageTk.PhotoImage(file='./images-logo/Add.png')
        self.button_AddNewStudents = tk.Button(self.labelFrameActivate, text="  Add New Students",image = self.photoAdd,borderwidth=1.5,width=150,height=30,relief="solid",font=('Times New Roman', 10),bg='#fff',compound=LEFT, command=open_add_students_form)
        self.button_AddNewStudents.grid(row=2, column=5,padx=100)
        self.label = tk.Label(self.labelFrameActivate,text='',bg='#f7e8c0')
        self.label.grid(row = 3, column = 5, padx=100)
        self.photoReload = ImageTk.PhotoImage(file='./images-logo/Reload.png')
        self.button_reloadList = tk.Button(self.labelFrameActivate, text="  Re-Load Student List",image=self.photoReload,borderwidth=1.5,relief="solid",width=150,height=30,bg='#fff',font=('Times New Roman', 10), compound=LEFT,command=self.updates)
        self.button_reloadList.grid(row=4, column=5, padx=100)
        self.label = tk.Label(self.labelFrameActivate,text='',bg='#f7e8c0')
        self.label.grid(row = 5, column = 5, padx=100)
        self.photoDelete = ImageTk.PhotoImage(file='./images-logo/Remove.png')
        self.button_DeleteAllStudents = tk.Button(self.labelFrameActivate, text="  Delete All Students",image=self.photoDelete, borderwidth=1.5,relief="solid",width=150,height=30,bg='#fff',font=('Times New Roman', 10), compound=LEFT,command=self.delete_all_sv)
        self.button_DeleteAllStudents.grid(row=6, column=5, padx=100)
        self.label = tk.Label(self.labelFrameActivate,text='',bg='#f7e8c0')
        self.label.grid(row = 7, column = 5, padx=100)
        self.photoWebcam = ImageTk.PhotoImage(file='./images-logo/CCTV-camera.png')
        self.button_FaceRecognition = tk.Button(self.labelFrameActivate, text="  Start to Detect",image=self.photoWebcam, borderwidth=1.5,relief="solid",width=150,height=30,bg='#fff',font=('Times New Roman', 10), compound=LEFT,command=self.Face_Mask_Detection)
        self.button_FaceRecognition.grid(row=8, column=5, padx=100)
        self.label = tk.Label(self.labelFrameActivate,text='',bg='#f7e8c0')
        self.label.grid(row = 9, column = 5, padx=100)
        self.photoShowList = ImageTk.PhotoImage(file='./images-logo/List.png')
        self.button_showListViolators = tk.Button(self.labelFrameActivate,text="  Violator List",image=self.photoShowList,borderwidth=1.5,relief="solid",width=150,height=30,bg='#fff',font=('Times New Roman', 10), compound=LEFT,command=self.show_ListInforViolators)
        self.button_showListViolators.grid(row=10, column=5, padx=100)
        self.label = tk.Label(self.labelFrameActivate,text='',bg='#f7e8c0')
        self.label.grid(row = 11, column = 5, padx=100)
        self.table.grid(column=0, row=1,padx=50)
    def show_ListInforViolators(self):
        app2 = APPVIOLATION()
        app2.mainloop()
    def updates(self):
        self.rows = get_student()
        for i in self.tree.get_children():
            self.tree.delete(i)
        for row in self.rows:
            self.tree.insert('', tk.END, values=[row[0], row[1], row[2], row[3]])
        self.table.update()
    def delete_all_sv(self):
        check = messagebox.askquestion("DANGER !!!","Are you sure to delete all students!")
        if check == 'yes':
            shutil.rmtree('dataset')
            os.mkdir(FOLDER)
            messagebox.showinfo("CONGRATULATION !!!","DELETE SUCCESSFUL !!! PLEASE RE-LOAD INFORMATION LIST !!!")
            del_all_students()


class App(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.frame = None
        self.delay = 1
        self.title("Add New Student Form")
        self.configure(bg='#f7e8c0')
        self.geometry("1600x800")
        self.create_video_frame()
        self.list_image_show = []
        self.num_img = 1
        self.check_photo_taken = True
        self.get_image_temp = None

    def update(self):
        ret, self.frame,self.frame2 = self.video_frame.get_frame()
        if ret:
            self.photo2 = ImageTk.PhotoImage(image=Image.fromarray(self.frame2))
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.video.after(1,self.update)

    def update_detect(self):
        ret, self.frame = self.video_frame.get_frame_detect()
        if ret:
            self.photo2 = ImageTk.PhotoImage(image=Image.fromarray(self.frame2))
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.video.after(1,self.update_detect)
    def create_video_frame(self):
        # add style into FORM
        s = ttk.Style()
        s.theme_use('clam')
        s.configure('new.TFrame', background='#f7e8c0')
        self.video = ttk.Frame(self, style='new.TFrame')
        self.video_frame = MyVideoCapture()
        self.lableFrame = tk.LabelFrame(self.video, text = 'Enter Information Of New Student',font=('Times New Roman', 14),fg='blue',bg = '#f7e8c0')
        self.lableFrame.grid(column = 0, row = 1, padx = 40)
        self.label = tk.Label(self.lableFrame,text='',bg='#f7e8c0')
        self.label.grid(pady=20)
        self.id_label = tk.Label(self.lableFrame,text="   Enter Student ID :",bg='#f7e8c0',font=('Times New Roman', 10))
        self.id_label.grid(row=0,column=0)
        self.id = tk.StringVar()
        self.id = ttk.Entry(self.lableFrame,width=30)
        self.id.grid(row=0,column=1)
        self.label = tk.Label(self.lableFrame,text='    ',bg='#f7e8c0')
        self.label.grid(row=0,column=2)
        self.label = tk.Label(self.lableFrame,text='',bg='#f7e8c0')
        self.label.grid(pady=30)
        #nhap ten
       
        self.name_label = tk.Label(self.lableFrame,text="    Enter Full Name :",bg='#f7e8c0',font=('Times New Roman', 10))
        self.name_label.grid(row = 1,column = 0)
        self.name = tk.StringVar()
        self.name = ttk.Entry(self.lableFrame,width=30)
        self.name.grid(row = 1,column = 1)
        self.label = tk.Label(self.lableFrame,text='    ',bg='#f7e8c0')
        self.label.grid(row=0,column=2)
        self.label = tk.Label(self.lableFrame,text='',bg='#f7e8c0')
        self.label.grid(pady=20)
        #nhap chuc vu
        self.name_class_label = tk.Label(self.lableFrame, text="   Enter Class :",bg='#f7e8c0',font=('Times New Roman', 10))
        self.name_class_label.grid(row=2, column=0)
        self.name_class = tk.StringVar()
        self.name_class = ttk.Entry(self.lableFrame, width=30)
        self.name_class.grid(row=2, column=1)
        self.label = tk.Label(self.lableFrame,text='    ',bg='#f7e8c0')
        self.label.grid(row=0,column=2)
        self.label = tk.Label(self.lableFrame,text='',bg='#f7e8c0')
        self.label.grid(pady=20)
        #nhap phone_number
        self.phone_number_label = tk.Label(self.lableFrame, text="Enter Phone Number :",bg='#f7e8c0',font=('Times New Roman', 10))
        self.phone_number_label.grid(row=3, column=0)
        self.phone_number = tk.StringVar()
        self.phone_number = ttk.Entry(self.lableFrame, width=30)
        self.phone_number.grid(row=3, column=1)
        self.label = tk.Label(self.lableFrame,text='    ',bg='#f7e8c0')
        self.label.grid(row=0,column=2)
        self.label = tk.Label(self.lableFrame,text='',bg='#f7e8c0')
        self.label.grid(pady=5)
        #camera
        self.cameraFrame = tk.LabelFrame(self.video, text = 'Camera',font=('Times New Roman', 14),fg='blue',bg = '#f7e8c0')
        self.cameraFrame.grid(column = 2, row = 0,rowspan=4,pady = 110)
        self.canvas = tk.Canvas(self.cameraFrame,width=self.video_frame.width,height=self.video_frame.height,bg = '#f7e8c0')
        self.canvas.grid(row = 0, column = 2,rowspan=4)
        self.photoCamera = ImageTk.PhotoImage(file='./images-logo/Camera.png')
        self.take_photos = tk.Button(self.video,text="   Take Photos ",font=('Times New Roman', 12),image=self.photoCamera, borderwidth=1.5,relief="solid",width=150,height=30,bg='#fff', compound=LEFT,command=self.take_photos)
        self.take_photos.grid(row = 3,column=2,pady = 10)
        #button chuyen sang nhan dien
        # button them sinh vien
        self.showed_video = self.update()
        self.video.grid(column=0, row=0, sticky=tk.NSEW, padx=10, pady=10)
    def take_photos(self):
        try:
            os.mkdir('dataset')
        except:
            pass
        id = self.id.get()
        if self.get_image_temp != None and id != self.get_image_temp:
            self.check_photo_taken = True
            for i in self.list_image_show:
                i.destroy()
            self.list_image_show = []
        if self.check_photo_taken == True:
            try:
                shutil.rmtree("dataset/" + str(id))
            except:
                pass
        if check_id(id) == False:
            messagebox.showwarning(
                "WARNING", "ID REQUIRED IS INTEGER !!! YOU ENTERED IN THE WRONG ID!!! PLEASE TRY AGAIN !!!")
            return False
        self.id_sv = id
        try:
            os.mkdir(FOLDER+str(id))
        except:
            pass
        
        self.name_student = self.name.get()
        if self.name_student == "":
            messagebox.showwarning(
                "WARNING", "YOU HAVE NOT ENTERED STUDENT'S NAME !!!, PLEASE TRY AGAIN !!!")
            return False
        self.class_student = self.name_class.get()
        if self.class_student == "":
            messagebox.showwarning(
                "WARNING", "YOU HAVE NOT ENTERED STUDENT'S CLASS !!!, PLEASE TRY AGAIN !!!")
            return False
        self.phoneNumber_student = self.phone_number.get()

        #có thể check số điện thoai nếu muốn
        if check_PhoneNumber(self.phoneNumber_student) == False:
            messagebox.showwarning(
                "WARNING", "YOU HAVE NOT ENTERED OR ENTER WRONG STUDENT'S PHONE NUMBER !!!, PLEASE TRY AGAIN !!!")
            return False
        
        # name_img = FOLDER+str(id) +"img"+str(randrange(1000,10000))+".jpg"
        name_img = FOLDER+str(id)+"/"+"img"+str(randrange(1000,10000))+".jpg"
        imgpil = ImageTk.getimage(self.photo2)
        imgpil = imgpil.convert('RGB')
        imgpil.save(name_img,"JPEG")
        imgpil.close()
        print('ok')
        self.get_image_temp = id
        self.pictureFrame = tk.LabelFrame(self.video, text = 'Student Photos ',font=('Times New Roman', 14),fg='blue',bg = '#f7e8c0')
        self.pictureFrame.grid(column = 3, row = 1, padx=40)
        self.label = tk.Label(self.pictureFrame,text='',bg='#f7e8c0')
        self.label.grid(pady=20)
        self.photo_taken_label = tk.Label(self.pictureFrame,text="   Images FACE {0}/9 :  ".format(self.num_img),bg='#f7e8c0',font=('Times New Roman', 10))
        self.photo_taken_label.grid(row=0,column=3)
        self.photoClearImage = ImageTk.PhotoImage(file='./images-logo/Clear-img.png')
        self.button_clearImage = tk.Button(self.pictureFrame,text = " Clear Images",image=self.photoClearImage,borderwidth=1.5,relief="solid",font=('Times New Roman', 10),width=150,height=30,bg='#fff', compound=LEFT,command = self.clear_img)
        self.button_clearImage.grid(row = 0 ,column = 4)
        self.label = tk.Label(self.pictureFrame,text='   ',bg='#f7e8c0')   
        self.label.grid(row = 0 ,column = 5)
        self.list_img = os.listdir(FOLDER+str(id)+"/")
        for (index,img) in enumerate(self.list_img):
            self.show_list_image(FOLDER+str(id)+"/"+img,row=1+int(index/3),col=3+index%3)
        self.num_img = len(self.list_img) + 1
        if self.num_img == 10:
            self.take_photos["state"] = "disabled"
            self.photoAddStudents = ImageTk.PhotoImage(file='./images-logo/Add-icon.png')
            self.buttonAddStudents = tk.Button(self.pictureFrame,text = " Add New Student",image=self.photoAddStudents,borderwidth=1.5,relief="solid",font=('Times New Roman', 10),width=150,height=30,bg='#fff', compound=LEFT,command = self.train)
            self.buttonAddStudents.grid(row = 6,column=4,pady=10)
            self.label = tk.Label(self.pictureFrame,text='   ',bg='#f7e8c0')   
            self.label.grid(pady=5)
            self.check_photo_taken = True
        self.check_photo_taken = False
    def show_list_image(self,name_img,row,col):
        img = Image.open(name_img)
        image1 = img.resize((70, 70), Image.ANTIALIAS)
        image1 = ImageTk.PhotoImage(image1)
        self.photo_taken = ttk.Label(self.pictureFrame, image=image1)
        self.photo_taken.grid(row=row, column=col,pady=10)
        self.photo_taken.image = image1
        self.list_image_show.append(self.photo_taken)
        # self.photo_taken_label = ttk.Label(self.video, text="Image FACE {0}/10: ".format(self.num_img))
    def clear_img(self):
        for i in self.list_image_show:
            i.destroy()
        self.list_image_show = []
        self.num_img = 1
        self.id.delete(0, 'end')
    def train_thread(self):
        #xu ly data truoc khi train
        #get all thu muc con cua thu muc dataset
        list_data_student = get_student()
        list_student = []
        for sv in list_data_student:
            list_student.append(str(sv[0]))
        list_data = os.listdir('dataset')
        for data in list_data:
            if str(data) not in list_student:
                shutil.rmtree('dataset/'+str(data))
        verbose = True
        tic = time.perf_counter()
        print("Training KNN classifier...")
        # Creates Classifier
        classifier = trainning_model_auto.train(FOLDER, model_save_path="trained_knn_model.clf", verbose=verbose)
        print("Training complete!!!")
        toc = time.perf_counter()
        if verbose:
            text_result_train = f"Add new students successful !!! Trained to identify students in {toc - tic:0.4f} second"
            self.label_result_train = tk.Label(self.video,font=('Times New Roman', 12),bg = '#f7e8c0',text =text_result_train)
            self.label_result_train.grid(row = 6,column=2,pady = 20)
            
    def train(self):
        result_add = add_student(self.id_sv,self.name_student,self.class_student,self.phoneNumber_student)
        if result_add == False:
            messagebox.showwarning(
                "WARNING", "STUDENT HAVE ALREADY !!!, PLEASE TRY AGAIN !!!")
            return False
        luong_train = Thread(target=self.train_thread)
        luong_train.start()


def detect_mask():
    video_frame = MyVideoCapture()
    while True:
        list_name, list_result, ret, frame = video_frame.get_frame_detect()
        cv2.imshow("WARNING TO WEARING FACE MASKS", frame)
        if cv2.waitKey(24) == 27:
            break
    cv2.destroyAllWindows()

def Face_Mask_Detection():
    luong_detect = Thread(target=detect_mask)
    luong_detect.start()


class APPVIOLATION(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.frame = None
        self.geometry("1600x800")
        self.configure(bg='#f7e8c0')
        self.label_violator_form = tk.Label(self, text="LIST OF VIOLATORS", font=('Times New Roman', 24,'bold'), bg = '#f7e8c0', fg='red')
        self.label_violator_form.grid(row=0, column=0, pady=60, padx=130)
        self.create_table_violation()
        self.title("VIOLATION FORM")
    def create_table_violation(self):
        # add style into FORM
        s = ttk.Style()
        s.theme_use('clam')
        s.configure('new.TFrame', background='#f7e8c0')
        
        self.find_lbFrame = tk.LabelFrame(self, text = 'List Of Violators',borderwidth=2,font=('Times New Roman', 14),fg='blue',bg = '#f7e8c0')
        self.find_lbFrame.grid(row=1,column=0,padx=150)
        # Style of treeview
        style = ttk.Style()
        style.configure('Treeview',rowheight = 20,font=('Times New Roman', 11))
        style.configure('Treeview.Heading', background="#D3D3D3", foreground="black",rowheight = 20,font=('Times New Roman', 12))
        self.tree = ttk.Treeview(self.find_lbFrame,style='Treeview', column=("#1", "#2", "#3", "#4","#5","#6"), show='headings')
        self.tree.column("#1", anchor=tk.CENTER)

        self.tree.heading("#1", text="Student ID")

        self.tree.column("#2", anchor=tk.CENTER)

        self.tree.heading("#2", text="Full Name")

        self.tree.column("#3", anchor=tk.CENTER)

        self.tree.heading("#3", text="Class")
        self.tree.column("#4", anchor=tk.CENTER)

        self.tree.heading("#4", text="Phone Number")
        self.tree.column("#4", anchor=tk.CENTER)

        self.tree.heading("#5", text="Time Of Violation")
        self.tree.column("#4", anchor=tk.CENTER)

        self.tree.heading("#6", text="The Path Contains Violation Photos")
        self.tree.column("#4", anchor=tk.CENTER)
        self.rows = get_violator_list()
        for row in self.rows:
            self.tree.insert('', tk.END, values=[row[0], row[1], row[2], row[3],row[4],row[5]])

        # bind the select event
        def item_selected(event):
            for selected_item in self.tree.selection():
                # dictionary
                item = self.tree.item(selected_item)
                # list
                record = item['values']
                number_of_violation = get_number_of_violation(str(record[0]))
                #
                text_title = "Student ID: {0} \n" \
                             "Full Name: {1}\n" \
                             "Class: {2}\n" \
                             "Phone Number: {3}\n" \
                             "Last Time Violation: {4}\n" \
                             "Number Of Violations: {5}".format(str(record[0]), record[1], record[2], "0" + str(record[3]),str(record[4]),number_of_violation)
                messagebox.showinfo(title='Information Of Violator',
                                    message=text_title)

        self.tree.bind('<<TreeviewSelect>>', item_selected)
        self.tree.grid(row=2, column=0, rowspan=4,columnspan=3)
        self.scrollbar = ttk.Scrollbar(self.find_lbFrame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=2, column=4, sticky='ns', rowspan=4)
        self.label = tk.Label(self.find_lbFrame,text='',bg='#f7e8c0')
        self.label.grid(row=1, column=0)
        self.label = tk.Label(self.find_lbFrame,text='',bg='#f7e8c0')
        self.label.grid(row=3, column=5,pady=30)
        

        self.activate_lbFrame = tk.LabelFrame(self, text = 'Activate',borderwidth=2,font=('Times New Roman', 14),fg='blue',bg = '#f7e8c0')
        self.activate_lbFrame.grid(row=2,column=0,pady=30)
        self.photoReloadViolator = ImageTk.PhotoImage(file='./images-logo/Reload.png')
        self.button_update_ds = tk.Button(self.activate_lbFrame, text="  Re-Load Violator List",font=('Times New Roman', 10),image=self.photoReloadViolator,borderwidth=1.5,relief="solid",width=150,height=30,bg='#fff', compound=LEFT, command=self.updates)
        self.button_update_ds.grid(row=1, column=0,pady = 10,padx=20)   
        self.photoDeleteViolator = ImageTk.PhotoImage(file='./images-logo/Delete-Student.png')
        self.button_delete_ds = tk.Button(self.activate_lbFrame, text="  Delete All Violators",font=('Times New Roman', 10),image=self.photoDeleteViolator,borderwidth=1.5,relief="solid",width=150,height=30,bg='#fff', compound=LEFT, command=self.delete_all_violator)
        self.button_delete_ds.grid(row=1, column=2,padx=20)
        # self.table.grid(column=0, row=1)

    def delete_all_violator(self):
        check = messagebox.askquestion("DANGER!!!", "Are you sure to delete all violators!!!")
        if check == 'yes':
            del_all_violation()
            self.updates()
    def updates(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.rows = get_violator_list()
        for row in self.rows:
            self.tree.insert('', tk.END, values=[row[0], row[1], row[2], row[3], row[4], row[5]])
        self.update()

if __name__ == '__main__':
    metadata.create_all(engine)
    app = Login()
    app.mainloop()
