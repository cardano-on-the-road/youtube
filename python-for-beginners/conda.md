
## COS'E' ANACONDA
Anaconda è una distribuzione gratuita e open source dei linguaggi di programmazione Python e R per il calcolo scientifico, che mira a semplificare la gestione dei pacchetti, l'isolamento degli ambienti e la relativa distribuzione.



## COMANDI PRINCIPALI ANACONDA


### Creazione di un ambiente
```
conda create --name nome_ambiente
```

### Attivazione e selezione di un ambiente
```
conda activate nome_ambiente
```

### Disattivazione di Anaconda
```
conda deactivate
```

### Lista ambienti installati
```
conda info --envs
```

### Eliminazione ambiente
```
conda env remove --name nome_ambiente
```

### Esportazione dei pacchetti installati
```
conda env export > conda_environment.yml
```

### Creazione di un nuovo ambiente a partire da un'esportazione precedente
```
conda env create -f conda_environment.yml
```

Più informazioni sono disponibili a questo [Link](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
