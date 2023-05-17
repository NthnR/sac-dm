import matplotlib.pyplot as plt
import scipy.io
import numpy as np
import matplotlib.colors as mcolors

def moving_average(a, n=3) :
	ret = np.cumsum(a, dtype=float)
	ret[n:] = ret[n:] - ret[:-n]
	return ret[n - 1:] / n

def compress(a, n=3):
	i=0
	j=n
	k=0
	ret = np.zeros(1)
	for k in range(int(len(a)/n)):
		ret = np.append(ret,np.average(a[i:j]))
		i = j
		j = j+n
	return ret
    

def show(dataset, title):
	print("dataset ", len(dataset))
	fig, ax = plt.subplots()

	plt.ylabel(title) 
	plt.xlabel('Time (ms)')
	
	ax.set_title(title)  
	colors = list(mcolors.CSS4_COLORS) 

	for i in range(len(dataset)):
		print("sub dataset ", len(dataset[i]))
		ax.plot(dataset[i],color=colors[i+10], label=("Data" ,i))	
		
	plt.legend(loc='upper left')


	#plt.show()
	return 1

def treinamentoMetade(dataset, title, fig, ax):
	
	plt.ylabel(title) 
	plt.xlabel('Time (ms)')
	
	colors = list(mcolors.CSS4_COLORS) 

	media_dataset = media_sac(dataset, 0, round(len(dataset)))
	desv_dataset = desvio_sac(dataset, 0, round(len(dataset)))

	aux_desv = np.zeros(len(dataset))
	aux_desv[round((len(dataset))/2)] = desv_dataset

	x = np.arange(len(dataset))
	y = np.zeros(len(dataset))
	y = np.full_like(y, media_dataset)

	ax.plot(x,y,color=colors[10], label = "Média da primeira metade do SAC F0")

	for j in range(len(dataset)):

		if(aux_desv[j] != 0):			
			ax.errorbar(j,media_dataset,yerr = aux_desv[j], color = colors[20],marker='s', capsize=2, markersize=4, linewidth=1, linestyle='--')

	ax.fill_between(x, media_dataset - desv_dataset, media_dataset + desv_dataset, alpha = 0.2, label = "Desvio Padrão da primeira metade do Arquivo F0")


def treinamentoCompleto(dataset, title, fig, ax):
	
	aux = title.split(':',1)
	plt.ylabel(aux[0]) 
	plt.xlabel('Time (ms)')
	

	ax.set_title(title)  
	colors = list(mcolors.CSS4_COLORS) 

	media_dataset = media_sac(dataset, 0, round(len(dataset)))
	desv_dataset = desvio_sac(dataset, 0, round(len(dataset)))

	aux_desv = np.zeros(len(dataset))
	aux_desv[round((len(dataset))/2)] = desv_dataset

	x = np.arange(len(dataset))
	y = np.zeros(len(dataset))
	y = np.full_like(y, media_dataset)

	ax.plot(x,y,color=colors[10], label = "Média do Arquivo F0")


	plt.xlim(right = (len(dataset)))

	for j in range(len(dataset)):

		if(aux_desv[j] != 0):			
			ax.errorbar(j,media_dataset,yerr = aux_desv[j], color = colors[20],marker='s', capsize=2, markersize=4, linewidth=1, linestyle='--')

	ax.fill_between(x, media_dataset - desv_dataset, media_dataset + desv_dataset, alpha = 0.2, label = "Desvio Padrão do Arquivo F0")




def testagem(dataset, title, fig, ax, color):

	colors = list(mcolors.CSS4_COLORS) 
	ax.plot(dataset,color=colors[color], label = title)
	
def showTreinamento(dataset, title, fig, ax):

	fig.suptitle('Treinamento')

	#				Eixo X
	auxT = title + ": Eixo X"
	ax[0].set_title(auxT)
	ax[0].set(ylabel = title)
	dataset_treinamento = amostragem_sac(dataset[0], 0, (round(len(dataset[0])/2) + 1))
	treinamentoMetade(dataset_treinamento, title, fig, ax[0])
	dataset_teste = amostragem_sac(dataset[0], round(len(dataset[0])/2), len(dataset[0]) )
	testagem(dataset_teste, "Segunda metade do arquivo F0", fig, ax[0], 11)
	ax[0].legend(loc = 'lower left')

	#				Eixo Y
	auxT = title + ": Eixo Y"
	ax[1].set_title(auxT)
	ax[1].set(ylabel = title)
	dataset_treinamento = amostragem_sac(dataset[1], 0, (round(len(dataset[1])/2) + 1))
	treinamentoMetade(dataset_treinamento, title, fig, ax[1])
	dataset_teste = amostragem_sac(dataset[1], round(len(dataset[1])/2), len(dataset[1]) )
	testagem(dataset_teste, "Segunda metade do arquivo F0", fig, ax[1], 12)
	ax[1].legend(loc = 'upper right')

	#				Eixo Z
	auxT = title + ": Eixo Z"
	ax[2].set_title(auxT)
	ax[2].set(ylabel = title)
	dataset_treinamento = amostragem_sac(dataset[2], 0, (round(len(dataset[2])/2) + 1))
	treinamentoMetade(dataset_treinamento, title, fig, ax[2])
	dataset_teste = amostragem_sac(dataset[2], round(len(dataset[2])/2), len(dataset[2]) )
	testagem(dataset_teste, "Segunda metade do arquivo F0", fig, ax[2], 13)
	ax[2].legend(loc = 'upper right')

