import re

def aggiorna_ontologia(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        linee = f.readlines()

    # Conserviamo le prime 242 linee
    testata = linee[:242]
    resto = "".join(linee[242:])

    # 1. Identifichiamo i blocchi che iniziano con ###
    blocchi = re.split(r'(###\s+https://w3id\.org/emmo/domain/neo#)', resto)
    
    mappa_nomi = {}
    
    # 2. Primo passaggio: estrazione ID e prefLabel
    # Cerchiamo l'URL completo della prefLabel come nel tuo esempio
    pattern_label = re.compile(r'<http://www\.w3\.org/2004/02/skos/core#prefLabel>\s+"([^"]+)"')

    for i in range(1, len(blocchi), 2):
        contenuto_blocco = blocchi[i+1]
        
        # L'ID è la prima stringa alfanumerica dopo i ### (che sono in blocchi[i])
        # Ma lo prendiamo più stabilmente dal corpo del blocco dopo i due punti ':'
        match_id = re.search(r':([a-zA-Z0-9]{10,})', contenuto_blocco)
        match_label = pattern_label.search(contenuto_blocco)
        
        if match_id and match_label:
            vecchio_id = match_id.group(1)
            nuova_label = match_label.group(1).replace(" ", "_")
            mappa_nomi[vecchio_id] = nuova_label
            print(f"Trovato: {vecchio_id} -> {nuova_label}")

    # 3. Secondo passaggio: Sostituzione globale nel testo dopo riga 242
    testo_modificato = resto
    
    # Ordiniamo per lunghezza decrescente per evitare sostituzioni parziali
    for vid in sorted(mappa_nomi.keys(), key=len, reverse=True):
        nid = mappa_nomi[vid]
        # Sostituiamo l'ID quando è nei commenti ###
        testo_modificato = testo_modificato.replace(f'neo#{vid}', f'neo#{nid}')
        # Sostituiamo l'ID quando è usato come prefisso :ID
        testo_modificato = testo_modificato.replace(f':{vid}', f':{nid}')

    # 4. Salvataggio
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(testata)
        f.write(testo_modificato)

    print(f"\nFine! Processate {len(mappa_nomi)} classi.")

# Avvia lo script
aggiorna_ontologia('neo.ttl', 'neo_aggiornato.ttl')
