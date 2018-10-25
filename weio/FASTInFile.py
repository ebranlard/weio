from __future__ import absolute_import
from .File import File, WrongFormatError
import numpy as np
import re
import pandas as pd

# from .dtuwetb import fast_io
# TODO members for  BeamDyn with mutliple key point
NUMTAB_FROM_VAL_DETECT   = ['HtFract'  , 'TwrElev'   , 'BlFract'  , 'Genspd_TLU' , 'BlSpn'    , 'WndSpeed' , 'HvCoefID' , 'AxCoefID' , 'JointID' , 'PropSetID'         , 'Dpth'      , 'FillNumM'    , 'MGDpth'    , 'SimplCd'  , 'RNodes' ,'kp_xr']
NUMTAB_FROM_VAL_DIM_VAR  = ['NTwInpSt' , 'NumTwrNds' , 'NBlInpSt' , 'DLL_NumTrq' , 'NumBlNds' , 'NumCases' , 'NHvCoef'  , 'NAxCoef'  , 'NJoints' , 'NPropSets'         , 'NCoefDpth' , 'NFillGroups' , 'NMGDepths' , 1          , 'BldNodes','kp_total']
NUMTAB_FROM_VAL_VARNAME  = ['TowProp'  , 'TowProp'   , 'BldProp'  , 'DLLProp'    , 'BldNodes' , 'Cases'    , 'HvCoefs'  , 'AxCoefs'  , 'Joints'  , 'MemberSectionProp' , 'DpthProp'  , 'FillGroups'  , 'MGProp'    , 'SmplProp' , 'BldNodes','MemberGeom']
NUMTAB_FROM_VAL_NHEADER  = [2          , 2           , 2          , 2            , 2          , 2          , 2          , 2          , 2         , 2                   , 2           , 2             , 2           , 2          , 1, 2]
NUMTAB_FROM_VAL_DETECT_L = [s.lower() for s in NUMTAB_FROM_VAL_DETECT]

NUMTAB_FROM_LAB_DETECT   = ['NumAlf' ,'F_X'      ,'MemberCd1'    ,'MJointID1','NOutLoc']
NUMTAB_FROM_LAB_DIM_VAR  = ['NumAlf' ,'NKInpSt'  ,'NCoefMembers','NMembers' ,'NMOutputs']
NUMTAB_FROM_LAB_VARNAME  = ['AFCoeff','TMDspProp','MemberProp'   ,'Members'  ,'MemberOuts']
NUMTAB_FROM_LAB_DETECT_L = [s.lower() for s in NUMTAB_FROM_LAB_DETECT]

FILTAB_FROM_LAB_DETECT   = ['FoilNm' ,'AFNames']
FILTAB_FROM_LAB_DIM_VAR  = ['NumFoil','NumAFfiles']
FILTAB_FROM_LAB_VARNAME  = ['FoilNm' ,'FoilNm']
FILTAB_FROM_LAB_DETECT_L = [s.lower() for s in FILTAB_FROM_LAB_DETECT]

TABTYPE_NOT_A_TAB          = 0
TABTYPE_NUM_WITH_HEADER    = 1
TABTYPE_NUM_WITH_HEADERCOM = 2
TABTYPE_FIL                = 3
TABTYPE_FMT                = 9999 # TODO

