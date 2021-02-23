""" 
Wrapper around wetb to read/write htc files.
TODO: rewrite of c2_def might not be obvious
"""
from .file import File

import numpy as np
import pandas as pd
import os

from .wetb.hawc2.htc_file import HTCFile
from .hawc2_st_file import HAWC2StFile

class HAWC2HTCFile(File):

    @staticmethod
    def defaultExtensions():
        return ['.htc']

    @staticmethod
    def formatName():
        return 'HAWC2 htc file'

    def _read(self):
        self.data = HTCFile(self.filename)
        self.data.contents # trigger read

    def _write(self):
        self.data.save(self.filename)

    def __repr__(self):
        s='<{} object> with attribute `data`\n'.format(type(self).__name__)
        return s

    def _toDataFrame(self):
        dfs ={}
        j=0

        simdir  = os.path.dirname(self.filename)

        # --- C2 def
        bodyKeys = [k for k in self.data.new_htc_structure.keys() if k.startswith('main_body')]
        for k in bodyKeys:
            bdy = self.data.new_htc_structure[k]
            nsec = bdy.c2_def.nsec
            val = np.array([bdy.c2_def[k].values[0:] for k in bdy.c2_def.keys() if k.startswith('sec')])
            val = val.reshape((-1,5))
            val = val[np.argsort(val[:,0]),:]
            val = val[:,[3,1,2,4]]
            name = bdy.name[0]
            dfs[name+'_c2'] = pd.DataFrame(data=val, columns=['z_[m]', 'x_[m]', 'y_[m]','twist_[deg]'])
            # potentially open st files..
            if "timoschenko_input" in bdy:
                tim = bdy.timoschenko_input
                H2_stfile = os.path.join(simdir, tim.filename[0])
                if not os.path.exists(H2_stfile):
                    print('[WARN] st file referenced in htc file was not found. St file: {}, htc file {}'.format(H2_stfile, self.filename))
                else:
                    dfs_st = HAWC2StFile(H2_stfile).toDataFrame()
                    if 'set' in tim.keys():
                        mset = tim.set[0]
                        iset = tim.set[1]
                        sSet = '{}_{}'.format(mset,iset)
                    else:
                        sSet = '1_1'
                    if sSet not in dfs_st:
                        raise Exception('Set {} not found in file {}'.format(sSet, H2_stfile))
                    else:
                        dfs[name+'_st'] = dfs_st[sSet]
        # --- Potentially ae and pc

        return dfs