def showSAC_figUnico(dataset, title):

	# # Criando graficos base ( Treinamento )
	fig, (ax1_X, ax2_Y, ax3_Z) = plt.subplots(3)
	treinamentoCompleto(dataset[0][0], "Eixo X", fig, ax1_X)
	treinamentoCompleto(dataset[0][1], "Eixo Y", fig, ax2_Y)
	treinamentoCompleto(dataset[0][2], "Eixo Z", fig, ax3_Z)

	fig.suptitle(title)

	ax1_X.set(ylabel = title)
	ax2_Y.set(ylabel = title)
	ax3_Z.set(ylabel = title)

	# # Plotar os eixos nos gráficos base ( Teste )
	# #						Eixo X

	testagem(dataset[1][0], 'Arquivo F6', fig, ax1_X, 11)
	testagem(dataset[2][0], 'Arquivo F14', fig, ax1_X, 12)
	testagem(dataset[3][0], 'Arquivo F22', fig, ax1_X, 13)
	ax1_X.legend(loc='lower right')

	# # 					Eixo Y
	testagem(dataset[1][1], 'Arquivo F6', fig, ax2_Y, 11)
	testagem(dataset[2][1], 'Arquivo F14', fig, ax2_Y, 12)
	testagem(dataset[3][1], 'Arquivo F22', fig, ax2_Y, 13)
	ax2_Y.legend(loc='lower right')

	# # 					Eixo Z
	testagem(dataset[1][2], 'Arquivo F6', fig, ax3_Z, 11)
	testagem(dataset[2][2], 'Arquivo F14', fig, ax3_Z, 12)
	testagem(dataset[3][2], 'Arquivo F22', fig, ax3_Z, 13)
	ax3_Z.legend(loc='lower right')

def showSAC_figUnicoComTreino(dataset, title):

	# # Criando graficos base ( Treinamento )
	fig, (ax1_X, ax2_Y, ax3_Z) = plt.subplots(3)

	auxT = title + ": Eixo X"
	ax1_X.set_title('Eixo X')
	dataset_treinamento = amostragem_sac(dataset[0][0], 0, (round(len(dataset[0][0])/2) + 1))
	treinamentoMetade(dataset_treinamento, auxT, fig, ax1_X)
	dataset_teste = amostragem_sac(dataset[0][0], round(len(dataset[0][0])/2), len(dataset[0][0]) )
	testagem(dataset_teste, "Segunda metade do Arquivo F0", fig, ax1_X, 16)

	auxT = title + ": Eixo Y"
	ax2_Y.set_title('Eixo Y')
	dataset_treinamento = amostragem_sac(dataset[0][1], 0, (round(len(dataset[0][1])/2) + 1))
	treinamentoMetade(dataset_treinamento, auxT, fig, ax2_Y)
	dataset_teste = amostragem_sac(dataset[0][1], round(len(dataset[0][1])/2), len(dataset[0][1]) )
	testagem(dataset_teste, "Segunda metade do Arquivo F0", fig, ax2_Y, 16)

	auxT = title + ": Eixo Z"
	ax3_Z.set_title('Eixo Z')
	dataset_treinamento = amostragem_sac(dataset[0][2], 0, (round(len(dataset[0][2])/2) + 1))
	treinamentoMetade(dataset_treinamento, auxT, fig, ax3_Z)
	dataset_teste = amostragem_sac(dataset[0][2], round(len(dataset[0][2])/2), len(dataset[0][2]) )
	testagem(dataset_teste, "Segunda metade do Arquivo F0", fig, ax3_Z, 16)



	fig.suptitle(title)

	ax1_X.set(ylabel = title)
	ax2_Y.set(ylabel = title)
	ax3_Z.set(ylabel = title)

	# # Plotar os eixos nos gráficos base ( Teste )
	# #							Eixo X
	dataset_teste = amostragem_sac(dataset[1][0], round(len(dataset[1][0])/2), len(dataset[1][0]) )
	testagem(dataset_teste, 'Arquivo F6', fig, ax1_X, 11)

	dataset_teste = amostragem_sac(dataset[2][0], round(len(dataset[2][0])/2), len(dataset[2][0]) )
	testagem(dataset_teste, 'Arquivo F14', fig, ax1_X, 12)

	dataset_teste = amostragem_sac(dataset[3][0], round(len(dataset[3][0])/2), len(dataset[3][0]) )
	testagem(dataset_teste, 'Arquivo F22', fig, ax1_X, 13)
	ax1_X.legend(loc='lower right')

	# # 						Eixo Y
	dataset_teste = amostragem_sac(dataset[1][1], round(len(dataset[1][1])/2), len(dataset[1][1]) )
	testagem(dataset_teste, 'Arquivo F6', fig, ax2_Y, 11)

	dataset_teste = amostragem_sac(dataset[2][1], round(len(dataset[2][1])/2), len(dataset[2][1]) )
	testagem(dataset_teste, 'Arquivo F14', fig, ax2_Y, 12)

	dataset_teste = amostragem_sac(dataset[3][1], round(len(dataset[3][1])/2), len(dataset[3][1]) )
	testagem(dataset_teste, 'Arquivo F22', fig, ax2_Y, 13)
	ax2_Y.legend(loc='lower right')

	# # 						Eixo Z
	dataset_teste = amostragem_sac(dataset[1][2], round(len(dataset[1][2])/2), len(dataset[1][2]) )
	testagem(dataset_teste, 'Arquivo F6', fig, ax3_Z, 11)

	dataset_teste = amostragem_sac(dataset[2][2], round(len(dataset[2][2])/2), len(dataset[2][2]) )
	testagem(dataset_teste, 'Arquivo F14', fig, ax3_Z, 12)

	dataset_teste = amostragem_sac(dataset[3][2], round(len(dataset[3][2])/2), len(dataset[3][2]) )
	testagem(dataset_teste, 'Arquivo F22', fig, ax3_Z, 13)
	ax3_Z.legend(loc='lower right')

