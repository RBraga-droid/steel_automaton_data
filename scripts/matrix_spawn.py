import sys
import os
import csv
import random
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import pyplot, patches
##  Processa il file dump per ricavare solo gli opcodes
def process_file(input_filename, output_filename):
    with open(input_filename, 'r') as input_file, open(output_filename, 'w') as output_file:
        for line in input_file:
            # Rimuovi spazi bianchi iniziali e finali dalla riga
            line = line.strip()

            # Controlla se la riga è più lunga di 100 caratteri
            if len(line) <= 100:
                # Dividi la riga in parole
                words = line.split()

                # Assicurati che ci siano almeno due parole nella riga
                if len(words) >= 2:
                    # Prendi la seconda parola e cattura i primi 4 (o 2) caratteri esadecimali in lettere minuscole
                    second_word = words[1][:2].lower()

                    # Verifica se i primi 4 caratteri sono tutti esadecimali
                    if all(char in '0123456789abcdef' for char in second_word):
                        # Scrivi i primi 4 caratteri esadecimali in lettere minuscole nel file di output
                        output_file.write(second_word + '\n')
##  Come da nome
def ottieni_nome_file_da_percorso(percorso_file):
    # Utilizza la funzione basename di os per ottenere solo il nome del file dal percorso
    nome_file = os.path.basename(percorso_file)
    return nome_file
##  Come da nome
def ottieni_percorso_senza_file(percorso_file):
    # Utilizza la funzione dirname di os per ottenere il percorso senza il nome del file
    percorso_senza_file = os.path.dirname(percorso_file)
    return percorso_senza_file

