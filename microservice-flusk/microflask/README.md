## Guida

### 1. Init virtual environment
```python
python3 -m venv venv
```

### 2. Setup project
```python
pip install -e .
```

### 3. Install requirements
```
pip install -r requirement.txt
```

### 4. Build image
```
docker image build -f DOCKERFILE -t python-container .
```

### 5. Run container
```
docker run -d -p 5000:5000 --name istanza-python python-container
```
In alternativa meglio usare docker-compose

### 6. Files & folders
* **wsgi.py**: Il file python che viene utilizzato per avviare l'api
* **requirement.txt**: contiene il riferimento a tutte le librerie necessarie per la corretta esecuzione del programma
* **settings.py**: viene utilizzato per centralizzare tutti i parametri di configurazione in un unico punto
* **setup.py**: file per la configurazione del progetto python
* **dockerfile**: file necessario per eseguire la build dell'immagine
* **dockerignore**: file e cartelle che vengono escluse dalla Docker Build image
* **wsgi.ini**: file di configurazione per eseguire uwsgi
* **app/**: la cartella contiene tutte le logiche del programma

### uWSGI configuration
* **wsgi-file** = : indica il file che contiene l'istruzione di avvio del web server
* **callable=app**: indica l'oggeto che avvia il web server
* **enable-threads=true**: abilita il mult
* **http=:6001**: indica il protocollo e i dettagli dell'host su cui i gateway è in ascolto. Un'opzione alternativa e più efficiente è **socket**
* **processes=1**: indica il numero di processi allocati al gateway 
* **threads=4**: indica il numero di thread allocati al gateway
* **master=true**: permette di accedere alla memoria dei workers e per eseguire il rispettivo caricamento. (Opzione consigliata)
* **vacuum=true**: elimina le socket quando uwsgi viene arrestato
* **die-on-term=true**: arresta wsgi quando viene ricevuto il segnale SIGTERM

### Comandi utili docker
```
docker container ls
docker container rm
docker images 
docker rmi {image id}
```
