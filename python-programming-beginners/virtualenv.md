## Virtualenv
Virtualenv permette di creare ambienti di Python isolati al fine di evitare conflitti tra le versioni dei pacchetti e tra le versione dell'interprete Python stesso.

Di seguito una lista dei comandi utili. Si fa riferimento a Python3.

### Aggiornamento PIP (Package manager di Python)
```
python -m pip install --upgrade pip
```

### Creazione ambiente virtuale
```
python3 -m venv tutorial-env
```

### Attivazione dell'ambiente
```
source ./nome_ambiente/bin/activate
```

### Disattivazione dell'ambiente
```
deactivate
```

### Import e export dei pacchetti installati
```
pip install -r requirements.txt --force-reinstall
pip freeze --local > requirements.txt
```
