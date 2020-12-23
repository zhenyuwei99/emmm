'''
Author: your name
Date: 2020-12-23 17:56:10
LastEditTime: 2020-12-23 18:25:30
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /emmm/test/test_wham.py
'''
import sys
import matplotlib.pyplot as plt
sys.path.append('/Users/zhenyuwei/Nutstore Files/emmm/')
from emmm.plugins.postprocessing.wham.wham_umbrella_sampling import WHAMUmbrellaSampling

analyser = WHAMUmbrellaSampling()
analyser.setDirPath('/Users/zhenyuwei/Simulation_Data/postprocessing/WHAM/data')
analyser.setFileIdRangeFromStartToEnd(1, 199)
analyser.setBinRangeFromStartToEnd(1, 25, 250)
analyser.setConstantK(100)
analyser.setTemperature(300)
analyser.loadData()

# analyser.iterativeSolver(tolerance=0.1)
analyser.iterativeSolver(num_steps=10000)

fig = plt.figure(figsize=[10, 10])
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()
for id in range(analyser.num_trajectories):
    ax1.plot(analyser.coord, analyser.biasing_free_energy[id, :], '-.', lw=0.5)
ax2.plot(analyser.coord, analyser.free_energy)
plt.show()