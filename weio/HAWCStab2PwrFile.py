from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from io import open
from builtins import map
from builtins import range
from builtins import chr
from builtins import str
from future import standard_library
standard_library.install_aliases()

from .File import File, WrongFormatError
import numpy as np
import pandas as pd


class HAWCStab2PwrFile(File):

    @staticmethod
    def defaultExtensions():
        return ['.pwr', '.txt']

    @staticmethod
    def formatName():
        return 'HAWCStab2 power file'

    def _read(self):
        try:
            self.data = np.loadtxt(self.filename, skiprows=1)
        except Exception as e:    
            raise WrongFormatError('Pwr File {}: '.format(self.filename)+e.args[0])

    #def _write(self):
        #self.data.to_csv(self.filename,sep=self.false,index=False)

    def _toDataFrame(self):
        cols=['V_[m/s]', 'P_[kW]', 'T_[kN]', 'Cp_[-]', 'Ct_[-]', 'Pitch_Q_[Nm]', 'Flap_M_[kNm]',
              'Edge_M_[kNm]', 'Pitch_[deg]', 'Speed_[rpm]', 'Tip_x_[m]', 'Tip_y_[m]', 'Tip_z_[m]',
              'J_rot_[kg*m^2]', 'J_DT_[kg*m^2]']
        return pd.DataFrame(data=self.data, columns=cols)

