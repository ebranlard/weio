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
import os
import re

from .File import File, WrongFormatError
import numpy as np
import pandas as pd


class HAWCStab2IndFile(File):

    @staticmethod
    def defaultExtensions():
        return ['.ind', '.txt']

    @staticmethod
    def formatName():
        return 'HAWCStab2 induction file'

    def _read(self):
        try:
            self.data = np.loadtxt(self.filename, skiprows=1)
            self.type = {38: '', 14: 'fext', 18: 'defl'}[self.data.shape[1]]  # type of ind file
        except Exception as e:    
            raise WrongFormatError('Ind File {}: '.format(self.filename)+e.args[0])

    def _toDataFrame(self):
        if self.type == '':
            cols=['s_[m]', 'A_[-]', 'AP_[-]', 'PHI0_[rad]', 'ALPHA0_[rad]', 'U0_[m/s]', 'FX0_[N/m]', 'FY0_[N/m]',
                  'M0_[Nm/m]', 'UX0_[m]', 'UY0_[m]', 'UZ0_[m]', 'Twist[rad]', 'X_AC0_[m]', 'Y_AC0_[m]', 'Z_AC0_[m]',
                  'CL0_[-]', 'CD0_[-]', 'CM0_[-]', 'CLp0[1/rad]', 'CDp0[1/rad]', 'CMp0[1/rad]', 'F0_[-]', "F'[1/rad]",
                  'CL_FS0_[-]', "CLFS'[1/rad]", 'V_a_[m/s]', 'V_t_[m/s]', 'Tors._[rad]', 'vx_[m/s]', 'vy_[m/s]',
                  'chord_[m]', 'CT_[-]', 'CP_[-]', 'angle_[rad]', 'v_1_[-]', 'v_2_[-]', 'v_3_[-]']
        elif self.type == 'fext':
            cols=['s_[m]', 'Node_[-]', 'Fx_e_[N]', 'Fy_e_[N]', 'Fz_e_[N]', 'Mx_e_[Nm]', 'My_e_[Nm]', 'Mz_e_[Nm]', 'Fx_r_[N]',
                  'Fy_r_[N]', 'Fz_r_[N]', 'Mx_r_[Nm]', 'My_r_[Nm]', 'Mz_r_[Nm]']
        elif self.type == 'defl':
            cols=['s_[m]', 'Element_no_[-]', 'pos_xR_[m]', 'pos_yR_[m]', 'pos_zR_[m]', 'Elem_angle_[rad]', 'Elem_v_1_[-]', 'Elem_v_2_[-]',
                  'Elem_v_3_[-]', 'Node_1_angle_[rad]', 'Node_1_v_1_[-]', 'Node_1_v_2_[-]', 'Node_1_v_3_[-]', 'Node_2_angle_[rad]',
                   'Node_2_v_1_[-]', 'Node_2_v_2_[-]', 'Node_2_v_3_[-]', 'Elongation_[m]']
        # isolate the ind files that match this one
        dirname = os.path.dirname(self.filename)
        basename = '_'.join(os.path.basename(self.filename).split('_')[:-1])
        regex = basename + '_u\d+.ind'
        files = [f for f in os.listdir(dirname) if re.match(regex, f)]
        # find order of wind speeds
        wsps = [float(f.split('_')[-1].rstrip('.ind').lstrip('u'))/1000 for f in files]
        idcs = np.argsort(wsps)
        # load the data
        dfs = {}
        for i_f in idcs:
            wsp_filename = os.path.join(dirname, files[i_f])
            key = '{:.3f}'.format(wsps[i_f])
            dfs[key] = pd.read_csv(wsp_filename, delim_whitespace=True, names=cols, skiprows=1)
        return dfs

