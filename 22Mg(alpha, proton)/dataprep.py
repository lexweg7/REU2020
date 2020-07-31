#!/usr/bin/env python
# coding: utf-8

# In[ ]:


'''
This function produces voxel-grid downsampled 128x128 xy projections for 22Mg data
'''

def downsample('my-file.h5','r'):
    
    #Read in h5 file in which each event is an individual key
    events = []
    for i in hf.keys():
        events.append(hf[i])
    
    #Dimensions of AT-TPC detector
    DETECTOR_LENGTH = 1000.0
    DETECTOR_RADIUS = 275.0

    #Number of divisions along each dimension in the detector
    x_disc = 128
    y_disc = 128
    z_disc = 128

    #z incriments
    z_inc = DETECTOR_LENGTH/z_disc
    
    
    #Make array for new data
    new_data = []
    for i in range(len(events)):
        new_events = np.zeros(128*128*128)
        num_pts = 0
        
        for point in events[i]:
            #Add up points in each bucket
            x_bucket = math.floor(((point[0]+DETECTOR_RADIUS)/(2*DETECTOR_RADIUS))*x_disc)
            y_bucket = math.floor(((point[1]+DETECTOR_RADIUS)/(2*DETECTOR_RADIUS))*y_disc)
            z_bucket = math.floor((point[2]/DETECTOR_LENGTH)*z_disc)

            #Determine ID of each bucket
            bucket_num = z_bucket*x_disc*y_disc + x_bucket + y_bucket*x_disc
            
            #Average z value within buckets
            avg_z = ((2*z_bucket+1)*z_inc)/2.0
            
            #Associate the average z value with each bucket
            new_events[bucket_num] = avg_z
        
            num_pts += 1
        
        #Reshape to be 128x128x128 matrix
        E = new_events.reshape((128,128,128))
        #Flatten to be xy only
        E_2d = np.sum(E,axis=0)
        #Add to new dataset
        new_data.append(E_2d)
        
    #New dataset to numpy array
    new_data=np.array(new_data)
    
return new_data

