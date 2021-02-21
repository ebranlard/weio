# -*- coding: utf-8 -*-
import os
import numpy as np
import re
import pandas as pd
# from binaryornot.check import is_binary 

class BladedFile:
    """
    Read a Bladed out put file (current version is only binary files)
    
    Main methods:
        read: it finds all % and $ files based on selected .$PJ file and calls "DataValue" to read data from all those files
        DataValue: it calls "SensorLib" method to find information about each %, $ file, and then read data based on those info
        OrgData: is is called by "DataValue" to sort channels and values
        toDataFrame: create Pandas dataframe output
        
        

    example: 
        filename = r'h:\004_Loads\Sim\Bladed\003\Ramp_up\Bladed_out_ascii.$04'        
        Output = Read_bladed_file(filename)
        df = Output.toDataFrame()
        
    """ 
    @staticmethod
    def defaultExtensions():
        return ['.%*', '.$*'] 

    @staticmethod
    def formatName():
        return 'Bladed output file'
    
    
    
    def __init__(self, filename=None, **kwargs):
        self.filename = None
        if filename:
            self.file_name = filename
            self.read()
        
        
  #--- a function to read sensors     
    def SensorLib(self):        
        fid = open(os.path.join(self.Folder_in,self.files_in), 'r')
        read_sensor = fid.readlines()
        i = -1
        
        ## read sensor file line by line (just read up to line 20)
        while i < 20: 
            i += 1
            t_line = read_sensor[i]
            # print(i)
            
            # check what is matrix dimension of the file. For blade & tower,  
            # the matrix is 3-dimensional. 
            if re.search('^NDIMENS',t_line):
                
                temp = []
                temp_2 = []
        
                temp =  t_line 
                temp_2 = str.split(temp,'\t')
                NDIMENS = int(temp_2[1]);
            
            # check what is the size of the matrix
            # for example, it can be 11x52500 or 12x4x52500            
            if re.search('^DIMENS',t_line):
                # print(i) # to debug
                temp = []
                temp_2 = []
                if NDIMENS == 3:
                    temp =  t_line 
                    temp_2 = str.split(temp,'\t')
                    SensorNumber = int(temp_2[1])
                    DataLength = int(temp_2[3])
                    
                    
                elif NDIMENS == 2:
                    temp =  t_line 
                    temp_2 = str.split(temp,'\t')
                    SensorNumber = int(temp_2[1])
                    DataLength = int(temp_2[2])  
                    NoOfSections = 1
                    SectionList = []
            
            # check the percision: is it 4 or 8?
            if re.search('FORMAT', t_line):
                # print(t_line)
                temp = t_line.split()
                Precision = int(temp[-1][-1])
            
            # check the category of the file you are reading:
            if re.search('GENLAB', t_line):
                # print(t_line)
                temp = t_line.split('\t')
                temp_2 = temp[-1]
                temp_2.strip() # removing /n from the end
                category = temp_2.replace('\n','')
            
            # what is section on the 3rd dimension you are reading
            # sometimes, the info is written on "AXITICK"
            if re.search('^AXIVAL',t_line):
                # print(t_line)
                temp = t_line
                temp_2 = str.split(temp)
                SectionList = np.array(temp_2[1:], dtype=float)
                NoOfSections = len(SectionList)
            
            # what is section on the 3rd dimension you are reading
            # sometimes, the info is written on "AXIVAL"
            if re.search('AXITICK', t_line):
                # print(t_line)
                temp = t_line
                temp_2 = str.split(temp)
                SectionList = np.array(temp_2[1:], dtype=float)
            
            # Here you can find channel names:    
            if re.search('^VARIAB',t_line):
                # print(t_line)
                temp = t_line.split('\t')
                name_tmp = temp[1]
                name_tmp_2 = name_tmp.split('\'')
                name_tmp_3 = []
                for j in range(len(name_tmp_2)):
                    if name_tmp_2[j] != ' ' and name_tmp_2[j] != '' and name_tmp_2[j] != '\n':
                        # print( name_tmp_2[j])
                        name_tmp_3.append(name_tmp_2[j]) 
                
                ChannelName = name_tmp_3
                
                
            # Here you can find channel units:         
            if re.search('VARUNIT', t_line):
                temp = t_line.split('\t')
                name_tmp = temp[1]
                name_tmp_2 = name_tmp.split(' ')
                name_tmp_2[-1] = name_tmp_2[-1].replace('\n','')
                name_tmp_4 = name_tmp_2
                for j in range(len(name_tmp_2)):
                    ## rename stupid unit's names of Bladed to SI unit's name
                    name_tmp_4[j] = name_tmp_2[j].replace('T','sec')
                    name_tmp_4[j] = name_tmp_2[j].replace('A','rad')
                    name_tmp_4[j] = name_tmp_2[j].replace('P','W')
                    name_tmp_4[j] = name_tmp_2[j].replace('L','m')
                    name_tmp_4[j] = name_tmp_2[j].replace('F','N')
                    name_tmp_4[j] = name_tmp_2[j].replace('M','Kg')
                ChannelUnit = name_tmp_4
                    
                    

                        
                        
        # remember to keep it out of while loop        
        return ChannelName, Precision, SectionList,NoOfSections,category,DataLength,SensorNumber, NDIMENS, ChannelUnit                
                
