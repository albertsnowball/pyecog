import numpy as np
import matplotlib.pyplot as plt

# Basic script to run network state classfication

from loadSeizureData  import LoadSeizureData
from classifierTester import ClassifierTester
from relabeling_functions import relabel, reorder
from visualisation import plots

from extractors.basicFeatures    import BasicFeatures
from extractors.freqfeatures     import FreqFeatures
from extractors.waveletfeatures import WaveletFeatures

from classifiers.randomForestClassifier import RandomForest
from classifiers.svm import SupportVecClf
from classifiers.neighbors import KNeighbors

dirpath = '/Users/Jonathan/Documents/PhD /Seizure_related/Network_states/VMData/Classified'
dataobj = LoadSeizureData(dirpath)
dataobj.load_data()
dataobj = relabel(dataobj)
dataobj = reorder(dataobj)
basicStatsExtractor = BasicFeatures()
wavelets = WaveletFeatures()
fourier = FreqFeatures()
#dataobj.extract_feature_array([basicStatsExtractor])
dataobj.extract_feature_array([wavelets, basicStatsExtractor, fourier])

print dataobj.features.shape
rf = RandomForest(no_trees = 100)
classtester = ClassifierTester(dataobj.features,np.ravel(dataobj.label_colarray), training_test_split = 80)
(score, predictedlabelsprobs, reallabels) = classtester.test_classifier(rf)
print 'training a random forest classifier!'
print score, 'percent correct!'

print 'training a support vector classifier'
svcclf = SupportVecClf(k_type = 'rbf')
(score, predictedlabelsprobs, reallabels) = classtester.test_classifier(svcclf)
print score, 'percent correct!'

print 'training a K nearest neighbors classifier'
knn_clf = KNeighbors(15)
(score, predictedlabelsprobs, reallabels) = classtester.test_classifier(knn_clf)
print score, 'percent correct!'

plots.radviz(dataobj)
#plots.scatter_matrix(dataobj)
#raw_input()
#plt.close('all')
#for row_index in range(predictedlabelsprobs.shape[0]):
 #   print predictedlabelsprobs[row_index,:], ' actual label was :', reallabels[row_index]