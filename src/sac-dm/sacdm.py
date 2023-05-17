# Standard python numerical analysis imports:
import numpy as np
from scipy import signal
from scipy.signal import find_peaks, peak_prominences

#import pandas as pd
#import peakutils

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import scipy.io

#import h5py

import sys
import time

import autocorrelation as auto
import chaos
import util

# def get_data_from_wav(filename):
# 	Fs, data = read(filename)
# 	data = data[:,0]
# 	return data, Fs

# Calcula SAC-DM medio total utilizando a funcao find_peaks do Python
def sac_dm_avg(data):
	peaks, _ = find_peaks(data)
	
	npeaks = 0.0 + len(peaks)
	n = len(data)
	
	return npeaks/n


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

# Calcula SAC-DM utilizando a funcao find_peaks do Python
def sac_dm_slow(data, N):
	peaks, _ = find_peaks(data)
	
	M = len(data)
	size = 1 + int(M/N)
	sacdm=[0.0] * size
	picos=[0.0] * size

	inicio = 0
	fim = N

	v = np.array(peaks)
	for k in range(size):
		#sum(v<fim) retorna a quantidade de elementos em v menores que fim. Ou seja, a quantidade de True da clausula
		sacdm[k] = sum(v<fim) - sum(v<inicio)
		inicio = fim
		fim = fim + N
	
	return np.true_divide(sacdm,N),peaks


# Calcula SAC-PM a prominencia (altura) media dos picos utilizando a funcao peak_prominences do Python
def sac_pm(data):
	peaks, _ = find_peaks(data)
	return peaks


# Calcula SAC-AM a largura  media dos picos utilizando a funcao peak_width do Python
def sac_wm(data):
	peaks, _ = find_peaks(data)
	return len(peaks)/len(data)


def sac_dm_old(data, N, threshold):
	
	M = len(data)
	#M = 50000

	print ("Numero de amostras: ", M)
	rho = 0.0

	size = 1 + int(M/N)
	sacdm=[0.0] * size


	up = 0
	peaks = 0
	i = 0
	n = N
	j = 0
	while i < M-2:
		a = data[i]
		b = data[i+1]
		c = data[i+2]

		if b > (a*(1+threshold)) and b > (c*(1+threshold)):
			peaks = peaks + 1
			
		if i == n:
			rho =  peaks/float(N)

			if rho != 0:
				sacdm[j] = rho 
				#sacdm[j]=1/(6*rho)
				#print "peaks: ", peaks , " N: ", N, " rho: ", rho, "sacdm: ", sacdm[j]
			else:
				sacdm[j] = 0
			j = j + 1
			n = n + N
			peaks = 0
		i = i+1

	#plot SAC-DM:
	#print data
	return sacdm



def test(file1, file2):
	N = int(sys.argv[3])
	
	#mat = scipy.io.loadmat(file1)
	#mat2 = scipy.io.loadmat(file2)
	#data = mat['y1']
	#data2 = mat2['y1']

	d = np.genfromtxt( filename, delimiter=';', names=['x','y','z','s','t'])
	d2 = np.genfromtxt( filename2, delimiter=';', names=['x','y','z','s','t'])


	data = d['z'].reshape(-1)
	data2 = d2['z'].reshape(-1)


	data = data.flatten()
	data2 = data2.flatten()

	#data = np.genfromtxt(file1name, delimiter='	')
	#data2 = np.genfromtxt(file2, delimiter='	')


	sac = sac_dm(data, N)
	am = sac_am(data, N)
	#pm = sac_pm(data, N)
	#wm = sac_wm(data, N)
	
	sac2 = sac_dm(data2, N)
	am2 = sac_am(data2, N)
	#pm2 = sac_pm(data2, N)
	#wm2 = sac_wm(data2, N)
	

	util.show([sac, sac2], "SAC-DM")
	util.show([am, am2], "SAC-AM")
	#util.show(pm, pm2, "SAC-PM")
	#util.show(wm, wm2, "SAC-WM")

	
	


