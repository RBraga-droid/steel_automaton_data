with open('sample-20200604.exe_231129_131856.dmp', 'rb') as file:
    # Imposta l'offset e la lunghezza in base ai tuoi dati di interesse
    offset = 0x00400000
    length = 100

    # Posizionati nell'offset specificato
    file.seek(offset)

    # Leggi i dati e salvali in un file di testo
    data = file.read(length)
    with open('output.txt', 'w') as output_file:
        output_file.write(data.decode('utf-8'))