# --------------------------------------------------------------------------------}
# --- INPUT FILE 
# --------------------------------------------------------------------------------{
class FASTInFile(File):

    @staticmethod
    def defaultExtensions():
        return ['.dat','.fst','.txt']

    @staticmethod
    def formatName():
        return 'FAST input file (.dat;.fst)'

    def getID(self,label):
        # brute force search
        for i in range(len(self.data)):
            d = self.data[i]
            if d['label']==label:
                return i
        raise KeyError('Variable '+ label+' not found')

    # Making it behave like a dictionary
    def __setitem__(self,key,item):
        i = self.getID(key)
        self.data[i]['value'] = item

    def __getitem__(self,key):
        i = self.getID(key)
        return self.data[i]['value']


    def _read(self):
        try: 
            with open(self.filename) as f:
                lines = f.read().splitlines()

            # Fast files start with ! or -
            #if lines[0][0]!='!' and lines[0][0]!='-':
            #    raise Exception('Fast file do not start with ! or -, is it the right format?')

            # Parsing line by line, storing each line into a disctionary
            self.data =[]
            i=0    
            nComments  = 0
            nWrongLabels = 0
            while i<len(lines):
                # Each "line" or "meaningful piece of information" is stored in a dictionary
                d = {'value':None, 'label':'', 'isComment':False, 'descr':''}

                line = lines[i]
                # OUTLIST Exceptions
                if line.upper().find('ADDITIONAL OUTPUTS')>0 \
                or line.upper().find('MESH-BASED OUTPUTS')>0 \
                or line.upper().find('OUTPUT CHANNELS'   )>0:
                    # TODO, lazy implementation so far
                    OutList,i = parseFASTOutList(lines,i+1)
                    d['label']   = 'OutList'   # TODO
                    d['tabType'] = TABTYPE_FIL # TODO
                    d['value']   = OutList
                    self.data.append(d)
                    if i>=len(lines):
                        break
                elif line.upper().find('ADDITIONAL STIFFNESS')>0:
                    # TODO, lazy implementation so far
                    i +=1
                    KDAdd = []
                    for _ in range(19):
                        KDAdd.append(lines[i])
                        i +=1
                    d['label']   = 'KDAdd'   # TODO
                    d['tabType'] = TABTYPE_FIL # TODO
                    d['value']   = KDAdd
                    self.data.append(d)
                    if i>=len(lines):
                        break

                # --- Parsing of standard lines: value(s) key comment
                line = lines[i]
                d = parseFASTInputLine(d,line,i)
                    
                # --- Handling of tables
                if isStr(d['value']) and d['value'].lower() in NUMTAB_FROM_VAL_DETECT_L:
                    # Table with numerical values, 
                    ii             = NUMTAB_FROM_VAL_DETECT_L.index(d['value'].lower())
                    d['label']     = NUMTAB_FROM_VAL_VARNAME[ii]
                    d['tabDimVar'] = NUMTAB_FROM_VAL_DIM_VAR[ii]
                    d['tabType']   = TABTYPE_NUM_WITH_HEADER
                    nHeaders       = NUMTAB_FROM_VAL_NHEADER[ii]
                    nTabLines=0
                    #print('Reading table {} Dimension {} (based on {})'.format(d['label'],nTabLines,d['tabDimVar']));
                    if isinstance(d['tabDimVar'],int):
                        nTabLines = d['tabDimVar']
                    else:
                        nTabLines = self[d['tabDimVar']]
                    d['value'], d['tabColumnNames'], d['tabUnits'] = parseFASTNumTable(lines[i:i+nTabLines+nHeaders],nTabLines,i,nHeaders)
                    i += nTabLines+nHeaders-1

                elif isStr(d['label']) and d['label'].lower() in NUMTAB_FROM_LAB_DETECT_L:
                    ii      = NUMTAB_FROM_LAB_DETECT_L.index(d['label'].lower())
                    # Special case for airfoil data, the table follows NumAlf, so we add d first
                    if d['label'].lower()=='numalf':
                        d['tabType']=TABTYPE_NOT_A_TAB
                        self.data.append(d)
                        # Creating a new dictionary for the table
                        d = {'value':None, 'label':'NumAlf', 'isComment':False, 'descr':'', 'tabType':None}
                        i += 1
                    d['label']     = NUMTAB_FROM_LAB_VARNAME[ii]
                    d['tabDimVar'] = NUMTAB_FROM_LAB_DIM_VAR[ii]
                    if d['label'].lower()=='afcoeff' :
                        d['tabType']        = TABTYPE_NUM_WITH_HEADERCOM
                    else:
                        d['tabType']   = TABTYPE_NUM_WITH_HEADER
                    nTabLines = self[d['tabDimVar']]
                    #print('Reading table {} Dimension {} (based on {})'.format(d['label'],nTabLines,d['tabDimVar']));
                    d['value'], d['tabColumnNames'], d['tabUnits'] = parseFASTNumTable(lines[i:i+nTabLines+2],nTabLines,i,2)
                    i += nTabLines+1

                elif isStr(d['label']) and d['label'].lower() in FILTAB_FROM_LAB_DETECT_L:
                    ii             = FILTAB_FROM_LAB_DETECT_L.index(d['label'].lower())
                    d['label']     = FILTAB_FROM_LAB_VARNAME[ii]
                    d['tabDimVar'] = FILTAB_FROM_LAB_DIM_VAR[ii]
                    d['tabType']   = TABTYPE_FIL
                    nTabLines = self[d['tabDimVar']]
                    #print('Reading table {} Dimension {} (based on {})'.format(d['label'],nTabLines,d['tabDimVar']));
                    d['value'] = parseFASTFilTable(lines[i:i+nTabLines],nTabLines,i)
                    i += nTabLines-1
                else:
                    d['tabType'] = TABTYPE_NOT_A_TAB

                self.data.append(d)
                i += 1

                # --- Safety checks
                if d['isComment']:
                    #print(line)
                    nComments +=1
                else:
                    if hasSpecialChars(d['label']):
                        nWrongLabels +=1
                        #print('label>',d['label'],'<',type(d['label']),line);
                        raise WrongFormatError('Special Character found in Label.')
                    if len(d['label'])==0:
                        nWrongLabels +=1
                if nComments>len(lines)*0.35:
                    #print('Comment fail',nComments,len(lines),self.filename)
                    raise WrongFormatError('Most lines were read as comments, probably not a FAST Input File')
                if nWrongLabels>len(lines)*0.10:
                    #print('Label fail',nWrongLabels,len(lines),self.filename)
                    raise WrongFormatError('Too many lines with wrong labels, probably not a FAST Input File')
                 
        except WrongFormatError as e:    
            raise WrongFormatError('Fast File {}: '.format(self.filename)+e.args[0])
        except Exception as e:    
            raise Exception('Fast File {}: '.format(self.filename)+e.args[0])

            

    def _write(self):
        with open(self.filename,'w') as f:
            for i in range(len(self.data)):
                d=self.data[i]
                if d['isComment']:
                    f.write('{}'.format(d['value']))
                elif d['tabType']==TABTYPE_NOT_A_TAB:
                    if isinstance(d['value'], list):
                        sList=', '.join([str(x) for x in d['value']])
                        f.write('{} {} {}'.format(sList,d['label'],d['descr']))
                    else:
                        f.write('{} {} {}'.format(d['value'],d['label'],d['descr']))
                elif d['tabType']==TABTYPE_NUM_WITH_HEADER:
                    f.write('{}'.format(' '.join(d['tabColumnNames'])))
                    if d['tabUnits'] is not None:
                        f.write('\n')
                        f.write('{}'.format(' '.join(d['tabUnits'])))
                    if np.size(d['value'],0) > 0 :
                        f.write('\n')
                        f.write('\n'.join('\t'.join('%15.8e' %x for x in y) for y in d['value']))
                elif d['tabType']==TABTYPE_NUM_WITH_HEADERCOM:
                    f.write('! {}\n'.format(' '.join(d['tabColumnNames'])))
                    f.write('! {}\n'.format(' '.join(d['tabUnits'])))
                    f.write('\n'.join('\t'.join('%15.8e' %x for x in y) for y in d['value']))
                elif d['tabType']==TABTYPE_FIL:
                    f.write('{} {} {}\n'.format(d['value'][0],d['tabDetect'],d['descr']))
                    f.write('\n'.join(fil for fil in d['value'][1:]))
                else:
                    raise Exception('Unknown table type for variable {}',d)
                if i<len(self.data)-1:
                    f.write('\n')

    def _toDataFrame(self):
        dfs={}
        for i in range(len(self.data)): 
            d=self.data[i]
            isATab = d['tabType']==TABTYPE_NUM_WITH_HEADER or d['tabType']==TABTYPE_NUM_WITH_HEADERCOM
            if isATab:
                Val= d['value']
                if d['tabUnits'] is None:
                    Cols=d['tabColumnNames']
                else:
                    Cols=['{}_{}'.format(c,u.replace('(','[').replace(')',']')) for c,u in zip(d['tabColumnNames'],d['tabUnits'])]
                name=d['label']
                dfs[name]=pd.DataFrame(data=Val,columns=Cols)
        return dfs


