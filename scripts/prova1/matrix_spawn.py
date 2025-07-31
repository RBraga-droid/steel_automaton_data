import sys
import os
import csv
import random
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
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
##  Funzione per definire il grafo
def graph_spawn(input_filename):
    g = nx.DiGraph()

    # Legge il file CSV e aggiunge gli archi al grafo
    with open(input_filename, mode='r') as input_file:
        reader = csv.DictReader(input_file)
        for row in reader:
            source = row['Partenza']
            target = row['Arrivo']
            if int(row['Peso'])>2:
              g.add_edge(source, target, color=[x / 255 for x in rgb_int2tuple(int(row['Peso'])*1000)], weight=(int(row['Peso'])))

    colors = nx.get_edge_attributes(g,'color').values()
    print(nx.get_edge_attributes(g,'weight').values())
    weights = log_transformator(nx.get_edge_attributes(g,'weight').values())

    #weights = nx.get_edge_attributes(g,'weight').values()
    print(weights)
    n_nodes = len(g.nodes)
    print(n_nodes)
    # Definizione delle posizioni
    pos = {node:(int(node, 16) // 16,int(node, 16) % 16) for node in g.nodes}
    print(pos)
    # Plottaggio immagine
    plt.figure(3,figsize=(60,60))

    nx.draw(g, pos, edge_color=colors, width=3*list(weights), with_labels=True)

    plt.savefig(cambia_estensione(input_filename, ".png"))


def elimina_file_non_desiderati(cartella, file_da_ignorare):
    # Elenco dei file nella cartella
    elenco_file = os.listdir(cartella)

    # Itera su ogni file nella cartella
    for nome_file in elenco_file:
        percorso_file = os.path.join(cartella, nome_file)

        # Verifica se il file è quello da ignorare
        if nome_file == file_da_ignorare:
            print(f"Ignorato il file: {file_da_ignorare}")
            continue

        # Verifica se il file ha un'estensione diversa da .png o .py
        if os.path.isfile(percorso_file) and not (nome_file.endswith('.png') or nome_file.endswith('.py')):
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
    output_path = ottieni_percorso_senza_file(input_file_path)+"\\"+output_filename
    # Il file viene purificato dalle stringhe di controllo del logging process
    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    with open(input_file_path+"_output_"+input_filename, 'w') as file:
        for line in lines:
            if not line.startswith('u'):
                file.write(line)
    
    
    # Il file di testo diventa solo una lista di opcodes
    process_file(input_file_path, output_path)
    # Viene creato il nome per il file .csv
    dumps_csv = cambia_estensione(output_path, ".csv")
    # Generato il file .csv
    generate_csv(output_path, dumps_csv)
    # Genera il grafo
    g = graph_spawn(dumps_csv)

    # Specifica la cartella di destinazione
    cartella_da_pulire = ottieni_percorso_senza_file(input_file_path)

    # Esegui la funzione per eliminare i file non desiderati
    elimina_file_non_desiderati(cartella_da_pulire, input_filename)
    
if __name__ == "__main__":
    main()
