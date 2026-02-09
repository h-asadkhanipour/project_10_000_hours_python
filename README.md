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
This project requires several modules. You have two options:  
    - Option 1 --> use project environment  
    - Option 2 --> install required module in your system  
After installing required modules run `python src/main.py`  

## Option 1 (use project environment)  
You can activate Python environment that contains modules
``` bash
source env/bin/activate
```

``` Powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\env\bin\Activate.ps1
```

## Option 2 (install required modules in your system)
You can install them with requirement.txt file.  
``` bash
pip install -r requirements.txt
```

