import matplotlib.pyplot as plt
import scipy.io
import numpy as np
import matplotlib.colors as mcolors


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

def cleanTxtDetailed(N, window_size):
	filename = (f"LiteSlidingWindowN{N}Size{window_size}.txt")
	file1 = open(filename, 'a+')
	file1.truncate(0)
	file1.close()

def get_change_t(current, previous):
    if current == previous:
        return 0
    try:
        return (abs(current)  / previous) * 100.0
    except ZeroDivisionError:
        return 0

def slidingWindowDetailedInTxt(dataset, arquivos, title, window_size, N):

	filename = (f"LiteSlidingWindowN{N}Size{window_size}.txt")
	file1 = open(filename, 'a+')
	media = np.zeros((len(dataset)))
	desvio = np.zeros((len(dataset)))
	matrixSaida = np.zeros((len(dataset),len(dataset)+1))
	matrix = np.zeros((len(dataset),len(dataset)+1))
	pontos_inconclusivos_int = np.zeros((len(dataset),len(dataset[0])))


	file1.write((title + "\n\n"))
	for i in range(len(dataset)):
		media[i] = media_sac(dataset[i], 0, len(dataset[i]))
		desvio[i] = desvio_sac(dataset[i], 0, len(dataset[i]))
		file1.write((arquivos[i] + ":" + " Média - " + str(round(media[i], 4)) + "\n"))
		file1.write((arquivos[i] + ":" + " Desvio padrao - " + str(round(desvio[i], 4)) + "\n"))
		file1.write((arquivos[i] + ":" + " Limite inferior - " + str(round(media[i] - desvio[i], 4)) + " | " + "Limite superior - " + str(round(media[i] + desvio[i], 4)) +"\n\n"))

	for i in range(len(dataset)): # Arquivos com os mesmos eixos

		for j in range( (len(dataset[i]) - window_size + 1) ): # array com n pontos
			janela = dataset[i][j:j+window_size]
			conclusion = np.zeros((len(arquivos) + 1))
			track = np.zeros(window_size)

			for k in range(len(janela)):
				if (janela[k] >= media[0] - desvio[0] and janela[k] <= media[0] + desvio[0]):
					conclusion[0] += 1
					continue

				elif(janela[k] >= media[1] - desvio[1] and janela[k] <= media[1] + desvio[1]):
					conclusion[1] += 1
					continue

				elif(janela[k] >= media[2] - desvio[2] and janela[k] <= media[2] + desvio[2]):
					conclusion[2] += 1
					continue

				elif(janela[k] >= media[3] - desvio[3] and janela[k] <= media[3] + desvio[3]):
					conclusion[3] += 1
					continue
				
				else:
					conclusion[4] += 1
					track[k] = 1
			
			matrix[i][np.argmax(conclusion)] += 1
			if( np.argmax(conclusion) == 4):
				pontos_inconclusivos_int[i][j] = dataset[i][j]
				

	file1.write(f"Matriz de confusao - Janela Deslizante[{window_size}] - N{N}\n\n")
	file1.write((f"{'Arquivo':<10}"))
	for i in range(len(arquivos)):
		file1.write(f"{arquivos[i]:<10}")
	file1.write(f"{'Inconclusivo':<10}\n")

	for i in range(len(matrix)):
		file1.write(f"{arquivos[i]:<10}")
		for j in range(len(matrix[i])):
			matrixSaida[i][j] = round(get_change_t(matrix[i][j],len(dataset[i])),2)
			file1.write(f"{matrixSaida[i][j]:<10}")
		file1.write("\n\n")


	file1.close()

