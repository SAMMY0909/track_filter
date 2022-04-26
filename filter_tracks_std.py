import h5py
import numpy as np
import os
import glob

results = glob.glob('std/*output.h5',recursive=True)
#print(results)

path_std = '../ttbar/std'

isExist_std = os.path.exists(path_std)

if not isExist_std:
    os.makedirs(path_std)
    print("The new std-directory has been created!")

loopctr=0
for f in results:
    print("Running cuts on: "+str(f)+"\n")
    with h5py.File(f, "r") as h5r:
        
        key_jets = list(h5r.keys())[0]
        key_tracks = list(h5r.keys())[1]
        #print (key_jets, h5r[key_jets].shape, h5r[key_jets].dtype)
        #print (key_tracks, h5r[key_tracks].shape, h5r[key_tracks].dtype)
        
        jets = np.copy(np.array(h5r['jets']))
        print("The shape of the jet dataset in the file is: ",jets.shape)
        tracks = np.copy(np.array(h5r['tracks_from_jet']))
        print("The shape of the track dataset in the file is: ",tracks.shape)
        
        
        tracks_d0 = np.array(h5r['tracks_from_jet']['d0'])
        tracks_z0 = np.array(h5r['tracks_from_jet']['z0SinTheta'])
        
        #print("The shape of the d0 array is: ",tracks_d0.shape)
        #print("The shape of the z0 array is: ",tracks_z0.shape)
        
        #print("The d0 removal arguments are: ",np.where(tracks_d0 > 1.0))
        #print("The z0 removal arguments are: ",np.where(tracks_z0 > 1.5))
        
        rem_list=np.where((tracks_d0 > 1.0) | (tracks_z0 > 1.5))
        
        if not rem_list:
            continue
        #print("The removal list is: ", rem_list)
        
        newfile = 'refined_std_tight' + os.path.basename(f)
        completeName = os.path.join(path_std, newfile)
        if os.path.exists(completeName):
            continue
        #dt stores the track key fields
        dt=[]
        for key,typ in h5r[key_tracks].dtype.fields.items():
            dt.append(key)
        
        with h5py.File(completeName, 'w') as fwrite:
            fwrite.create_dataset('jets', data=jets,compression='gzip',compression_opts=7)
            #print("The native track data types are: ",np.dtype(h5r[key_tracks]))
            
            #print("The track data shape for: "+str(key)+" is ",tracks[key].shape)
            
            for i,j in zip(rem_list[0],rem_list[1]):
                    #a=str(i)
                    #b=str(j)
                    
                    #print(f"Track index to be overwritten in {a} th jet is {b}.....")
                    tracks[i][j]=tracks[i][39]
            fwrite.create_dataset('tracks_from_jet',data=tracks,compression='gzip',compression_opts=7)
        loopctr+=1
        c=str(loopctr)
        print(f"End of file ops for file {completeName} in loop num {c} ==================\n")
