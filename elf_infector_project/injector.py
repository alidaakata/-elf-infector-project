import struct

# Adresse de la fonction malveillante secretFunction du bufferoverfow
new_entry_point = 0x401146  # Adresse de secretFunction

# Offset de la section .text (obtenu avec `readelf -S vuln64`)
offset_text_section = 0x401060  # L'offset de la section .text

# Ouvre le fichier ELF vulnérable en mode lecture-écriture binaire
with open('vuln64', 'r+b') as f:
    # Injecte du code malveillant à l'offset de la section .text
    f.seek(offset_text_section)
    # Remplacer par des NOPs (ici 4 octets) pour ne pas perturber le programme
    #f.write(b"\x90\x90\x90\x90\x90")  # NOP sled 
    f.write(b"\x90" * 100)  # NOP sled plus grand
    # Modifie l'entry point du programme pour pointer vers la fonction malveillante
    f.seek(0x18)  # L'entry point est à l'offset 0x18 dans l'en-tête ELF
    f.write(struct.pack('<Q', new_entry_point))  # Écrire l'adresse de l'entry point modifié
#affichage simple
    print("Injection réussie !")