#************************************

	corr = auto.autocorrelation(data, N)
	corr2 = auto.autocorrelation(data2, N)

	util.show([corr, corr2], "Autocorrelation")

	#le = lyapunov_e(data[0:10000], 1000)
	lr = chaos.lyapunov_e(data, N)
	lr2 = chaos.lyapunov_e(data2, N)

	#print (le.shape)
	print (lr.shape)

	util.show([lr, lr2], 'lyapunov coef')

	l = max(lr)
	l2 = max(lr2)

	print ('lyapunov max coef: ', l)
	print ('lyapunov max coef: ', l2)

	plt.show()

	return 0

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

	# fig_SAC_AM_T, (ax1_SAC_AM_X_T, ax2_SAC_AM_Y_T, ax3_SAC_AM_Z_T) = plt.subplots(3)
	# util.showTreinamento([sac_am_F0_x, sac_am_F0_y, sac_am_F0_z], "SAC-AM", fig_SAC_AM_T, [ax1_SAC_AM_X_T, ax2_SAC_AM_Y_T, ax3_SAC_AM_Z_T])

	# # Criando e plotando graficos para o treinamento de SAC-DM

	# fig_SAC_DM_T, (ax1_SAC_DM_X_T, ax2_SAC_DM_Y_T, ax3_SAC_DM_Z_T) = plt.subplots(3)
	# util.showTreinamento([sac_dm_F0_x, sac_dm_F0_y, sac_dm_F0_z], "SAC-DM", fig_SAC_DM_T, [ax1_SAC_DM_X_T, ax2_SAC_DM_Y_T, ax3_SAC_DM_Z_T])


	# # Plotando em uma unica figura, todos os graficos

	# util.showSAC_figUnico([[sac_am_F0_x, sac_am_F0_y, sac_am_F0_z], [sac_am_F6_x, sac_am_F6_y, sac_am_F6_z], [sac_am_F14_x, sac_am_F14_y, sac_am_F14_z],
	# 						[sac_am_F22_x, sac_am_F22_y, sac_am_F22_z]], "SAC-AM")
	# util.showSAC_figUnico([[sac_dm_F0_x, sac_dm_F0_y, sac_dm_F0_z], [sac_dm_F6_x, sac_dm_F6_y, sac_dm_F6_z], [sac_dm_F14_x, sac_dm_F14_y, sac_dm_F14_z],
	# 						[sac_dm_F22_x, sac_dm_F22_y, sac_dm_F22_z]], "SAC-DM")


	# # Plotando em uma unica figura, todos os graficos com treino
	# util.showSAC_figUnicoComTreino([[sac_am_F0_x, sac_am_F0_y, sac_am_F0_z], [sac_am_F6_x, sac_am_F6_y, sac_am_F6_z], [sac_am_F14_x, sac_am_F14_y, sac_am_F14_z],
	# 						[sac_am_F22_x, sac_am_F22_y, sac_am_F22_z]], "SAC-AM")

	# util.showSAC_figUnicoComTreino([[sac_dm_F0_x, sac_dm_F0_y, sac_dm_F0_z], [sac_dm_F6_x, sac_dm_F6_y, sac_dm_F6_z], [sac_dm_F14_x, sac_dm_F14_y, sac_dm_F14_z],
	# 						[sac_dm_F22_x, sac_dm_F22_y, sac_dm_F22_z]], "SAC-DM")



	# Plotando graficos de forma individual

	# # 								SAC-AM
	# util.showSAC([sac_am_F0_x, sac_am_F6_x, sac_am_F14_x, sac_am_F22_x], "SAC-AM: Eixo X")
	# util.showSAC([sac_am_F0_y, sac_am_F6_y, sac_am_F14_y, sac_am_F22_y], "SAC-AM: Eixo Y")
	# util.showSAC([sac_am_F0_z, sac_am_F6_z, sac_am_F14_z, sac_am_F22_z], "SAC-AM: Eixo Z")

	# # 								SAC-DM
	# util.showSAC([sac_dm_F0_x, sac_dm_F6_x, sac_dm_F14_x, sac_dm_F22_x], "SAC-DM: Eixo X")
	# util.showSAC([sac_dm_F0_y, sac_dm_F6_y, sac_dm_F14_y, sac_dm_F22_y], "SAC-DM: Eixo Y")
	# util.showSAC([sac_dm_F0_z, sac_dm_F6_z, sac_dm_F14_z, sac_dm_F22_z], "SAC-DM: Eixo Z")


	# # 								Matriz de confusao

	util.confusionMatrix([sac_am_F0_x, sac_am_F6_x, sac_am_F14_x, sac_am_F22_x], ["F0", "F6", "F14", "F22"], "SAC-AM: Eixo X")
	util.confusionMatrix([sac_am_F0_y, sac_am_F6_y, sac_am_F14_y, sac_am_F22_y], ["F0", "F6", "F14", "F22"], "SAC-AM: Eixo Y")
	util.confusionMatrix([sac_am_F0_z, sac_am_F6_z, sac_am_F14_z, sac_am_F22_z], ["F0", "F6", "F14", "F22"], "SAC-AM: Eixo Z")

	util.confusionMatrix([sac_dm_F0_x, sac_dm_F6_x, sac_dm_F14_x, sac_dm_F22_x], ["F0", "F6", "F14", "F22"], "SAC-DM: Eixo X")
	util.confusionMatrix([sac_dm_F0_y, sac_dm_F6_y, sac_dm_F14_y, sac_dm_F22_y], ["F0", "F6", "F14", "F22"], "SAC-DM: Eixo Y")
	util.confusionMatrix([sac_dm_F0_z, sac_dm_F6_z, sac_dm_F14_z, sac_dm_F22_z], ["F0", "F6", "F14", "F22"], "SAC-DM: Eixo Z")
	plt.show()

	return 0

#********* Main ********
filename = sys.argv[1]
filename2 = sys.argv[2]

# test(filename, filename2)
plotSAC_AM_DM()






