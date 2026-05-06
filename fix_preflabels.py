import re

def separa_camel_case(testo):
    """
    Inserisce uno spazio prima di ogni lettera maiuscola, 
    evitando di aggiungere spazi all'inizio.
    Esempio: "NuclearPowerPlant" -> "Nuclear Power Plant"
    """
    # Regex: trova una minuscola seguita da una maiuscola
    res = re.sub(r'([a-z])([A-Z])', r'\1 \2', testo)
    # Gestisce anche casi come "NPPNormal" -> "NPP Normal"
    res = re.sub(r'([A-Z])([A-Z][a-z])', r'\1 \2', res)
    return res.strip()

def formatta_labels_ontologia(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        linee = f.readlines()

    # Manteniamo intatta la testata (prime 242 righe)
    testata = linee[:242]
    corpo = "".join(linee[242:])

    # Regex per catturare prefLabel e altLabel (sia in formato breve che URL)
    # Cerca: predicato + spazio + virgoletta + contenuto + virgoletta
    pattern = re.compile(
        r'((?:skos:prefLabel|skos:altLabel|<http://www\.w3\.org/2004/02/skos/core#(?:prefLabel|altLabel)>)\s+")([^"]+)(")'
    )

    def trasforma_match(match):
        predicato_e_apertura = match.group(1) # es: skos:prefLabel "
        testo_label = match.group(2)           # es: NuclearPowerPlant
        chiusura = match.group(3)             # es: "
        
        # Applichiamo la separazione CamelCase e puliamo eventuali underscore
        label_pulita = separa_camel_case(testo_label.replace("_", " "))
        
        return f"{predicato_e_apertura}{label_pulita}{chiusura}"

    # Applichiamo la trasformazione a tutto il corpo
    corpo_modificato = pattern.sub(trasforma_match, corpo)

    # Salvataggio
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(testata)
        f.write(corpo_modificato)

    print(f"Sistemazione completata! File salvato in: {output_file}")

# Esecuzione
formatta_labels_ontologia('neo.ttl', 'neo_final.ttl')
