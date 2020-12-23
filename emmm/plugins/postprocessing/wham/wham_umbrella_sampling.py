'''
Author: Zhenyu Wei
Date: 2020-12-23 13:44:22
LastEditTime: 2020-12-23 18:31:37
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /postprocessing/WHAM/codes/wham_umbrella_sampling.py
'''

import numpy as np
import os
from copy import copy
from . import WHAMBase

class WHAMUmbrellaSampling(WHAMBase):
    """ A Weighted Histogram Analysis Method analyser for umbrella sampling results.
    Example:
        ```python
            analyser = WHAMUmbrellaSampling()
            analyser.setDirPath('/Users/zhenyuwei/Simulation_Data/postprocessing/WHAM/data')
            analyser.setFileIdRangeFromStartToEnd(1, 199)
            analyser.setBinRangeFromStartToEnd(1, 25, 250)
            analyser.setConstantK(100)
            analyser.setTemperature(300)
            analyser.loadData()

            # analyser.iterativeSolver(tolerance=0.1)
            analyser.iterativeSolver(num_steps=10000)
        ```
    """
    def __init__(self):
        super(WHAMUmbrellaSampling, self).__init__()

    def _checkVariableRequirements(self):
        super(WHAMUmbrellaSampling, self)._checkVariableRequirements()
        try:
            self.k
        except:
            raise AttributeError('`k` should be defined by .setConstantK()')

    def setConstantK(self, k) -> None:
        """ Set the elastic constant for the harmonic bias potential
        Unit: Energy / Length^2
        """
        self.k = k

    def biasingFactor(self, coord, origin):
        """ Return a bias energy with given origin
        """
        return np.exp(- 0.5 * self.k * (coord-origin)**2 / self.kbt)

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
        self.origins = self.raw_data[:, 0]
        self.raw_data = self.raw_data[:, 1:]

    def _setBiasingFactor(self) -> None:
        self.bias_factor = np.ones([self.num_trajectories, self.num_bins])
        for (id, origin) in enumerate(self.origins):
            self.bias_factor[id, :] = np.array(list(map(self.biasingFactor, self.coord, np.ones_like(self.coord)*origin)))

    def _setComplete(self):
        super(WHAMUmbrellaSampling, self)._setComplete()
        self._setBiasingFactor()
        self.biasing_free_energy = - self.kbt * np.log(self.biasing_p)
        self.p = np.zeros([self.num_bins, 1]) # p is the probability distribution
        
    def iterativeSolver(self, num_steps=None, tolerance=None, max_steps=20000) -> None:
        """ Solver of the WHAM equations with iterative paradigm.
        Keywords:
            - num_steps: the number of iteration steps,
            - tolerance: the error tolerance of p
            - max_steps: used with `tolerance` to avoid too much iterative
        Note:
            - One and only one of `num_steps` and `tolerace` should be specified
        """
        if num_steps == None and tolerance == None:
            raise KeyError('One of `num_steps` or `tolerance` should be specified')
        elif num_steps != None and tolerance != None:
            raise KeyError('Only one keyword should be specified')
        else:
            self._setComplete()
            if num_steps != None:
                f_temp = copy(self.f)
                p_temp = copy(self.p)
                for _ in range(num_steps):
                    p_nominator = self.histograms.sum(0)
                    p_denominator = (self.bias_factor * self.num_samples[:, np.newaxis] * self.f[:, np.newaxis]).sum(0) + 0.000001
                    p_temp = p_nominator / p_denominator
                    self.p = p_temp
                    f_temp = (self.bias_factor * self.p).sum(1)
                    self.f = f_temp
            else:
                f_temp = copy(self.f)
                p_temp = copy(self.p) + 0.1
                total_step = 0
                while np.abs(p_temp - self.p).sum() > tolerance and total_step < max_steps:
                    total_step += 1
                    self.p = p_temp
                    p_nominator = self.histograms.sum(0)
                    p_denominator = (self.bias_factor * self.num_samples[:, np.newaxis] * f_temp[:, np.newaxis]).sum(0) + 0.000001
                    p_temp = p_nominator / p_denominator
                    self.f = f_temp
                    f_temp = (self.bias_factor * p_temp).sum(1)
                    
            self.p /= self.p.sum()
            self.free_energy = -self.kbt * np.log(self.p)
