import tkinter as tk
from PIL import Image, ImageTk
import pygame
        
class APP:
    def __init__(self):
        #時間設置
        self.time_out=120.9 #暫停時長
        self.clock=180.9 #比賽時長
        # after 100ms : 0.10725s
        # after 10ms  : 0.0155s
        self.batch_time=0.0155 #每次減多少秒
        self.after_time=10 #after執行頻率(ms)

        pygame.mixer.init()
        pygame.mixer.music.load("theme.mp3")
        pygame.mixer.music.play(-1)
        self.fighting = False
        
        self.app=tk.Tk()
        self.app.title("記分板") #UI名稱
        #self.app.geometry("1920x1080") #預設視窗大小
        #self.app.attributes('-topmost', True) #置頂
        self.app.config(bg="black") #視窗背景顏色
        self.fullScreenState=True #全螢幕模式預設啟用
        self.app.attributes("-fullscreen", self.fullScreenState) #初始設定全螢幕
        self.app.bind("<F11>",self.FullScreenSwitch) #使用F11切換全螢幕
        self.app.bind("<Escape>",self.quit) #使用Del關閉視窗
        self.app.bind("<F1>",self.change1min) #更改時長1分鐘
        self.app.bind("<F2>",self.change2min) #更改時長2分鐘
        self.app.bind("<F3>",self.change3min) #更改時長3分鐘
    # 標題 row0 ============================================
        self.t_lb=tk.Label(text="機器人格鬥錦標賽",font="微軟正黑體 45 bold",bg="black",fg="orange")
        self.t_lb.grid(row=0,column=0,columnspan=13)
    # 輸入 row1 ============================================
        self.rn_en=tk.Entry(text="Team Red", bg="black", width=30, bd=0, cursor='hand2')
        self.rn_en.bind("<Return>", self.r_ch_name)
        self.rn_en.grid(row=1,column=0)
        
        self.bn_en=tk.Entry(text="Team Blue", bg="black", width=30, bd=0, cursor='hand2')
        self.bn_en.bind("<Return>", self.b_ch_name)
        self.bn_en.grid(row=1,column=9)
    # 隊名 row2 ============================================
        self.r="#EA0000"
        self.b="#0080FF"
        self.rn="Team Red"
        self.bn="Team Blue"
        self.switch={"b":"r", "r":"b"}
        
        self.rt_lb=tk.Label(text=self.rn, font="微軟正黑體 47 bold", fg="white", bg=self.r, width=20)
        self.rt_lb.grid(row=2,column=0,columnspan=4)
        self.bt_lb=tk.Label(text=self.bn, font="微軟正黑體 47 bold", fg="white",bg=self.b, width=20)
        self.bt_lb.grid(row=2,column=9,columnspan=4)
    # 血量 row3 ============================================
        self.rh=3
        self.bh=3
        self.ch=0
        
        for i in range(4):
            exec(f"self.img=Image.open('heart{i}.png')")
            exec(f"self.h{i}_img=ImageTk.PhotoImage(self.img)")
        
        self.rh_btn=tk.Button(image=self.h3_img, bg="black", bd=0, cursor='hand2', command=lambda:self.heart_count("r"))
        self.rh_btn.grid(row=3,column=0,columnspan=4)

        self.bh_btn=tk.Button(image=self.h3_img, bg="black", bd=0, cursor='hand2', command=lambda:self.heart_count("b"))
        self.bh_btn.grid(row=3,column=9,columnspan=4)
    # 黃牌 row4 ============================================
        self.ryc=0
        self.byc=0
        self.cyc=0
        
        for i in range(3):
            exec(f"self.img=Image.open('yc{i}.png')")
            exec(f"self.yc{i}_img=ImageTk.PhotoImage(self.img)")
        
        self.ryc_btn=tk.Button(image=self.yc0_img, bg="black", bd=0, cursor='hand2', command=lambda:self.yellow_count("r"))
        self.ryc_btn.grid(row=4, column=0, columnspan=4)
        
        self.byc_btn=tk.Button(image=self.yc0_img, bg="black", bd=0, cursor='hand2', command=lambda:self.yellow_count("b"))
        self.byc_btn.grid(row=4, column=9, columnspan=4)
    #  br  row5 ============================================
        self.br1=tk.Label(font="微軟正黑體 5", bg="black")
        self.br1.grid(row=5,column=0,columnspan=13)
    # 暫停 row6 ============================================
        self.rt=self.time_out
        self.bt=self.time_out
        self.rid=None
        self.bid=None
        
        self.img=Image.open("timeout.jpg")
        self.timeout_img=ImageTk.PhotoImage(self.img)
        
        self.rtm_btn=tk.Button(image=self.timeout_img, bg="black", bd=0, cursor='hand2', command=lambda:self.countdown_first("r"))
        self.rtm_btn.grid(row=6,column=0)
        self.rtmt_btn=tk.Button(text="----", font="微軟正黑體 60", bg="black", fg="#FF66CC", bd=0, cursor='hand2', command=self.r_stop, state="disable")
        self.rtmt_btn.grid(row=6,column=1)

        self.btm_btn=tk.Button(image=self.timeout_img, bg="black", bd=0, cursor='hand2', command=lambda:self.countdown_first("b"))
        self.btm_btn.grid(row=6,column=9)
        self.btmt_btn=tk.Button(text="----", font="微軟正黑體 60", bg="black", fg="#FF66CC", bd=0, cursor='hand2', command=self.b_stop, state="disable")
        self.btmt_btn.grid(row=6,column=10)
    # 計時器 row7 ============================================
        self.clk_lb=tk.Label(text="3:00", font="微軟正黑體 150", bg="black", fg="green")
        self.clk_lb.grid(row=7,column=0,columnspan=13)
        
        self.clk=self.clock
        self.clkid=None
        
        self.time_state=["start.jpg","pause.jpg","reset.png"]
        for i in range(3):
            self.img=Image.open(self.time_state[i])
            exec(f"self.{self.time_state[i][:-4]}_img=ImageTk.PhotoImage(self.img)")

        self.start_btn=tk.Button(image=self.start_img, bg="black", bd=0, cursor='hand2', command=self.start)
        self.start_btn.grid(row=3,column=6)
        self.pause_btn=tk.Button(image=self.pause_img, bg="black", bd=0, cursor='hand2', command=self.pause, state="disabled")
        self.pause_btn.grid(row=4,column=6)
        self.reset_btn=tk.Button(image=self.reset_img, bg="black", bd=0, cursor='hand2', command=self.reset, state="disabled")
        self.reset_btn.grid(row=6,column=6)
        
        self.app.mainloop()
        
        
    def FullScreenSwitch(self,event):
        self.fullScreenState = not self.fullScreenState
        self.app.attributes("-fullscreen", self.fullScreenState)
        
    def quit(self,event):
        self.app.destroy()
        
    def change3min(self,event):
        self.clk_lb.config(text="3:00",fg="green")
        self.clock=180.9
        self.clk=self.clock
        
    def change2min(self,event):
        self.clk_lb.config(text="2:00",fg="green")
        self.clock=120.9
        self.clk=self.clock

    def change1min(self,event):
        self.clk_lb.config(text="1:00",fg="green")
        self.clock=60.9
        self.clk=self.clock
        
    def r_ch_name(self,event):
        self.rn=self.rn_en.get()
        self.rt_lb.config(text=self.rn)
        
    def b_ch_name(self,event):
        self.bn=self.bn_en.get()
        self.bt_lb.config(text=self.bn)

    def heart_count(self,c):
        exec(f"self.{c}h-=1")
        exec(f"if self.{c}h<0 : self.{c}h=3")
        exec(f"self.ch=self.{c}h")
        exec(f"self.{c}h_btn.config(image=self.h{self.ch}_img)")
        exec(f"if self.{c}h==0 : self.alarm_win('{self.switch[c]}')")
            
    def yellow_count(self,c):
        exec(f"self.{c}yc+=1")
        exec(f"if self.{c}yc>2 : self.{c}yc=0")
        exec(f"self.cyc=self.{c}yc")
        exec(f"self.{c}yc_btn.config(image=self.yc{self.cyc}_img)")
        exec(f"if self.{c}yc==2 : self.heart_count('{c}')")
    
    def countdown_first(self,c):
        exec(f"self.heart_count('{c}')")
        exec(f"self.{c}tm_btn.config(state='disabled')")
        exec(f"self.{c}tmt_btn.config(state='normal')")
        exec(f"self.{c}_countdown()")
        
    def to_time(self,t):
        Min=str(int(t//60))
        Sec=str(int(t%60))
        Dot=str(t%1)[1:4] #從.開始
        
        if len(Sec)<2 : Sec="0"+Sec
        if 60<=t : return f"{Min}:{Sec}"
        elif 10<=t<60 : return f"{Sec}{Dot[:2]}"
        elif 0<t<10 : return f"{Sec[1:]}{Dot}"
        else : return f"{Sec}"

    def r_countdown(self):
        if self.rt>0:
            self.rtmt_btn.config(text=self.to_time(self.rt))
            self.rt-=self.batch_time
            self.rid=self.rtmt_btn.after(self.after_time,self.r_countdown)
        else:
            self.rtmt_btn.config(text="----")
            self.rt=self.time_out
            self.rtm_btn.config(state="normal")
            self.rtmt_btn.config(state="disabled")
            
    def r_stop(self):
        self.rtm_btn.config(state="normal")
        self.rtmt_btn.config(state="disabled")
        
        if self.rid:
            self.app.after_cancel(self.rid)
            self.rid=None
            self.rtmt_btn.config(text="----")
            self.rt=self.time_out
            
    def b_countdown(self):
        if self.bt>0:
            self.btmt_btn.config(text=self.to_time(self.bt))
            self.bt-=self.batch_time
            self.bid=self.btmt_btn.after(self.after_time,self.b_countdown)
        else:
            self.btmt_btn.config(text="----")
            self.bt=self.time_out
            self.btm_btn.config(state="normal")
            self.btmt_btn.config(state="disabled")
            
    def b_stop(self):
        self.btm_btn.config(state="normal")
        self.btmt_btn.config(state="disabled")
        
        if self.bid:
            self.app.after_cancel(self.bid)
            self.bid=None
            self.btmt_btn.config(text="----")
            self.bt=self.time_out
            
    def start(self):
        if not self.fighting:
            round = 7 - (self.rh + self.bh)
            print(self.rh,self.bh)
            if round >= 3: round = 3
            self.play_effect(f"round{round}.mp3")
            self.fighting = True
        self.start_btn.config(state="disabled")
        self.pause_btn.config(state="normal")
        self.reset_btn.config(state="normal")
        
        if self.clk>0:
            if 60<=self.clk: self.clk_lb.config(fg="green")
            elif 30<=self.clk<60: self.clk_lb.config(fg="yellow")
            elif 10<=self.clk<30: self.clk_lb.config(fg="orange")
            else: self.clk_lb.config(fg="red")
            self.clk_lb.config(text=self.to_time(self.clk))
            self.clk-=self.batch_time
            self.clkid=self.clk_lb.after(self.after_time,self.start)
        else:
            self.clk_lb.config(text="Time's Up!")
            self.clk=self.clock
            
            self.start_btn.config(state="disabled")
            self.pause_btn.config(state="disabled")
            self.reset_btn.config(state="normal")
            
    def pause(self):
        self.fighting = False
        self.start_btn.config(state="normal")
        self.pause_btn.config(state="disabled")
        self.reset_btn.config(state="disabled")
        
        if self.clkid:
            self.app.after_cancel(self.clkid)
            self.clkid=None
        
    def reset(self):
        self.start_btn.config(state="normal")
        self.pause_btn.config(state="disabled")
        self.reset_btn.config(state="disabled")
        
        self.app.after_cancel(self.clkid)
        self.clkid=None

        if self.clock==180.9:
            self.clk_lb.config(text="3:00",fg="green")
        elif self.clock==120.9:
            self.clk_lb.config(text="2:00",fg="green")
        elif self.clock==60.9:
            self.clk_lb.config(text="1:00",fg="green")
        self.clk=self.clock
        
    def alarm_win(self,c):
        self.play_effect("win.mp3")
        self.win=tk.Tk()
        self.win.title("Victory")
        self.win.attributes('-topmost', True)
        self.win.attributes("-fullscreen", True)
        exec(f"self.win.config(bg=self.{c})")
        self.win.grid_rowconfigure(0, weight=1)
        self.win.grid_columnconfigure(0, weight=1)
        self.win.grid_rowconfigure(2, weight=1)
        self.win.grid_columnconfigure(2, weight=1)
        
        exec(f"self.win_lb=tk.Label(self.win, text='👑WINNER👑', font='微軟正黑體 150 bold', bg=self.{c}, fg='yellow')")
        self.win_lb.grid(row=0, column=1)
        exec(f"self.name_lb=tk.Label(self.win, text=self.{c}n, font='微軟正黑體 120 bold', bg=self.{c}, fg='white')")
        self.name_lb.grid(row=1, column=1)
        self.leave_btn=tk.Button(self.win, text='exit', font='微軟正黑體 30', bg='yellow', fg='black', bd=0, command=self.quit_win)
        self.leave_btn.grid(row=2, column=1)

        self.win.mainloop()
    
    def quit_win(self):
        self.ryc=self.byc=3
        self.rh=self.bh=-1
        
        self.heart_count("r")
        self.heart_count("b")
        self.yellow_count("r")
        self.yellow_count("b")
        self.win.destroy()

    def play_effect(self, file): # 播放音效
        sound = pygame.mixer.Sound(file)
        sound.set_volume(1)
        sound.play()

a=APP()