# --------------------------------------------------------------------------------}
# --- Helper functions 
# --------------------------------------------------------------------------------{
def isStr(s):
    # Python 2 and 3 compatible
    try: 
       basestring # python 2
    except NameError:
       basestring=str #python 3
    return isinstance(s, basestring)

def strIsFloat(s):
    #return s.replace('.',',1').isdigit()
    try:
        float(s)
        return True
    except:
        return False

def strIsBool(s):
    return (s.lower() is 'true') or (s.lower() is 'false')

def strIsInt(s):
    s = str(s)
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()    

def hasSpecialChars(s):
    # fast allows for parenthesis
    # For now we allow for - but that's because of BeamDyn geometry members 
    return not re.match("^[a-zA-Z0-9_()-]*$", s)

def cleanLine(l):
    # makes a string single space separated
    l = l.replace('\t',' ')
    l = ' '.join(l.split())
    l = l.strip()
    return l

def cleanAfterChar(l,c):
    # remove whats after a character
    n = l.find(c);
    if n>0:
        return l[:n]
    else:
        return l


def parseFASTInputLine(d,line_raw,i):
    try:
        # preliminary cleaning (Note: loss of formatting)
        line = cleanLine(line_raw)
        # Comment
        if any(line.startswith(c) for c in ['#','!','--','==']) or len(line)==0:
            d['isComment']=True
            d['value']=line_raw
            return d

        # Detecting lists
        List=[];
        iComma=line.find(',')
        if iComma>0 and iComma<30:
            fakeline=line.replace(' ',',')
            fakeline=re.sub(',+',',',fakeline)
            csplits=fakeline.split(',')
            # Splitting based on comma and looping while it's numbers of booleans
            ii=0
            s=csplits[ii]
            while strIsFloat(s) or strIsBool(s) and ii<len(csplits):
                if strIsInt(s):
                    List.append(int(s))
                elif strIsFloat(s):
                    List.append(float(s))
                elif strIsBool(s):
                    List.append(bool(s))
                else:
                    raise WrongFormatError('Lists of strings not supported.')
                ii =ii+2
                if ii>=len(csplits):
                    raise WrongFormatError('Wrong number of list values')
                s = csplits[ii]
            #print('[INFO] Line {}: Found list: '.format(i),List)
        # Defining value and remaining splits
        if len(List)>=2:
            d['value']=List
            sLast=csplits[ii-1]
            ipos=line.find(sLast)
            line_remaining = line[ipos+len(sLast):]
            splits=line_remaining.split()
            iNext=0
        else:
            # It's not a list, we just use space as separators
            splits=line.split(' ')
            s=splits[0]

            if strIsInt(s):
                d['value']=int(s)
            elif strIsFloat(s):
                d['value']=float(s)
            elif strIsBool(s):
                d['value']=bool(s)
            else:
                d['value']=s
            iNext=1
            #import pdb  ; pdb.set_trace();

        # Extracting label (TODO, for now only second split)
        bOK=False
        while (not bOK) and iNext<len(splits):
            # Nasty handling of !XXX: comments
            if splits[iNext][0]=='!' and splits[iNext][-1]==':': 
                iNext=iNext+2
                continue
            # Nasty handling of the fact that sometimes old values are repeated before the label
            if strIsFloat(splits[iNext]):
                iNext=iNext+1
                continue
            else:
                bOK=True
        if bOK:
            d['label']= splits[iNext].strip()
            iNext = iNext+1
        else:
            #print('[WARN] Line {}: No label found -> comment assumed'.format(i+1))
            d['isComment']=True
            d['value']=line_raw
            iNext = len(splits)+1
        
        # Recombining description
        if len(splits)>=iNext+1:
            d['descr']=' '.join(splits[iNext:])
    except WrongFormatError as e:
        raise WrongFormatError('Line {}: '.format(i+1)+e.args[0])
    except Exception as e:
        raise Exception('Line {}: '.format(i+1)+e.args[0])

    return d

