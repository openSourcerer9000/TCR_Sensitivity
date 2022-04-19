import pandas as pd, numpy as np

class ftbend:
    def _TCplusR(L,S,N,S0,I):
        return 128*( (L/np.sqrt(S))**.57 )*( N**.8 )/      \
        ( (S0**.11)*(10**I) )
    def _TCR(L,S,N,S0,I):
        tc_r = ftbend._TCplusR(L,S,N,S0,I)
        TC = tc_r*.38*np.log10(S0)
        R = tc_r - TC
        return (TC,R)
    def _TCRfromSubbasin(sub):
        '''sub is a mappable to translate names to variables for Ft Bend Cty EQ\n
        DAs_gdf.apply(hmsCalc.ftbend.TCRfromSubbasin,axis=1)'''
        len_units = sub['length_units']
        if len_units=='ft':
            mi=5280
        elif len_units=='m':
            mi=1609.34
        else:
            assert False, f'ERROR: unhandled case length units as {len_units}'

        L,S,N,S0,I=sub[['longest_length','10_85_slope','n','basin_slope','imp']].map(float)

        L=L/mi
        assert L>2/5280, 'sanity check after ft to mi conversion'
        assert L<10000
        S,S0=S*mi,S0*mi
        I=I/100
        assert I<=1, 'sanity check percent to ratio impervious conversion'
        # assert I*100

        TC,R = ftbend._TCR(L,S,N,S0,I)
        return (TC,R)