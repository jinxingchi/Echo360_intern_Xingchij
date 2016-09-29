from Tkinter import *
import data_plot as d_p
import clean_data as c_d
import claim_analysis as c_a
import Tkinter
import tkMessageBox



class Application(Frame):
    """ A GUI application for claim data analysis """

    def __init__(self, master):
        """ Initialize the Frame """
        ## The constructor ##
        self.loadOption = StringVar(master)
        #self.loadOption.set("")
        self.prodCate = StringVar(master)
        self.prodCate.set('None')
        
        self.prodTime = StringVar(master)
        self.prodTime.set('None')
        
##        self.prodMth = StringVar(master)
##        self.prodMth.set('None')

        self.brandList = c_d.TG_BRAND_CODE
        self.compntList = ['None']
        #c_d.comp_code['Wash']
        self.btnMap = []
        self.txtCompntMap = []
        self.txtUsrSet = []
        
        self.analCtrl = BooleanVar(master)
        self.analCtrl.set(False)

        self.pageCtrl = IntVar(master)
        self.color = d_p.pd.DataFrame()

        self.timeList = d_p.set_prodList()
        self.menuTime = None
        
        Frame.__init__(self, master)
        self.grid()
        self.init_widgets()        

        
        
    def init_widgets(self):
        """ Create widgets on the window. """
        ## Layer 0: Explaination of operation steps
       
        txtExplain = Label(self, text = ("Steps: (1) Load claim data --> "+\
                                         "(2) Select category & production year/month --> "+\
                                         "(3) Click 'Analyze' to show results"),\
                           bg = 'white', font = ("Arial", 12, "bold italic"))
        txtExplain.grid(row = 0, column = 0, columnspan = 5, sticky = W+E)

        ## Layer 1: Control menu and button
        loadList = ["Production volume data","Product claim data"]
        menuLoad = Menubutton(self, text = "Load Datasets", bg = '#EECB1D',\
                           font = ("Arial", 12, "bold"), relief = FLAT,\
                           padx=0, pady=0, activebackground = '#EECB1D')
        
        menuLoad.grid(row = 1, column = 0, sticky = W+E)
        menuLoad.menu = Menu(menuLoad, tearoff = 0)
        menuLoad["menu"] = menuLoad.menu
        menuLoad.menu.add_command(label = "Load claim and production volume data", \
                                  command = lambda cmdUsr = ('load',0): \
                                  self.menuCmd(cmdUsr))

        cateList = ['Wash','Documentation','Structures','Controls']
        menuCate = Menubutton(self, bg = '#EECB1D', text = "Product Sub-system", \
                           font = ("Arial", 12, "bold"), relief = FLAT, \
                           padx=0, pady=0, activebackground = '#EECB1D')
        menuCate.grid(row = 1, column = 1, sticky = W+E)
        menuCate.menu = Menu(menuCate, tearoff = 0)
        menuCate["menu"] = menuCate.menu
        for cate in cateList:
            menuCate.menu.add_command(label = cate, command = lambda cmdUsr = \
                                      ('cate',cateList.index(cate)): self.menuCmd(cmdUsr))

        ## automated year list ##
  
       # timeList = d_p.set_prodList()
        self.menuTime = Menubutton(self, bg = '#EECB1D', text = "Production Y-M", \
                           font = ("Arial", 12, "bold"), relief = FLAT, \
                           padx=0, pady=0, activebackground = '#EECB1D')
        self.menuTime.grid(row = 1, column = 2, sticky = W+E)

        self.menuTime.menu = Menu(self.menuTime, tearoff = 0)
        self.menuTime["menu"] = self.menuTime.menu

        
        for time in self.timeList:
            parts = time.split('-')
            month = parts[0]
            year = parts[1]
            self.menuTime.menu.add_command(label = time, command = lambda cmdUsr = \
                                      ('time',self.timeList.index(time)): self.menuCmd(cmdUsr))
        btnSubmit = Button(self, text = "Analyze", fg = 'red',\
                         bg = '#EECB1D', font = ("Arial", 12, "bold"))


        ##
        btnSubmit.grid(row = 1, column = 4, sticky = W+E)
        btnSubmit['command'] = self.analyze

        ## Layer 2
        layer2Fm = Frame(self)
        layer2Fm.grid(row = 2, column = 0, columnspan = 5, sticky = W+E)            
        ## Layer 2: Claim map
        mapFm = Frame(layer2Fm, bg = 'gray')
        mapFm.grid(row = 0, column = 0, rowspan = 4, padx = 1, pady = 1, sticky = W)
        txtMapTitle = Label(mapFm, text = 'Claim Rate Map of Components', \
                            fg = 'black', bg = 'gray', font = ("Arial", 9, "bold"))
        txtMapTitle.grid(row = 0, column = 0, columnspan = 19, sticky = W+E)

        
        ## iterate over each brand_code ##
        ##Scomp_len = len(c_d.comp_code['Wash'])
        disp_len = 20
        i = 0
        while i <= 18:
        
            j = 0
            while j <= disp_len:
             
                if (j == 0) & (i <= 17):
                    txtBrand = Label(mapFm, width = 8, height = 1, bg = 'gray', \
                                     font = ("Arial", 9, "bold"), text = self.brandList[i])
                    txtBrand.grid(row = i+1, column = j, pady= 2)
                elif (j >= 1) & (i == 18):
                    txtCompnt = Label(mapFm, width = 3, height = 1, bg = 'gray', \
                                     font = ("Arial", 8, "bold"), text = 'xxx')
                    txtCompnt.grid(row = 19, column = j, pady= 2)
                    self.txtCompntMap.append(txtCompnt)
                elif (j == 0) & (i == 18):
                    pass
                else:           
                        
                    brand_code = self.brandList[i]
                    compnt_code = 'xxx'

                    ## -------------------------------------------------------------------------##
                    ##               This is where I make changes to button text                 ##
                    ## ---------------------------------------------------------------------------##
                    mapBtn = Button(mapFm, width = 3, height = 1, text = '', bg = 'gray', relief = RIDGE)
                    mapBtn['command'] = lambda target = (brand_code, compnt_code):\
                                    self.compnt_plot(target)

                    mapBtn.grid(row = i+1, column = j, padx = 2, pady= 2)
                    self.btnMap.append(mapBtn) 
                j += 1
            i += 1
        
        ## Layer 2: Display of user settings
        dispUsrFM = Frame(layer2Fm)
        dispUsrFM.grid(row = 0, column = 1, sticky = W+E)
        dispList = ["Product Sub-system:", "Production Y-M:"]
        i = 0
        while i < 3:
            if i == 0:
                txtUsr = Label(dispUsrFM, relief = FLAT, text = "User settings:", \
                               font = ("Arial", 9, "bold"))
                txtUsr.grid(row = 0, column = 0, columnspan =2, padx = 2, pady = 2, sticky = W+E)
            else:
                j = 0
                while j < 2:
                    if j == 0:                            
                        txtUsr = Label(dispUsrFM, relief = FLAT, text = dispList[i-1], \
                                       font = ("Arial", 9, "bold"))
                        txtUsr.grid(row = i, column = 0, pady = 2, sticky = W+E)
                    else:
                        txtUsr = Label(dispUsrFM, bg = 'white', relief = FLAT, width = 10, height = 1)
                        txtUsr.grid(row = i, column = 1, pady = 2, sticky = W+E)
                        self.txtUsrSet.append(txtUsr)
                    j += 1
            i += 1
        
        
        ## Layer 2: Claim map legend
        legendFm = Frame(layer2Fm)
        legendFm.grid(row = 1, column = 1, sticky = W+E)
        txtLegend = Label(legendFm, text = "Map legend:", font = ("Arial", 9, "bold"))
        txtLegend.grid(row = 0, column = 0, columnspan = 2, sticky = W, pady = 1)
        bntNA = Button(legendFm, width = 3, height = 1, bg = 'gray', relief=FLAT)
        bntNA.grid(row = 1, column = 0, sticky = W, pady = 1)
        txtNA = Label(legendFm, text = " -- NaN", font = ("Arial", 9, "bold"))
        txtNA.grid(row = 1, column = 1, sticky = W, pady = 1)
        bntIn = Button(legendFm, text = 'Y',  width = 3, height = 1, bg = '#EECB1D', relief=FLAT)
        bntIn.grid(row = 2, column = 0, sticky = W, pady = 1)
        txtIn = Label(legendFm, text = " -- Within range", font = ("Arial", 9, "bold"))
        txtIn.grid(row = 2, column = 1, sticky = W, pady = 1)
        bntLow = Button(legendFm, text = 'G', width = 3, height = 1, bg = 'green', relief=FLAT)
        bntLow.grid(row = 3, column = 0, sticky = W, pady = 1)
        txtLow = Label(legendFm,text = " -- Lower than lower bound", \
                       font = ("Arial", 9, "bold"))
        txtLow.grid(row = 3, column = 1, sticky = W, pady = 1)
        bntHigh = Button(legendFm, width = 3, text = 'R', height = 1, bg = 'red', relief=FLAT)
        bntHigh.grid(row = 4, column = 0, sticky = W, pady = 1)
        txtHigh = Label(legendFm, text = " -- Higher than upper bound", \
                        font = ("Arial", 9, "bold"))
        txtHigh.grid(row = 4, column = 1, sticky = W, pady = 1)

        ## Layer 2: Next/back Arrow
        ArrowFm = Frame(layer2Fm)
        ArrowFm.grid(row = 2, column = 1, columnspan = 2, sticky = W+E+S)
        btnBack = Button(ArrowFm, text = "<<  Go  Back", font = ("Arial", 9, "bold"),\
                        height = 3, command = lambda usrCmd = 'back': self.page_ctrl(usrCmd))
        btnBack.grid(row = 0, column = 0, padx = 3, pady = 1, sticky = W+E)
        btnNxt = Button(ArrowFm, text = "Next Page >>", font = ("Arial", 9, "bold"),\
                        height = 3, command = lambda usrCmd = 'next': self.page_ctrl(usrCmd))
        btnNxt.grid(row = 0, column = 1, padx = 3, pady = 1, sticky = W+E)
        
        ## Layer 2: Logo
        logoFm = Frame(layer2Fm)
        logoFm.grid(row = 3, column = 1, columnspan = 2, sticky = W+E+S)
        img = PhotoImage(file = "logo.gif")
        imgLogo = Label(logoFm, image = img)
        imgLogo.image = img
        imgLogo.grid(row = 0, column = 0, padx = 0, pady = 0, sticky = W+E+S)

    def menuCmd(self, cmdUsr):
        cateList = ['Wash','Documentation','Structures','Controls']
        if cmdUsr[0] == 'load':
            c_d.loadData()
            tkMessageBox.showinfo('Information',"Data has been (re)loaded!")
            self.menuTime.menu.delete(0,len(self.timeList)-1)

            self.timeList = d_p.set_prodList()

            for time in self.timeList:
                parts = time.split('-')
                month = parts[0]
                year = parts[1]
                self.menuTime.menu.add_command(label = time, command = lambda cmdUsr = \
                                      ('time',self.timeList.index(time)): self.menuCmd(cmdUsr))
        elif cmdUsr[0] == 'cate':
           
            self.prodCate.set(cateList[cmdUsr[1]])
            self.txtUsrSet[0]['text'] = self.prodCate.get()
         
        elif  cmdUsr[0] == 'time':
           
            self.prodTime.set(self.timeList[cmdUsr[1]])
            self.txtUsrSet[1]['text'] = self.prodTime.get() 
         
    def page_ctrl(self, pageUsr):
        if not self.analCtrl.get():
            tkMessageBox.showinfo('Warning',"Please make analysis first!")
        elif pageUsr == 'next':
            self.pageCtrl.set(self.pageCtrl.get()+1)
            self.disp_update()
        elif pageUsr == 'back':
            if self.pageCtrl.get() >= 1:
                self.pageCtrl.set(self.pageCtrl.get()-1)
                self.disp_update()

    def analyze(self):
        if self.prodCate.get() == 'None' or self.prodTime.get() == 'None':
            tkMessageBox.showinfo('Warning',"Please select product sub-system and production year/month!")
        else:
            self.analCtrl.set(True)
            
            prodDate = str(self.prodTime.get())
           
            c = 0
            if len(prodDate) == 6:
                c = c + 1
                prodDate = '0' + prodDate
               

            parts = prodDate.split('-')
            month = parts[0]
            year = parts[1]

            prodDate = year + '-' + month
            c_a.claimAnalyze(prodDate, self.prodCate.get())

            # ------------------------------------------------------#
            self.color = d_p.set_color(prodDate, self.prodCate.get())
            self.compntList = c_d.comp_code[self.prodCate.get()]
            self.pageCtrl.set(0)
            self.disp_update()

    def disp_update(self):
        colorList = ['red', 'green', '#EECB1D', 'gray']
        
        ## -------------------------------------------------------------------------##
        ##               This is where I make changes to button text                 ##
        ## ---------------------------------------------------------------------------##
        
        textList = ['R', 'G', 'Y', '']

        ##text = self.text
        
        color = self.color
        page = self.pageCtrl.get()
        disp_len = 20
        compnt_len = len(self.compntList)            
        i = 0
        while i <= 18:
            j = 0
            while j <= disp_len:
                if j == 0:
                    pass
                elif (j >= 1) & (i == 18):
                    if ((j+20*page) <= compnt_len):
                        self.txtCompntMap[j-1]['text'] = self.compntList[j+20*page-1]
                    else:
                        self.txtCompntMap[j-1]['text'] = 'xxx'
                else:                            
                    brand_code = self.brandList[i]
                    if ((j+20*page) <= compnt_len):
                        compnt_code = self.compntList[j+20*page-1]
                    else:
                        compnt_code = 'xxx'
                    bgColor = color[(color['brand_code'] == brand_code) & \
                                    (color['component_code'] == compnt_code)]['color_code'].astype(int)
                    
                    if bgColor.empty:
                        bgColor = [3]
                    else:
                        self.btnMap[i*20+j-1]['command'] = lambda target = (brand_code, compnt_code):\
                                    self.compnt_plot(target)
                        
                    self.btnMap[i*20+j-1]['bg'] = colorList[bgColor[0]]
                    self.btnMap[i*20+j-1]['text'] = textList[bgColor[0]]

                j += 1
            i += 1
        

    def compnt_plot(self, target):
        brand_code = target[0]
        compnt_code = target[1]
        if not self.analCtrl.get():
            tkMessageBox.showinfo('Warning',"Please make analysis first!")
        else:
            prodDate = str(self.prodTime.get())
            
            if len(prodDate) == 6:
                prodDate = '0' + prodDate

            parts = prodDate.split('-')
            month = parts[0]
            year = parts[1]

            prodDate = year + '-' + month
            if compnt_code != 'xxx':
                d_p.data_plot(prodDate, brand_code, compnt_code)
        

        
## create & initialize main window
root = Tk()

root.title("Claim Rate Analysis Tool -- ver 1.0")
root.geometry()
app = Application(root)
## run the main window
root.mainloop()
