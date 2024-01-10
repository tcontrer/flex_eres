import json

#configs = ['s1.3mmp15mm', 's1.3mmp7mm', 's1.3mmp1.3mm', 
#            's3mmp15mm', 's3mmp7mm', 's3mmp3mm',
#            's6mmp15mm', 's6mmp6mm',
#           's1.3mmp15mm_teflon', 's1.3mmp7mm_teflon',
#            's3mmp15mm_teflon', 's3mmp7mm_teflon',
#            's6mmp15mm_teflon']

configs = ['s1.3mmp15mm', 's1.3mmp7mm', 's1.3mmp1.3mm',
           's1.3mmp5.82mm', 's1.3mmp4.11mm', 's1.3mmp2.9mm',
           's1.3mmp2.37mm', 's1.3mmp1.84mm',
           's3mmp15mm', 's3mmp7mm', 's3mmp3mm',
           's3mmp9.49mm', 's3mmp6.71mm', 's3mmp5.48mm',
           's3mmp4.74mm', 's3mmp4.24mm',
           's6mmp15mm', 's6mmp6mm',
           's6mmp18.97mm', 's6mmp13.42mm', 's6mmp10.95mm',
           's6mmp9.49mm', 's6mmp8.49mm'] 
mcs = {'s1.3mmp3.5mm':
        {'size':1.3, 'pitch':3.5,  'teflon':False, 'nsipms':61053,   'run':True},
    's1.3mmp2.4mm':
        {'size':1.3, 'pitch':2.4,    'teflon':False, 'nsipms':129889,  'run':True},
    's3mmp5.5mm':
        {'size':3, 'pitch':5.5,  'teflon':False, 'nsipms':24748, 'run':True}}
configs = mcs.keys()

data_dir = 'data_eres_0vbb_rcut300.0_sthresh0_zcut1200.0_test/'
data = {}
for config in configs:
    print(config)
    d = json.load(open(data_dir+config+'.txt'))
    data[config] = d
print(data)
json.dump(data, open(data_dir+'all_data.txt', 'w'))
