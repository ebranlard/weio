from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from io import open
from .File import File, isBinary, WrongFormatError, BrokenFormatError
import pandas as pd
import numpy as np
import re


class FASTLinFile(File):

    @staticmethod
    def defaultExtensions():
        return ['.lin']

    @staticmethod
    def formatName():
        return 'FAST linearization output'

    def _read(self, *args, **kwargs):
        self['header']=[]

        def extractVal(lines, key):
            for l in lines:
                if l.find(key)>=0:
                    return l.split(key)[1].split()[0]
            return None

        def readToMarker(fid, marker, nMax):
            lines=[]
            for i, line in enumerate(fid):
                if i>nMax:
                    raise BrokenFormatError('`{}` not found in file'.format(marker))
                if line.find(marker)>=0:
                    break
                lines.append(line.strip())
            return lines, line
        
        def readOP(fid, n):
            OP=[]
            Var = {'RotatingFrame': [], 'DerivativeOrder': [], 'Description': []}
            colNames=fid.readline().strip()
            dummy=   fid.readline().strip()
            bHasDeriv= colNames.find('Derivative Order')>=0
            for i, line in enumerate(fid):
                sp=line.strip().split()
                OP.append(float(sp[1]))
                Var['RotatingFrame'].append(sp[2])
                if bHasDeriv:
                    Var['DerivativeOrder'].append(int(sp[3]))
                    Var['Description'].append(' '.join(sp[4:]).strip())
                else:
                    Var['DerivativeOrder'].append(-1)
                    Var['Description'].append(' '.join(sp[3:]).strip())
                if i>=n-1:
                    break
            return OP, Var

        def readMat(fid, n, m):
            return np.array([f.readline().strip().split() for i in np.arange(n)]).astype(np.float)

        # Reading 
        with open(self.filename, 'r', errors="surrogateescape") as f:
            # --- Reader header
            self['header'], lastLine=readToMarker(f, 'Jacobians included', 30)
            self['header'].append(lastLine)
            nx  = int(extractVal(self['header'],'Number of continuous states:'))
            nxd = int(extractVal(self['header'],'Number of discrete states:'  ))
            nz  = int(extractVal(self['header'],'Number of constraint states:'))
            nu  = int(extractVal(self['header'],'Number of inputs:'           ))
            ny  = int(extractVal(self['header'],'Number of outputs:'          ))
            bJac = extractVal(self['header'],'Jacobians included in this file?')
            try:
                self.Azimuth = float(extractVal(self['header'],'Azimuth:'))
            except:
                self.Azimuth = None
            try:
                self.RotSpeed = float(extractVal(self['header'],'Rotor Speed:')) # rad/s
            except:
                self.RotSpeed = None
            try:
                self.WindSpeed = float(extractVal(self['header'],'Wind Speed:'))
            except:
                self.WindSpeed = None


            KEYS=['Order of','A:','B:','C:','D:','ED M:']


            for i, line in enumerate(f):
                line = line.strip()
                KeyFound=any([line.find(k)>=0 for k in KEYS])
                if KeyFound:
                    if line.find('Order of continuous states:')>=0:
                        self['x'], self['x_info'] = readOP(f, nx)
                    elif line.find('Order of continuous state derivatives:')>=0:
                        self['xdot'], self['xdot_info'] = readOP(f, nx)
                    elif line.find('Order of inputs')>=0:
                        self['u'], self['u_info'] = readOP(f, nu)
                    elif line.find('Order of outputs')>=0:
                        self['y'], self['y_info'] = readOP(f, ny)
                    elif line.find('A:')>=0:
                        self['A'] = readMat(f, nx, nx)
                    elif line.find('B:')>=0:
                        self['B'] = readMat(f, nx, nu)
                    elif line.find('C:')>=0:
                        self['C'] = readMat(f, ny, nx)
                    elif line.find('D:')>=0:
                        self['D'] = readMat(f, ny, nu)
                    elif line.find('ED M:')>=0:
                        self['EDDOF'] = line[5:].split()
                        self['M']     = readMat(f, 24, 24)

    def toString(self):
        s=''
        return s

    def _write(self):
        with open(self.filename,'w') as f:
            f.write(self.toString())

    def short_descr(self,slist):
        def shortname(s):
            s=s.strip()
            s = s.replace('(m/s)'   , '_[m/s]'  );
            s = s.replace('(kW)'    , '_[kW]'   );
            s = s.replace('(deg)'   , '_[deg]'  );
            s = s.replace('(N)'     , '_[N]'    );
            s = s.replace('(kN-m)'  , '_[kN-m]' );
            s = s.replace('(N-m)'  , '_[N-m]' );
            s = s.replace('(kN)'  , '_[kN]' );
            s = s.replace('(rpm)'   , '_[rpm]'  );
            s = s.replace('(m/s^2)' , '_[m/s^2]');
            s = s.replace('(m)'     , '_[m]'    );
            s = s.replace(', m/s','_[m/s]');
            s = s.replace(', rad/s','_[rad/s]');
            s = s.replace(', rad','_[rad]');
            s = s.replace(', m','_[m]');
            s = s.replace(', -','_[-]');
            s = s.replace(', Nm','_[Nm]');
            s= re.sub(r'\([^)]*\)','', s)
            s = s.replace('ED ','');
            s = s.replace('IfW ','');
            s = s.replace('Extended input: ','')
            s = s.replace('1st tower ','qt1');
            s = s.replace('First time derivative of '     ,'d_');
            s = s.replace('Variable speed generator DOF ','psi_gen');
            s = s.replace('fore-aft bending mode DOF '    ,'FA'     );
            s = s.replace('side-to-side bending mode DOF','SS'     );
            s = s.replace('bending-mode DOF of blade '    ,''     );
            s = s.replace(' rotational-flexibility DOF, rad','-ROT'   );
            s = s.replace('rotational displacement in ','rot'   );
            s = s.replace('Drivetrain','DT'   );
            s = s.replace('translational displacement in ','trans'   );
            s = s.replace('finite element node ','N'   );
            s = s.replace('cosine','cos'   );
            s = s.replace('sine','sin'   );
            s = s.replace('collective','coll.');
            s = s.replace('Blade','Bld');
            s = s.replace('rotZ','TORS-R');
            s = s.replace('transX','FLAP-D');
            s = s.replace('transY','EDGE-D');
            s = s.replace('rotX','EDGE-R');
            s = s.replace('rotY','FLAP-R');
            s = s.replace('flapwise','FLAP');
            s = s.replace('edgewise','EDGE');
            s = s.replace('vertical power-law shear exponent','alpha')
            s = s.replace('horizontal wind speed ','WS')
            s = s.replace('propagation direction','WD')
            s = s.replace(' pitch command','pitch')
            s = s.replace('Bld ','Bld')
            s = s.replace('Generator torque','Qgen')
            s = s.replace('coll. blade-pitch command','PitchColl')
            s = s.replace(',','');
            s = s.replace(' ','');
            s=s.strip()
            return s
        return [shortname(s) for s in slist]

    def xdescr(self):
        return self.short_descr(self['x_info']['Description'])
    def ydescr(self):
        return self.short_descr(self['y_info']['Description'])
    def udescr(self):
        return self.short_descr(self['u_info']['Description'])

    def _toDataFrame(self):
        dfs={}
        xdescr_short=['{:17.17s}'.format(d).strip() for d in self.xdescr()]
        udescr_short=['{:17.17s}'.format(d).strip() for d in self.udescr()]
        ydescr_short=['{:17.17s}'.format(d).strip() for d in self.ydescr()]
        dfs['A'] = pd.DataFrame(data = self['A'], index=xdescr_short, columns=xdescr_short)
        dfs['B'] = pd.DataFrame(data = self['B'], index=xdescr_short, columns=udescr_short)
        dfs['C'] = pd.DataFrame(data = self['C'], index=ydescr_short, columns=xdescr_short)
        dfs['D'] = pd.DataFrame(data = self['D'], index=ydescr_short, columns=udescr_short)
        dfs['x'] = pd.DataFrame(data = np.asarray(self['x']).reshape((1,-1)), columns=xdescr_short)
        dfs['u'] = pd.DataFrame(data = np.asarray(self['u']).reshape((1,-1)), columns=udescr_short)
        dfs['y'] = pd.DataFrame(data = np.asarray(self['y']).reshape((1,-1)), columns=ydescr_short)
        try:
            dfs['M'] = pd.DataFrame(data = self['M'], index=self['EDDOF'], columns=self['EDDOF'])
        except:
            pass
        return dfs


