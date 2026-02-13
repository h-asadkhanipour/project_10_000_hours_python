# 10,000 hours Python project  

I want to make a python program with dashboard that can record my python studying and practicing time.  
Ofcourse its not for perfectionism, Its main purpose is to halp me to have claritiy and record of my progress.  

## Features that I want to have in this program:  
- have a database for my study record, maybe a excel file or csv file
- automatically save itself in git  
- show a estimate of day that I will acheive this 10_000 hours goal (based on my history)  
- show a calender that I can see my past activity  
- every day I can give one or more updates
- if previous day I didn't work, ask me to explain why I was away (also save this information in json file)  
- show a progress bar that I have acheive for example 50 percent of my goal  
- have env directory for required modules (run every where)


# How to run:  
You can this project in CLI and with streamlit dashboard. 
After installing required modules and activating env:
- Run in CLI `python src/main.py`  
- Run in terminal `streamlit run src/streamlit_app.py`

This project requires several modules. You have two options to install third-party packages:  
    - Option 1 --> use Python environment manager
    - Option 2 --> use Conda environment manager

## Option 1 (use Python environment manager)  
- 1 create new environment `python -m venv env`  
- 2 activate project enviromnet:(you should see (env) in left side of your terminal)
for unix users:  
``` bash
source env/bin/activate
```
for windows power shell users:  
``` Powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\env\bin\Activate.ps1
```
- 3 install required modules `pip install -r requirements.txt`  
## Option 2 (use Conda environment manager)
- 1 create new enviroment `conda create -n env`  
- 2 activate conda environment `conda actiavte env`  
- 3 install required modules `pip install -r requirements.txt`  
