# -*- coding: utf-8 -*-
import os
import numpy as np
import re
import pandas as pd

from .file import File, isBinary

class BladedFile(File):
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
            self.filename = filename
            self.read()
        
        
  #--- a function to read sensors     
    def SensorLib(self, sensorfile):        
        with open(sensorfile, 'r') as fid:
            read_sensor = fid.readlines()
        i = -1
        
        ## read sensor file line by line (just read up to line 20)
        while i < 17: 
            i += 1
            t_line = read_sensor[i]
            # print(i)
            
            # check what is matrix dimension of the file. For blade & tower,  
            # the matrix is 3-dimensional. 
            if re.search('^NDIMENS',t_line):
                
                temp = []
                temp_2 = []
        
                temp =  t_line 
                temp_2 = temp.split()
                NDIMENS = int(temp_2[-1]);
            
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
                    if len(temp_2) == 1:
                        temp_2 = str.split(temp)
                    
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
                temp_2 = str.split(temp,'\' \'')
                temp_2[0] = temp_2[0].replace('AXITICK\t','')
                SectionList = np.array(temp_2[:], dtype=str)
                NoOfSections = len(SectionList)
            
            # Here you can find channel names:    
            if re.search('^VARIAB',t_line):
                # print(t_line)
                temp = t_line.split('\t')
                if len(temp) == 1:
                    temp = t_line.split('   ') # use 3 space instead of TAB
                try:    
                    name_tmp = temp[1]
                except:
                    name_tmp = temp[0]
                    
                name_tmp_2 = name_tmp.split('\'')
                name_tmp_3 = []
                for j in range(len(name_tmp_2)):
                    if name_tmp_2[j] != ' ' and name_tmp_2[j] != '' and name_tmp_2[j] != '\n' and name_tmp_2[j] != 'VARIAB ':
                        # print( name_tmp_2[j])
                        name_tmp_3.append(name_tmp_2[j]) 
                
                ChannelName = name_tmp_3
                
                
            # Here you can find channel units:         
            if re.search('VARUNIT', t_line):
                # temp = t_line.split('\t')
                # if len(temp)<2:
                temp = t_line.split()
                name_tmp_2 = temp[1:]
                # name_tmp = temp[1]
                # name_tmp_2 = name_tmp.split(' ')
                # name_tmp_2[-1] = name_tmp_2[-1].replace('\n','')
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
            self.Data_Length_out = DataLength



# main function to read the data and call other functions:
    def DataValue(self, rootFolder, sensorfile):
        
        # call "find_files" function to find all %, $ files
        # self.find_files()
        sensorfile_full=os.path.join(rootFolder, sensorfile)
        
        ChannelName, Precision, SectionList, NoOfSections, category, DataLength, SensorNumber, NDIMENS, ChannelUnit  = self.SensorLib(sensorfile_full)
        
        ## Read only files that ends with $:
        file_in = sensorfile.replace('%','$')

        filename = os.path.join(rootFolder, file_in)
        Binary_test_2 = isBinary(filename)
        
        with open(os.path.join(filename), 'r') as fid_2:
            if Precision == 4:
                tmp_2 = np.fromfile(fid_2, np.float32)
            elif Precision == 8:
                tmp_2 = np.fromfile(fid_2, np.float64)
            
        if Binary_test_2:            # it is binary            
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
                try:
                    tmp_3 = np.loadtxt(filename) 
                    data_tmp = np.transpose(tmp_3)#np.reshape(tmp_3,(SensorNumber, DataLength), order='F')
                except:
                    ####  I am getting tired of bladed, so just leave it empty if it is not possible to read it.
                    data_tmp = np.empty((SensorNumber, DataLength)) * np.nan

                    # data_tmp =[] #
           
            if NDIMENS == 3:
                try:
                    tmp_3 = np.loadtxt(filename) 
                    #print(file_in)
                    
                
                    temp_4 = np.zeros([SensorNumber,NoOfSections,DataLength])
                    
                     
                    
                    ## Bladed ascii file is written so stupid when matrix is 3 dimensional: 
                    for nsec in range(NoOfSections):
                        # print('nsec',nsec)
                        dd_new = 0
                        for dd in range(nsec,int(tmp_3.shape[0]),NoOfSections): #enumerate(np.arange(nsec,int(tmp_3.shape[0]),NoOfSections)):
                            # print('dd',dd)
                            # print(dd_new)
                            temp_4[:,nsec,dd_new] = tmp_3[dd,:]
                            dd_new += 1 # it should go up to "DataLength"
                    data_tmp = np.reshape(temp_4,(SensorNumber, NoOfSections, DataLength), order='F') 
                    
                except:
                    data_tmp = np.empty((SensorNumber, NoOfSections, DataLength)) * np.nan
        
        self.OrgData(DataLength,SectionList,ChannelName,data_tmp,NDIMENS,ChannelUnit)

    
    
  
    
  
# %% find all %, $ files:
    
    def _read(self):
        filename_0 = self.filename
        filename_1 = filename_0.replace('\\' , '/')
        filename_2 = os.path.splitext(filename_1)
        
        pth = os.path.dirname(filename_1)
        # pth = self.filename.replace(filename_2[-1],'') # remove file name
        
        filename_3 = filename_2[0].split('/')
        
        keep_filename = filename_3[-1]
              
        # keep_filename = filename_2[-1].replace('.$PJ','')
        searchName = keep_filename + '.%'
        
        # pth = pth[:-1] #  keep only the path
        files_out = [] 
        Folder_out = []
        DataLength_file =[]
        jj = 0
        for Folder, sub_folder, files in os.walk(pth):
            for i in range(len(files)): 
                if searchName in files[i]:
                    
                    jj +=1 # check if it is the first file
                    files_out.append(files[i])
                    Folder_out.append(Folder)    
                    
                    
                    # Call "Read_bladed_file" function to Read and store data:
                    self.DataValue(Folder, files[i])    
                    
                    # gather all channel files together:
                    if jj == 1: # for the 1st index, create a variable with file name
                        
                        # name = files_out[0][:-4]
                        self.BL_Data = self.DataOut
                        self.BL_SensorNames = self.SensorName
                        self.BL_SensorUnits = self.SensorUnit
                        DataLength_file.append(self.Data_Length_out)
                    else: # append the rest, but in axis=1
                        # name = files_out[0][:-4]
                        # skip the file if data length (dimension) is different with the rest:
                        if DataLength_file[0] == self.Data_Length_out: 
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


