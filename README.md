# Instruccions for use

### Clone the repository
```git clone https://github.com/ruteru/cluster_db.git```

### Create venv
```python3 -m venv venv```

### Activate venv
```venv/scripts/activate```

### install requirements
```pip install -r requirements.txt```

### run to test locally:
```python users_db.py```

### replace host and port by cluster ip and cluster port
```kubectl get svc proxysql```

### run on the cluster network
```kubectl run -i --tty --rm debug --image=ubuntu -- bash```
```telnet proxysql 6033```