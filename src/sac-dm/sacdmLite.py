# Standard python numerical analysis imports:
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, peak_prominences
import sys
import utilLite

# Calcula SAC-DM utilizando a funcao find_peaks do Python
def sac_dm(data, N):
	
	M = len(data)
	size = 1 + int(M/N)
	sacdm=[0.0] * size

	inicio = 0
	fim = N
	for k in range(size):
		peaks, _ = find_peaks(data[inicio:fim])
		v = np.array(peaks)
		sacdm[k] = 1.0*len(v)/N
		inicio = fim
		fim = fim + N
	
	return sacdm

# Calcula SAC-AM (amplitude media dos maximos) utilizando a funcao find_peaks do Python
def sac_am(data, N):
	
	M = len(data)
	size = 1 + int(M/N)
	sacdm=[0.0] * size

	inicio = 0
	fim = N
	for k in range(size):
		peaks, _ = find_peaks(data[inicio:fim])
		v = np.abs(data[peaks])
		s = sum(v)
		sacdm[k] = 1.0*s/N
		inicio = fim
		fim = fim + N

	return sacdm


def plotSAC_AM_DM():
	N = int(sys.argv[3])

	#Abrindo arquivos
	F0 = np.genfromtxt( "../../files/drone_signals/accel_80_F0.csv", delimiter=';', names=['x','y','z','s','t'])
	F6 = np.genfromtxt( "../../files/drone_signals/accel_80_F6_v1.csv", delimiter=';', names=['x','y','z','s','t'])
	F14 = np.genfromtxt( "../../files/drone_signals/accel_80_F14.csv", delimiter=';', names=['x','y','z','s','t'])
	F22 = np.genfromtxt( "../../files/drone_signals/accel_80_F22.csv", delimiter=';', names=['x','y','z','s','t'])

	#Extraindo eixos
	F0_x = F0['x'].reshape(-1)
	F0_y = F0['y'].reshape(-1)
	F0_z = F0['z'].reshape(-1)

	F6_x = F6['x'].reshape(-1)
	F6_y = F6['y'].reshape(-1)
	F6_z = F6['z'].reshape(-1)

	F14_x = F14['x'].reshape(-1)
	F14_y = F14['y'].reshape(-1)
	F14_z = F14['z'].reshape(-1)

	F22_x = F22['x'].reshape(-1)
	F22_y = F22['y'].reshape(-1)
	F22_z = F22['z'].reshape(-1)

	#Obtendo SAC_DM
	sac_dm_F0_x = sac_dm(F0_x, N)
	sac_dm_F0_y = sac_dm(F0_y, N)
	sac_dm_F0_z = sac_dm(F0_z, N)

	sac_dm_F6_x = sac_dm(F6_x, N)
	sac_dm_F6_y = sac_dm(F6_y, N)
	sac_dm_F6_z = sac_dm(F6_z, N)

	sac_dm_F14_x = sac_dm(F14_x, N)
	sac_dm_F14_y = sac_dm(F14_y, N)
	sac_dm_F14_z = sac_dm(F14_z, N)

	sac_dm_F22_x = sac_dm(F22_x, N)
	sac_dm_F22_y = sac_dm(F22_y, N)
	sac_dm_F22_z = sac_dm(F22_z, N)

	#Obtendo SAC_AM
	sac_am_F0_x = sac_am(F0_x, N)
	sac_am_F0_y = sac_am(F0_y, N)
	sac_am_F0_z = sac_am(F0_z, N)

	sac_am_F6_x = sac_am(F6_x, N)
	sac_am_F6_y = sac_am(F6_y, N)
	sac_am_F6_z = sac_am(F6_z, N)

	sac_am_F14_x = sac_am(F14_x, N)
	sac_am_F14_y = sac_am(F14_y, N)
	sac_am_F14_z = sac_am(F14_z, N)

	sac_am_F22_x = sac_am(F22_x, N)
	sac_am_F22_y = sac_am(F22_y, N)
	sac_am_F22_z = sac_am(F22_z, N)

	#Removendo ultima amostra
	sac_dm_F0_x.pop()
	sac_dm_F0_y.pop()
	sac_dm_F0_z.pop()
	
	sac_dm_F6_x.pop()
	sac_dm_F6_y.pop()
	sac_dm_F6_z.pop()

	sac_dm_F14_x.pop()
	sac_dm_F14_y.pop()
	sac_dm_F14_z.pop()

	sac_dm_F22_x.pop()
	sac_dm_F22_y.pop()
	sac_dm_F22_z.pop()

	sac_am_F0_x.pop()
	sac_am_F0_y.pop()
	sac_am_F0_z.pop()
	
	sac_am_F6_x.pop()
	sac_am_F6_y.pop()
	sac_am_F6_z.pop()

	sac_am_F14_x.pop()
	sac_am_F14_y.pop()
	sac_am_F14_z.pop()

	sac_am_F22_x.pop()
	sac_am_F22_y.pop()
	sac_am_F22_z.pop()

	# # Criando e plotando graficos para o treinamento de SAC-AM

	# Plotando graficos de forma individual

	# 								SAC-AM
	# utilLite.showSAC([sac_am_F0_x, sac_am_F6_x, sac_am_F14_x, sac_am_F22_x], "SAC-AM: Eixo X")
	# utilLite.showSAC([sac_am_F0_y, sac_am_F6_y, sac_am_F14_y, sac_am_F22_y], "SAC-AM: Eixo Y")
	# utilLite.showSAC([sac_am_F0_z, sac_am_F6_z, sac_am_F14_z, sac_am_F22_z], "SAC-AM: Eixo Z")

	# # 								SAC-DM
	# utilLite.showSAC([sac_dm_F0_x, sac_dm_F6_x, sac_dm_F14_x, sac_dm_F22_x], "SAC-DM: Eixo X")
	# utilLite.showSAC([sac_dm_F0_y, sac_dm_F6_y, sac_dm_F14_y, sac_dm_F22_y], "SAC-DM: Eixo Y")
	# utilLite.showSAC([sac_dm_F0_z, sac_dm_F6_z, sac_dm_F14_z, sac_dm_F22_z], "SAC-DM: Eixo Z")
	
	# # # 								Janela Deslizante em um arquivo txt
	utilLite.cleanTxtDetailedS(N, int(sys.argv[4]))
	utilLite.slidingWindowDetailedInTxt([sac_am_F0_x, sac_am_F6_x, sac_am_F14_x, sac_am_F22_x], ["F0", "F6", "F14", "F22"], "SAC-AM: Eixo X", int(sys.argv[4]), N)
	utilLite.slidingWindowDetailedInTxt([sac_am_F0_y, sac_am_F6_y, sac_am_F14_y, sac_am_F22_y], ["F0", "F6", "F14", "F22"], "SAC-AM: Eixo Y", int(sys.argv[4]), N)
	utilLite.slidingWindowDetailedInTxt([sac_am_F0_z, sac_am_F6_z, sac_am_F14_z, sac_am_F22_z], ["F0", "F6", "F14", "F22"], "SAC-AM: Eixo Z", int(sys.argv[4]), N)

	utilLite.slidingWindowDetailedInTxt([sac_dm_F0_x, sac_dm_F6_x, sac_dm_F14_x, sac_dm_F22_x], ["F0", "F6", "F14", "F22"], "SAC-DM: Eixo X", int(sys.argv[4]), N)
	utilLite.slidingWindowDetailedInTxt([sac_dm_F0_y, sac_dm_F6_y, sac_dm_F14_y, sac_dm_F22_y], ["F0", "F6", "F14", "F22"], "SAC-DM: Eixo Y", int(sys.argv[4]), N)
	utilLite.slidingWindowDetailedInTxt([sac_dm_F0_z, sac_dm_F6_z, sac_dm_F14_z, sac_dm_F22_z], ["F0", "F6", "F14", "F22"], "SAC-DM: Eixo Z", int(sys.argv[4]), N)
	
	# # # 								Janela Pulante em um arquivo txt
	# utilLite.cleanTxtDetailedJ(N, int(sys.argv[4]))
	# utilLite.jumpingWindowDetailedInTxt([sac_am_F0_x, sac_am_F6_x, sac_am_F14_x, sac_am_F22_x], ["F0", "F6", "F14", "F22"], "SAC-AM: Eixo X", int(sys.argv[4]), N)
	# utilLite.jumpingWindowDetailedInTxt([sac_am_F0_y, sac_am_F6_y, sac_am_F14_y, sac_am_F22_y], ["F0", "F6", "F14", "F22"], "SAC-AM: Eixo Y", int(sys.argv[4]), N)
	# utilLite.jumpingWindowDetailedInTxt([sac_am_F0_z, sac_am_F6_z, sac_am_F14_z, sac_am_F22_z], ["F0", "F6", "F14", "F22"], "SAC-AM: Eixo Z", int(sys.argv[4]), N)

	# utilLite.jumpingWindowDetailedInTxt([sac_dm_F0_x, sac_dm_F6_x, sac_dm_F14_x, sac_dm_F22_x], ["F0", "F6", "F14", "F22"], "SAC-DM: Eixo X", int(sys.argv[4]), N)
	# utilLite.jumpingWindowDetailedInTxt([sac_dm_F0_y, sac_dm_F6_y, sac_dm_F14_y, sac_dm_F22_y], ["F0", "F6", "F14", "F22"], "SAC-DM: Eixo Y", int(sys.argv[4]), N)
	# utilLite.jumpingWindowDetailedInTxt([sac_dm_F0_z, sac_dm_F6_z, sac_dm_F14_z, sac_dm_F22_z], ["F0", "F6", "F14", "F22"], "SAC-DM: Eixo Z", int(sys.argv[4]), N)

	# # # 								Plots com a comparação Janela Deslizante vs Janela Pulante
	# utilLite.windowsPlot([sac_am_F0_x, sac_am_F6_x, sac_am_F14_x, sac_am_F22_x], ["F0", "F6", "F14", "F22"], "SAC-AM: Eixo X", int(sys.argv[4]), N)
	# utilLite.windowsPlot([sac_am_F0_y, sac_am_F6_y, sac_am_F14_y, sac_am_F22_y], ["F0", "F6", "F14", "F22"], "SAC-AM: Eixo Y", int(sys.argv[4]), N)
	# utilLite.windowsPlot([sac_am_F0_z, sac_am_F6_z, sac_am_F14_z, sac_am_F22_z], ["F0", "F6", "F14", "F22"], "SAC-AM: Eixo Z", int(sys.argv[4]), N)

	# utilLite.windowsPlot([sac_dm_F0_x, sac_dm_F6_x, sac_dm_F14_x, sac_dm_F22_x], ["F0", "F6", "F14", "F22"], "SAC-DM: Eixo X", int(sys.argv[4]), N)
	# utilLite.windowsPlot([sac_dm_F0_y, sac_dm_F6_y, sac_dm_F14_y, sac_dm_F22_y], ["F0", "F6", "F14", "F22"], "SAC-DM: Eixo Y", int(sys.argv[4]), N)
	# utilLite.windowsPlot([sac_dm_F0_z, sac_dm_F6_z, sac_dm_F14_z, sac_dm_F22_z], ["F0", "F6", "F14", "F22"], "SAC-DM: Eixo Z", int(sys.argv[4]), N)

	# plt.show()
	return 0

#********* Main ********
filename = sys.argv[1]
filename2 = sys.argv[2]

# test(filename, filename2)
plotSAC_AM_DM()