def showSAC(dataset, title):

	# # Criando graficos base ( Treinamento )
	fig, ax = plt.subplots()

	treinamentoCompleto(dataset[0],title, fig, ax)

	# # Plotar os eixos nos gráficos base ( Teste )
	testagem(dataset[1], 'Arquivo F6', fig, ax, 11)
	testagem(dataset[2], 'Arquivo F14', fig, ax, 12)
	testagem(dataset[3], 'Arquivo F22', fig, ax, 13)
	ax.legend(loc='lower right')


def media_sac(dataset,inicio,fim):

	media = np.average(dataset[inicio:fim])

	return media

def variancia_sac(dataset,inicio,fim):

	variancia = np.var(dataset[inicio:fim])

	return variancia

def desvio_sac(dataset, inicio, fim):

	desvio_padrao = np.std(dataset[inicio:fim])

	return desvio_padrao

def amostragem_sac(dataset, inicio, fim):

	return dataset[inicio:fim]

def confusionMatrix(dataset, arquivos, title):

	media = np.zeros((len(dataset)))
	desvio = np.zeros((len(dataset)))
	matrix = np.zeros((len(dataset),len(dataset)+1))

	for i in range(len(dataset)):
		media[i] = media_sac(dataset[i], 0, len(dataset[i]))
		desvio[i] = desvio_sac(dataset[i], 0, len(dataset[i]))

	for i in range(len(dataset)): # Arquivos com os mesmos eixos
		for j in range(len(dataset[i])): # array com n pontos
			
			if (dataset[i][j] >= media[0] - desvio[0] and dataset[i][j] <= media[0] + desvio[0]):
				matrix[i][0] += 1
				continue

			elif(dataset[i][j] >= media[1] - desvio[1] and dataset[i][j] <= media[1] + desvio[1]):
				matrix[i][1] += 1
				continue

			elif(dataset[i][j] >= media[2] - desvio[2] and dataset[i][j] <= media[2] + desvio[2]):
				matrix[i][2] += 1
				continue

			elif(dataset[i][j] >= media[3] - desvio[3] and dataset[i][j] <= media[3] + desvio[3]):
				matrix[i][3] += 1
				continue
			
			else:
				matrix[i][4] += 1


	print(f"\n\t\t{title}\n")

	print(f"{'Arquivo':<10}", end="")
	for i in range(len(arquivos)):
		print(f"{arquivos[i]:<10}", end="")

	print(f"{'Inconclusivo':<10}")

	for i in range(len(matrix)):
		print(f"{arquivos[i]:<10}{matrix[i][0]:<10}{matrix[i][1]:<10}{matrix[i][2]:<10}{matrix[i][3]:<10}{matrix[i][4]:<10}")
	


	