def parseFASTOutList(lines,iStart):
    OutList=[]
    i = iStart
    MAX=200
    while i<len(lines) and lines[i].upper().find('END')!=0:
        OutList.append(lines[i]) #TODO better parsing
        #print('OutList',lines[i])
        i += 1
        if i-iStart>MAX :
            raise Exception('More that 200 lines found in outlist')
        if i>=len(lines):
            print('[WARN] End of file reached while reading Outlist')
    i=min(i+1,len(lines))
    return OutList,i



def parseFASTNumTable(lines,n,iStart,nHeaders=2):
    Tab = None
    ColNames = None
    Units = None

    if len(lines)!=n+nHeaders:
        raise Exception('Not enough lines in table: {} lines instead of {}'.format(len(lines)-nHeaders,n))

    if nHeaders<1:
        raise NotImplementedError('Reading FAST tables with no headers not implemented yet')

    try:
        if nHeaders>=1:
            # Extract column names
            i = 0
            sTmp = cleanLine(lines[i])
            sTmp = cleanAfterChar(sTmp,'[')
            if sTmp.startswith('!'):
                sTmp=sTmp[1:].strip()
            ColNames=sTmp.split()
        if nHeaders>=2:
            # Extract units
            i = 1
            sTmp = cleanLine(lines[i])
            if sTmp.startswith('!'):
                sTmp=sTmp[1:].strip()
            Units=sTmp.split()
            # Forcing user to match number of units and column names
            if len(ColNames) != len(Units):
                raise Exception('Number of column names different from number of units in table')

        nCols=len(ColNames)

        Tab = np.zeros((n, len(ColNames))) 
        for i in range(nHeaders,n+nHeaders):
            l = lines[i].lower()
            v = l.split()
            if len(v) > nCols:
                print('[WARN] Line {}: number of data different from number of column names'.format(iStart+i+1))
            if len(v) < nCols:
                raise Exception('Number of data is lower than number of column names')
            # Accounting for TRUE FALSE and converting to float
            v = [s.replace('true','1').replace('false','0').replace('noprint','0') for s in v]
            v = [float(s) for s in v[0:nCols]]
            if len(v) < nCols:
                raise Exception('Number of data is lower than number of column names')
            Tab[i-nHeaders,:] = v
            
    except Exception as e:    
        raise Exception('Line {}: '.format(iStart+i+1)+e.args[0])
    return Tab, ColNames, Units


def parseFASTFilTable(lines,n,iStart):
    Tab = []
    try:
        i=0
        if len(lines)!=n:
            raise Exception('Not enough lines in table: {} lines instead of {}'.format(len(lines),n))
        for i in range(n):
            l = lines[i].split()
            #print(l[0].strip())
            Tab.append(l[0].strip())
            
    except Exception as e:    
        raise Exception('Line {}: '.format(iStart+i+1)+e.args[0])
    return Tab


if __name__ == "__main__":
    pass
    #B=FASTIn('Turbine.outb')



