import numpy as np
import sys

from invisible_cities.io import pmaps_io
from invisible_cities.io.dst_io import load_dsts

mcs = {'s1.3mmp3.5mm':
        {'size':1.3, 'pitch':3.5, 'teflon':False, 'nsipms':61053,  'run':True},
    's1.3mmp2.4mm':
        {'size':1.3, 'pitch':2.4, 'teflon':False, 'nsipms':129889, 'run':True},
    's3mmp5.5mm':
        {'size':3,   'pitch':5.5, 'teflon':False, 'nsipms':24748,  'run':True},
    's6mmp11mm':
        {'size':6,   'pitch':11,  'teflon':False, 'nsipms':6181,   'run':True},
    's6mmp7.8mm':
        {'size':6,   'pitch':7.8, 'teflon':False, 'nsipms':12304,   'run':True}}

def GetWidth(pmap_file, kdst_file, outfile):

    ### Load kdst files
    dst = load_dsts([kdst_file], 'DST', 'Events')
    print(kdst_file)
    print(dst)
    ### Select events with 1 S1 and 1 S2
    mask_s1 = dst.nS1==1
    mask_s2 = np.zeros_like(mask_s1)
    mask_s2[mask_s1] = dst[mask_s1].nS2 == 1
    nevts_after      = dst[mask_s2].event.nunique()
    nevts_before     = dst[mask_s1].event.nunique()
    eff              = nevts_after / nevts_before
    print('S2 selection efficiency: ', eff*100, '%')

    # Get good events
    pmap_evt_ids = load_dsts([pmap_file], "Run", "events")
    good_events = np.intersect1d(pmap_evt_ids.evt_number.to_numpy(), dst[mask_s2].event.to_numpy())
    mask_evt = np.isin(dst.event.to_numpy(), good_events)
    mask_evt = mask_s2 & mask_evt

    # Get SiPM Widths from PMAPs
    pmaps = pmaps_io.load_pmaps(pmap_file)
    sipm_widths = []
    for evt in good_events:
        if pmaps[evt].s2s:
            if np.shape(pmaps[evt].s2s[0].sipms.all_waveforms)[1] != len(pmaps[evt].s2s[0].times):
                print('Not same size!')
            sipm_widths.append(len(pmaps[evt].s2s[0].times))

    # Add SiPM width to dst
    dst_widths = np.zeros_like(dst.S2w)
    dst_widths[mask_evt] = sipm_widths
    dst['S2w_sipm'] = dst_widths

    dst.to_hdf(outfile, key='df', mode='w')

    return

if __name__ == '__main__':

    start_dir = sys.argv[1]
    pmap_file = sys.argv[2]
    kdst_file = sys.argv[3]
    outfile = sys.argv[4]

    for mc in mcs:
        if mcs[mc]['run']:
            this_pmap_file = start_dir + mc +  pmap_file
            this_kdst_file = start_dir + mc + kdst_file
            this_outfile = start_dir + mc + outfile

            GetWidth(this_pmap_file, this_kdst_file, this_outfile)