## Funzione per generare il file CSV con le transizioni
def generate_csv(input_filename, output_filename):
    transitions = {}

    with open(input_filename, 'r') as infile:
        hex_sequence = infile.read().split()

    for i in range(len(hex_sequence) - 1):
        source = hex_sequence[i]
        target = hex_sequence[i + 1]
        transition = (source, target)

        if transition in transitions:
            transitions[transition] += 1
        else:
            transitions[transition] = 1

    with open(output_filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Partenza', 'Arrivo', 'Peso'])

        for (source, target), weight in transitions.items():
            csvwriter.writerow([source, target, weight])

    print(f"File CSV '{output_filename}' generato con successo.")
    

## Cambiare estensione
def cambia_estensione(nome_file, nuova_estensione):
    # Utilizza la funzione splitext di os.path per dividere il nome del file e l'estensione
    nome_base, vecchia_estensione = os.path.splitext(nome_file)

    # Combina il nome del file base con la nuova estensione
    nuovo_nome_file = nome_base + nuova_estensione

    return nuovo_nome_file
    
##  Funzione per la definizione dei colori
def rgb_int2tuple(rgbint):
    return (rgbint // 256 // 256 % 256, rgbint // 256 % 256, rgbint % 256)
    
##  Funzione per la trasformata logaritmica dei pesi


# Serie di dati
def log_transformator(original_data):

  # Applica la trasformazione logaritmica in base 10
  log_transformed_data = [np.log10(x) for x in original_data]

  return (log_transformed_data)
  
## Funzione per la adjacency matrix
def draw_adjacency_matrix(G, input_filename, node_order=None, partitions=[], colors=[]):

    #adjacency_matrix = nx.to_numpy_matrix(G, dtype=bool, nodelist=node_order)
    adjacency_matrix = nx.to_numpy_array(G, weight='weight')
    weights = nx.get_edge_attributes(G,'weight').values()
    max_weight = max(weights)
    min_weight = min(weights)
    normalized_weights = [(weight - min_weight) / (max_weight - min_weight) for weight in weights]
    normalized_adj_matrix = adjacency_matrix / max_weight
    log_normalized_weights = [np.log(weight + 1)for weight in weights]
    log_normalized_adj_matrix = np.log(adjacency_matrix + 1)
    
    #Plot adjacency matrix in toned-down black and white
    fig = pyplot.figure(figsize=(50, 50)) # in inches
    pyplot.imshow(log_normalized_adj_matrix,
                  cmap="Greys",
                  interpolation="nearest")
    
    # The rest is just if you have sorted nodes by a partition and want to
    ## highlight the module boundaries
    #assert len(partitions) == len(colors)
    #ax = pyplot.gca()
    #for partition, color in zip(partitions, colors):
    #    current_idx = 0
    #    for module in partition:
    #        ax.add_patch(patches.Rectangle((current_idx, current_idx),
    #                                      len(module), # Width
    #                                      len(module), # Height
    #                                      facecolor="none",
    #                                      edgecolor=color,
    #                                      linewidth="1"))
    #        current_idx += len(module)
    fig.savefig(input_filename)
    
    import torch
    from torch_geometric.data import Data
    from torch_geometric.utils.convert import from_networkx
    from torch_geometric.transforms import Pad
    # Funzione per convertire la matrice di adiacenza in una lista di archi
    #def adjacency_matrix_to_edge_list(adjacency_matrix):
        #edge_index = []
        #num_nodes = adjacency_matrix.shape[0]
        #for i in range(num_nodes):
        #    for j in range(i+1, num_nodes):
        #        if adjacency_matrix[i, j].any():  # Se c'è un arco tra i nodi i e j
        #            edge_index.append([i, j])
        #return torch.tensor(edge_index).t().contiguous()
        
    # Converti la matrice di adiacenza in una lista di archi
    #edge_index = adjacency_matrix_to_edge_list(adjacency_matrix)

    # Crea un oggetto Data per il grafo
    #label = 0 #for not malware
    #label = 1 #for malware
    #data = Data(edge_index=edge_index, y=torch.tensor([label]))
    
    data = from_networkx(G)
    if "softonic" in input_filename or "Windows" in input_filename:
        print("qui era y=0 windows o softonic")
        data.y = 0
    else: 
        data.y = 1
    num_nodes = 256
    num_edges = 65536
    node_padding = 0
    edge_padding = 0
    transform = Pad(num_nodes, num_edges, node_padding, edge_padding)
    data = transform(data)
    #Salva i dati in un file .pt
    torch.save(data, cambia_estensione(input_filename, ".pt"))

def linear_transformator(original_data):

  # Applica la trasformazione logaritmica in base 10
  log_transformed_data = [100+x for x in original_data]

  return (log_transformed_data)

##  Funzione per definire il grafo
def graph_spawn(input_filename):
    g = nx.DiGraph()

    # Legge il file CSV e aggiunge gli archi al grafo
    with open(input_filename, mode='r') as input_file:
        reader = csv.DictReader(input_file)
        for row in reader:
            source = row['Partenza']
            target = row['Arrivo']
            if int(row['Peso'])>0:  #---------------------------------------------------------------------------------------------------------------LIMIT DEI PESI
              g.add_edge(source, target, weight=(int(row['Peso'])))


    
    #print(nx.get_edge_attributes(g,'weight').values())
    #weights = log_transformator(nx.get_edge_attributes(g,'weight').values())
    
    #weights = nx.get_edge_attributes(g,'weight').values()
    #print(weights)
    n_nodes = len(g.nodes)
    #print(n_nodes)
    # Definizione delle posizioni
    pos = {node:(int(node, 16) // 16,int(node, 16) % 16) for node in g.nodes}
    #print(pos)
    # Plottaggio immagine
    plt.figure(3,figsize=(60,60))

    #nx.draw_networkx(g, pos, width=3*list(weights), with_labels=True)

    #plt.savefig(cambia_estensione(input_filename, ".png"))
    print("salvando in "+input_filename)
    draw_adjacency_matrix(g, cambia_estensione(input_filename, "-matrix.png"))
    
    
    





def elimina_file_non_desiderati(cartella, file_da_ignorare):
    # Elenco dei file nella cartella
    elenco_file = os.listdir(cartella)

    # Itera su ogni file nella cartella
    for nome_file in elenco_file:
        percorso_file = os.path.join(cartella, nome_file)



        # Verifica se il file ha un'estensione diversa da .png o .py
        if os.path.isfile(percorso_file) and not ( nome_file.endswith('.pt') or nome_file.endswith('.png')): #(nome_file.endswith('.png') or nome_file.endswith('.py') or nome_file.endswith('.csv') or
            try:
                # Elimina il file
                os.remove(percorso_file)
                print(f"File eliminato: {nome_file}")
            except Exception as e:
                print(f"Errore durante l'eliminazione di {nome_file}: {e}")

##  main dello script

def main():
    # Verifica se è stato fornito almeno un argomento
    if len(sys.argv) < 2:
        print("Usage: python script.py <argomento>")
        sys.exit(1)

    # Assegna l'argomento alla variabile interna
    input_file_path = sys.argv[1]
    input_filename = ottieni_nome_file_da_percorso(input_file_path)
    output_filename = "opcodes_"+input_filename
    output_path = ottieni_percorso_senza_file(input_file_path)+"\\..\\images\\"+output_filename
    # Il file viene purificato dalle stringhe di controllo del logging process
    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    with open(ottieni_percorso_senza_file(input_file_path)+"\\..\\images\\"+input_filename, 'w') as file:
        for line in lines:
            if not line.startswith('u'):
                file.write(line)
    
    # Il file di testo diventa solo una lista di opcodes
    process_file(ottieni_percorso_senza_file(input_file_path)+"\\..\\images\\"+input_filename, output_path)
    # Viene creato il nome per il file .csv
    dumps_csv = cambia_estensione(output_path, ".csv")
    # Generato il file .csv
    generate_csv(output_path, dumps_csv)
    # Genera il grafo
    g = graph_spawn(dumps_csv)

    # Specifica la cartella di destinazione
    cartella_da_pulire = ottieni_percorso_senza_file(output_path)

    # Esegui la funzione per eliminare i file non desiderati
    elimina_file_non_desiderati(cartella_da_pulire, input_filename)
    
if __name__ == "__main__":
    main()
