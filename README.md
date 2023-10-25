# README #

### What is this repository for? ###

* Quick summary
* Version

### How do I get set up? ###

* Summary of set up
1. Generar nuestro entorno virtual
* Windows
  + python3 -m venv env 
* Mac Linux
  + python3 -m venv env 
2. Activar el entorno virtual
* Windows
  + env\Scripts\activate
* Mac Linux
  + source env/bin/activate
3. Actualizar pipi y setup tools
  + pip3 install -U pip
  + pip3 install -U setuptools

4. Ejecucion de la API 
* uvicorn main:app --reload --port 8081 --host 0.0.0.0