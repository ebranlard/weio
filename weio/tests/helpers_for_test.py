import glob
import os

MyDir=os.path.join(os.path.dirname(__file__),'example_files')

__all__  = ['MyDir', 'reading_test']

def reading_test(Pattern, Reader, DEBUG=True):
    nError=0
    if DEBUG:
        print('')
    for f in glob.glob(os.path.join(MyDir,Pattern)):
        if os.path.splitext(f)[-1] in ['.py','.pyc'] or f.find('_TMP')>0:
            continue
        try:
            obj = Reader(f)
            s=type(obj).__name__.replace('file','')[:20]
            if DEBUG:
                print('[ OK ] {:30s}\t{:20s}'.format(os.path.basename(f)[:30],s))
        except:
            nError += 1
            if DEBUG:
                print('[FAIL] {:30s}\tException occurred'.format(os.path.basename(f)[:30]))
            raise 
    if nError>0:
        raise Exception('Some tests failed')
