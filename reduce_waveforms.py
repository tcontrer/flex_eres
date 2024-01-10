import numpy  as np
import tables as tb
import pandas as pd
import sys

from invisible_cities.io.dst_io import df_writer
import invisible_cities.database.load_db as db
import invisible_cities.io.mcinfo_io as mcio

def first_nonzero(arr, axis=0, invalid_val=-1):
    # Function to find the first nonzero entry
    # in a given array, returning invalid_val if none
    mask = arr!=0
    return np.where(mask.any(axis=axis), mask.argmax(axis=axis), invalid_val)

def GetMaxR(particles):
    # Get r_max position based on true particles position
    return np.sqrt(particles.initial_x**2 + particles.initial_y**2).max()

def VectorizePerEvent(sipm_event, pmt_event, event_id, database):
    sipm_charge = np.sum(sipm_event, axis=1)
    pmt_charge = np.sum(pmt_event, axis=1) 
    nsipms = np.shape(sipm_charge)[0]
    npmts = np.shape(pmt_charge)[0]
    sipm_charge = sipm_charge.ravel()
    pmt_charge = pmt_charge.ravel()
    sens = 1000
    # Make sensor and event id numbers, SiPMs start at 1000
    ids = np.arange(sens, sens+nsipms)
    pmt_ids = np.arange(0, npmts)
    #print('Num sipms', nsipms)
    #print('database num sensors', len(database.SensorID.to_numpy()))
    #print('ids', database.SensorID.to_numpy())
    sipm_ids = database.SensorID.to_numpy() >= sens

    # Get sensor positions from the database based on sensor id
    xs = database[sipm_ids].X.values
    ys = database[sipm_ids].Y.values
    #print('len x', len(xs))
    
    # Get time (z pos) of event based on sensor time bins
    zs = np.apply_along_axis(first_nonzero, axis=1, arr=sipm_event).ravel() - 100

    # Repeat event ids for number of sensors
    event_ids = [event_id]
    pmt_events = np.repeat(event_ids, npmts)
    event_ids = np.repeat(event_ids, nsipms)

    # Remove sensors with zero charge in an event
    nonzero_entries = np.where(sipm_charge>0)
    #print('nonzero sipms', len(sipm_charge>0))
    ids = np.array(ids[nonzero_entries])
    sipm_charge = np.array(sipm_charge[nonzero_entries])
    xs = np.array(xs[nonzero_entries])
    ys = np.array(ys[nonzero_entries])
    zs = np.array(zs[nonzero_entries])
    event_ids = np.array(event_ids[nonzero_entries])
    
    return event_ids, sipm_charge, xs, ys, zs, ids, pmt_events, pmt_charge, pmt_ids
    
def ReduceWaveforms(h5file, outname, dbname, fnum, nevents=100):
    event_start = fnum * nevents
    h5 = tb.open_file(h5file)
    database = db.DataSiPM(dbname)
    sipm_events = h5.root.sipmrd
    pmt_events = h5.root.pmtrd
    
    particles = mcio.load_mcparticles_df(h5file).reset_index()
    rs = particles.groupby('event_id').apply(lambda grp: np.sqrt(grp.initial_x**2 + grp.initial_y**2).max())

    event_ids, sipm_charge, xs, ys, zs, ids, pmt_eids, pmt_charge, pmt_ids = np.array([]), np.array([]), np.array([]), np.array([]), np.array([]), np.array([]), np.array([]), np.array([]), np.array([])
    nevents = len(sipm_events)
    for event in range(0,nevents):
        print('Events: ',nevents)
        print('len of data',len(sipm_events))
        sipm_data = sipm_events[event]
        pmt_data = pmt_events[event]
        events, s_charge, x, y, z, i, pmt_event, pmt_c, pmt_id = VectorizePerEvent(sipm_data, pmt_data, event, database)
        
        events = events + event_start
        event_ids = np.concatenate((event_ids,events))
        sipm_charge = np.concatenate((sipm_charge,s_charge))
        xs = np.concatenate((xs,x))
        ys = np.concatenate((ys,y))
        zs = np.concatenate((zs,z))
        ids = np.concatenate((ids,i))
        pmt_eids = pmt_eids + event_start
        pmt_eids = np.concatenate((pmt_eids,pmt_event))
        pmt_charge = np.concatenate((pmt_charge,pmt_c))
        pmt_ids = np.concatenate((pmt_ids,pmt_id))
        
    sipmtable = {'event_id': event_ids,
         'charge': sipm_charge,
          'X':xs,
          'Y':ys,
          'Z':zs,
          'sensor_id': ids}
    sipmtable_df = pd.DataFrame(sipmtable)

    pmttable = {'event_id': pmt_eids,
                'charge': pmt_charge,
              'sensor_id': pmt_ids}
    pmttable_df = pd.DataFrame(pmttable)
    
    rtable = {'r_max':rs, 'event_id':particles.event_id.unique()}
    rtable_df = pd.DataFrame(rtable)

    print(f'Out {outname}')
    h5out = tb.open_file(outname, 'w')

    df_writer(h5out, sipmtable_df, 'SiPM',  'Waveforms')
    df_writer(h5out, pmttable_df, 'PMT', 'Waveforms')
    df_writer(h5out, rtable_df, 'particles', 'r_max')

    h5out.close()

    return

if __name__ == '__main__':

    h5file = sys.argv[1]
    outname = sys.argv[2]
    dbname = sys.argv[3]
    fnum = int(sys.argv[4])
    if len(sys.argv) > 5:
        events = int(sys.argv[5])
        ReduceWaveforms(h5file, outname, dbname, fnum, events)
    else:
        ReduceWaveforms(h5file, outname, dbname, fnum)
