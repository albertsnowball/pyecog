import numpy as np
class LFPData(object):
    """
    Class for one section of data before the light pulse.
    """
    def __init__(self, path,preprocess, window_len, fs = 512, label = None):
        self.fs = 512
        self.window_len = window_len*fs
        self.label = None
        self.filename = path
        
        self.alldata = np.load(path)
        
        if preprocess:
            # if more advanced can make a method for this
            self.alldata = self.alldata[::20,:]   
        self.lfpdata = self.alldata[:,1]
            
       
        if self.alldata.shape[1]>1:
            self.lightindexes = self._getLightIndexes(self.alldata[:,0])
            self.n_lightpulses = len(self.lightindexes)
        
            self.data_array = []
            self.label_array = []
            #print len(self.lightindexes)
            for lightindextuple in self.lightindexes:
                #print lightindextuple
                i = lightindextuple[0] - (self.window_len) # in case we 
                if i > 0:
                    data_section = self.lfpdata[i:lightindextuple[0]]
                    self.data_array.append(data_section)
                    self.label_array.append(label)

            self.data_array = np.array(self.data_array)
            if preprocess:
                self.data_array -= np.mean(self.data_array,axis = 0)
                self.data_array /= np.std(self.data_array,axis = 0)
            self.label_array = np.array(self.label_array)
            #plt.figure(figsize=(12,6))
            #plt.plot(self.data_array.T)
            #plt.title(self.filename)
            assert len(self.data_array.shape) ==2
        
    
        
    def _getLightIndexes(self,light):
        threshold =  ((max(light)-min(light))/2)+min(light)
        mask = np.where(light>threshold,1,0)
        mask1 = np.roll(mask[:],1)
        mask = abs(np.subtract(mask,mask1))
        lightindexes = np.where(mask==1)[0]
        if not lightindexes.shape[0]%2 == 0:
            raise AssertionError('The file has an odd number of light pulses,\
                                 cannot automatically detect the pulse times')
        light_index_list = []
        for i in range(0,lightindexes.shape[0],2):
            pulse = (lightindexes[i],lightindexes[i+1])
            light_index_list.append(pulse)
        return light_index_list