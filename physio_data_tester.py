# -*- coding: utf-8 -*-
__author__ = "Batuhan Tomekce and Burak Alp Kaya"
__email__ = "tbatuhan@ethz.ch, bukaya@ethz.ch"

"""
    Program to test given data. Looks for variations in the signal properties and reports them back to the user.
    
    USAGE: tune file_name line to look for correct data locations, change default values for signal parameters
"""

# pyEDFlib is a python library to read/write EDF+/BDF+ files based on EDFlib.
import pyedflib
import numpy as np
import os

def test_data(subjects, runs, PATH):
    
    '''
    Keyword arguments:
    subject -- array of subject numbers in range [1, .. , 109] (integer)
    runs    -- array of the numbers of the runs in range [1, .. , 14] (integer)
    PATH    -- string of PATH to directory containing .edf data
               ex: /home/<username>/<project_directory>/<data>/
               to this, SXXXRYY.edf will be added to form the full path
    
    Output: Prints variations in data
        
    Return: PATHS -- PATHs to irregular data in a String List
    '''
    PATHS = []
    for subject in subjects:
        for run in runs:
            
            if(subject < 10):
                subject_str = '00'+str(subject)
            elif(subject < 100):
                subject_str = '0'+str(subject)
            else:
                subject_str = str(subject)
                
            if(run < 10):
                run_str = '0'+str(run)
            else:
                run_str = str(run)
    
            # Create file name variable to access edf file
            file_name = os.path.join(PATH +'S' + subject_str,'S'+ subject_str + 'R' + run_str + '.edf')
                
            # Read file
            f = pyedflib.EdfReader(file_name)
                
            # Signal Parameters - measurement frequency
            freq = f.getSampleFrequencies()
            for i in np.arange(1, len(freq)):
                if (freq[i-1] != freq[i]):
                    print('S'+ subject_str + 'R' + run_str + " contains channels with differing frequencies!")
            
            # Number of eeg channels = number of signals in file
            n = f.signals_in_file
    
            # Get Label information
            annotations = f.readAnnotations()
            labels = annotations[2]
            
            # Define expected values
            frequency = 160
            eeg_channels = 64
            events = 30
            
            # Check irregularities
            if (frequency != freq[0]):
                print('S'+ subject_str + 'R' + run_str + "  Frequency changed: " + str(frequency) + " to: " + str(freq[0]))
                #frequency = freq[0]
                if file_name not in PATHS:
                    PATHS.append(file_name)
            
            if (eeg_channels != n):
                print('S'+ subject_str + 'R' + run_str + "  Number of signals changed: " + str(eeg_channels) + " to: " + str(n))
                #eeg_channels = n
                if file_name not in PATHS:
                    PATHS.append(file_name)
                
            if (events != len(labels)):
                print('S'+ subject_str + 'R' + run_str + "  Number of Events per Run changed: " + str(events) + " to: " + str(len(labels)))
                #events = len(labels)
                if file_name not in PATHS:
                    PATHS.append(file_name)
        
            f.close()
    return PATHS


""" example usage:
p = test_data(np.arange(1,110), np.arange(3,15), "<PATH>")
""" 