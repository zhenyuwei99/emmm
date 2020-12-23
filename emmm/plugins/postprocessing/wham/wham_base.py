'''
Author: Zhenyu Wei
Date: 2020-12-23 11:08:28
LastEditTime: 2020-12-23 17:38:32
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /postprocessing/WHAM/codes/wham.py
'''

import numpy as np
import os

class WHAMBase(object):
    def __init__(self) -> None:
        """Set default values
        """
        self.file_pattern = 'cv_%d.txt'
        self.energy_unit = 'kj/mol'
        self.length_unit = 'angstrom'

    def __str__(self):
        return '<Weighted Histograms Analysis Method analyser for files in %s>' %(self.dir_path)

    __repr__ = __str__

    def _checkVariableRequirements(self) -> None:
        """ Check the existance of required variables for the solvation
        """
        try:
            self.dir_path
        except:
            raise AttributeError('`dirPath` should be defined by .setDirPath()')
        try:
            self.file_id_range
        except:
            raise AttributeError('`file_id_range` should be defined by .setFileIdRange() or ' +
                '.setFileIdRangeFromStartToEnd()')
        try:
            self.bin_range
        except:
            raise AttributeError('`bin_range` should be defined by .setBinRange() or ' + 
                '.setBinRangeFromStartToEnd()')
        
        try:
            self.T
        except:
            raise AttributeError('Temperature `T` should be defined by .setTemperature()')

    def setDirPath(self, dir_path) -> None:
        self.dir_path = dir_path

    def setFileIdRangeFromList(self, file_id_range) -> None:
        """ Set `file_id_range` from a list and set the number of trajectories (M)
        """
        self.file_id_range = file_id_range
        self.num_trajectories = len(self.file_id_range) # The value of M

    def setFileIdRangeFromStartToEnd(self, file_id_start, file_id_end) -> None:
        """ Set `file_id_range` from the start and end id
        Meanwhile set the number of trajectories (M)
        Note this method can only be called when the file id is continous
        """
        self.file_id_range = list(range(file_id_start, file_id_end+1))
        self.num_trajectories = len(self.file_id_range) # The value of M

    def setBinRangeFromList(self, bin_range) -> None:
        """ Set `bin_range` from a list 
        Meanwhile set the number of bins (B) and `coord` for the center of each bins
        """
        self.bin_range = bin_range
        self.coord = self.bin_range[1:] - self.bin_range[:-1]
        self.num_bins = len(self.coord) # The value of B

    def setBinRangeFromStartToEnd(self, bin_start, bin_end, num_bins) -> None:
        """ Set `bin_range` using np.linspace()
        Meanwhile set the number of bins (B) and `coord` for the center of each bins
        This method will set a equal-seperated `bin_range`
        """
        self.bin_range = np.linspace(bin_start, bin_end, num_bins+1)
        self.coord = (self.bin_range[1:] + self.bin_range[:-1]) / 2
        self.num_bins = len(self.coord) # The value of B
    
    def setEnergyUnit(self, energy_unit) -> None:
        """ Set `enegy_unit`
        Supported unit:
        - kj/mol
        - kcal/mol
        """
        energy_unit_list = ['kj/mol', 'kcal/mol']
        if energy_unit in energy_unit_list:
            self.energy_unit = energy_unit
        else:
            raise KeyError('Unit: %s is not supported! Only %s are supported'
                %(energy_unit, energy_unit_list))
    
    def setLengthUnit(self, length_unit):
        """ Set `length_unit`
        Supported unit:
        - angstrom / an
        - nanometer / nm
        """
        length_unit_list = ['angstrom', 'an', 'nanometer', 'nm']
        if length_unit in length_unit_list:
            self.length_unit = length_unit
        else:
            raise KeyError('Unit: %s is not supported! Only %s are supported'
                %(length_unit, length_unit_list))

    def setTemperature(self, temp):
        """ Set the temperature `T` and correspond `kbt` respect to `energy_unit`
        """
        self.T = temp
        if self.energy_unit == 'kj/mol':
            self.kbt = 0.008314 * self.T
        elif self.energy_unit == 'kcal/mol':
            self.kbt = 0.001987 * self.T

    def setFilePattern(self, file_pattern):
        """ Set the `file_pattern` for files in `dir_path`
        E.g: The file pattern for files 'cv_1.txt', 'cv_2.txt' is 'cv_%d.txt'
        """
        self.file_pattern = file_pattern

    def loadData(self) -> None:
        """ Loading data from files with pattern 'file_pattern' in `dir_path`
        Set a attribute `raw_data` containing all information
        """
        self._checkVariableRequirements()
        self.raw_data = []
        for file_id in self.file_id_range:
            file_name = os.path.join(self.dir_path, self.file_pattern %(file_id))
            self.raw_data.append(self._loadFile(file_name))
        self.raw_data = np.array(self.raw_data)

    def _parseLine(self, line):
        data = line.split()
        for (i, value) in enumerate(data):
            try:
                value = float(value)
            except:
                data[i] = value
            else:
                data[i] = value
        return data

    def _loadFile(self, file_name) -> None:
        data = []
        with open(file_name, 'r') as io:
            for line in io:
                data.append(self._parseLine(line))
        try:
            return np.array(data)
        except:
            return data
    
    def _setHistograms(self) -> None:
        """ Set h_i(xi_j)
        Set a MxB array
        """
        self.histograms = []
        self.biasing_p = []
        for data in self.raw_data:
            hist = np.histogram(data, self.bin_range)[0]
            self.histograms.append(hist)
            self.biasing_p.append(hist/hist.sum())
        self.histograms = np.array(self.histograms)
        self.biasing_p = np.array(self.biasing_p)
    
    def _setNumSamples(self) -> None:
        """ Set Ni for each trajectoryies.
        Set a Mx1 vector
        """
        self.num_samples = []
        for histogram in self.histograms:
            self.num_samples.append(histogram.sum())
        self.num_samples = np.array(self.num_samples)
    
    def _setInitNormalFactor(self) -> None:
        """ Set the initial value for f_i
        Set a Mx1 vector
        """
        self.f = np.ones_like(self.num_samples)

    def _setComplete(self):
        self._checkVariableRequirements()
        self._setHistograms()
        self._setNumSamples()
        self._setInitNormalFactor()
        self.biasing_free_energy = - self.kbt * np.log(self.biasing_p)
        self.p = np.zeros([self.num_bins, 1]) # p is the probability distribution