##  ----- a function to organize data -------------------------------- 
    def OrgData(self,DataLength,SectionList,ChannelName,data_tmp,NDIMENS,ChannelUnit):
            
        # since some of the matrices are 3 dimensional, we want to make all 
        # to 2d matrix, so I am organizing them here:
            if NDIMENS == 3:
                
                data_T = np.transpose(data_tmp)
                SName = []
                SUnit = []
                self.DataOut = np.ones( (DataLength,len(SectionList)*len(ChannelName)) ) 
                
                col_vec = -1
                for ss in range(len(SectionList)):
                    for cc in range(len(ChannelName)):                    
                
                        SName.append(str(SectionList[ss]) + 'm-' + ChannelName[cc])
                        SUnit.append(str(SectionList[ss]) + 'm-' + ChannelUnit[cc])
                        col_vec +=1
                        self.DataOut[:,col_vec] = data_T[:,ss,cc]
                        
            elif NDIMENS == 2:
                data_T = np.transpose(data_tmp)
                SName = []
                self.DataOut = np.ones( (DataLength,len(ChannelName)) ) 
                col_vec = -1
                
                self.DataOut = data_T
                SName = ChannelName
                SUnit = ChannelUnit
            
            self.SensorName = SName
            self.SensorUnit = SUnit




# main function to read the data and call other functions:
    def DataValue(self):
        
        # call "find_files" function to find all %, $ files
        # self.find_files()
        
        ChannelName, Precision, SectionList, NoOfSections, category, DataLength, SensorNumber, NDIMENS, ChannelUnit  = self.SensorLib()
        
        print(self.files_in)
        ## Read only files that ends with $:
        file_in = self.files_in.replace('%','$')
        fid_2 = open(os.path.join(self.Folder_in,file_in), 'r')
        
        """
        I comment binary check here and assume it is always binary
        """
        Binary_test_2 = True #is_binary(os.path.join(self.Folder_in,file_in))
        
        if Precision == 4:
            tmp_2 = np.fromfile(fid_2, np.float32)
        elif Precision == 8:
            tmp_2 = np.fromfile(fid_2, np.float64)
            
        if Binary_test_2 is True:            # it is binary            
            if NDIMENS == 3:
                tmp_3 = np.reshape(tmp_2,(SensorNumber, NoOfSections, DataLength), order='F')
                data_tmp = tmp_3
                # self.data_T = np.transpose(tmp_3)
            
               
                
            elif NDIMENS == 2:
                tmp_3 = np.reshape(tmp_2,(SensorNumber, DataLength), order='F')
                data_tmp = tmp_3
                
        else:
            # print('it is ascii')
            if NDIMENS == 2:
               tmp_3 = np.loadtxt(os.path.join(self.Folder_in,file_in)) 
               data_tmp = np.reshape(tmp_3,(SensorNumber, DataLength), order='F')
           
            if NDIMENS == 3:
                tmp_3 = np.loadtxt(os.path.join(self.Folder_in,file_in),) 
                print(file_in)
                
            
                n_rows = int(tmp_3.shape[0]/len(SectionList))
                n_cols = int(len(SectionList)*len(ChannelName))
                temp_4 = np.zeros( [n_rows,n_cols])
                
                ## Bladed ascii file is written so stupid when matrix is 3 dimensional: 
                col_nr = 0 
                for rr in range(len(SectionList)):
                    dd = 0
                    for ss in range(rr,int(tmp_3.shape[0]),len(SectionList)):  
                        
                        temp_4[dd, col_nr:int(len(ChannelName))+col_nr] = tmp_3[ss,:]
                        dd += 1
                    
                    col_nr += len(ChannelName)
                data_tmp = np.reshape(temp_4,(SensorNumber, NoOfSections, DataLength), order='F')            
        
        self.OrgData(DataLength,SectionList,ChannelName,data_tmp,NDIMENS,ChannelUnit)

    
    
  
    
  
# %% find all %, $ files:
    
    def read(self):
        file_name_0 = self.file_name
        file_name_1 = file_name_0.replace('\\' , '/')
        file_name_2 = file_name_1.split('/')
        pth = self.file_name.replace(file_name_2[-1],'') # remove file name
        keep_filename = file_name_2[-1][:-4]
        # keep_filename = file_name_2[-1].replace('.$PJ','')
        searchName = keep_filename + '.%'
        pth = pth[:-1] #  keep only the path
        files_out = [] 
        Folder_out = []
        jj = 0
        for Folder, sub_folder, files in os.walk(pth):
            for i in range(len(files)): 
                if searchName in files[i]:
                    
                    jj +=1 # check if it is the first file
                    files_out.append(files[i])
                    Folder_out.append(Folder)    
                    
                    
                    # Call "Read_bladed_file" function to Read and store data:
                    self.Folder_in = Folder
                    self.files_in = files[i]
                    self.DataValue()    
                    
                    # gather all channel files together:
                    if jj == 1: # for the 1st index, create a variable with file name
                        
                        # name = files_out[0][:-4]
                        self.BL_Data = self.DataOut
                        self.BL_SensorNames = self.SensorName
                        self.BL_SensorUnits = self.SensorUnit
                    else: # append the rest, but in axis=1
                        # name = files_out[0][:-4]
                        self.BL_Data =  np.append(self.BL_Data, self.DataOut, axis=1)
                        for ind_s in range(len(self.SensorName)):
                            self.BL_SensorNames.append(self.SensorName[ind_s])
                            self.BL_SensorUnits.append(self.SensorUnit[ind_s])
            
            self.BL_ChannelUnit =[]
            for jjj, name_unit in enumerate(self.BL_SensorNames):
                self.BL_ChannelUnit.append(self.BL_SensorNames[jjj] + '[' + self.BL_SensorUnits[jjj] + ']')
            
            ## outputs are:
            ## self.BL_Data
            ## self.BL_ChannelUnit
                
    def toDataFrame(self):        
        df = pd.DataFrame(data=self.BL_Data, columns=self.BL_ChannelUnit)
        return df
    

                    
      

#filename = r'E:\Work_Google Drive\Bladed_Sims\Bladed_out_binary.$41'

#Output = BladedFile(filename)
#df = Output.toDataFrame()


