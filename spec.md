# version 2 specifications  

## List of what I want to change  

- streamlit doesn't take float numbers as study hours  
- program runs slowly  
- each day sould be assigned only once a day (append was not a good idea)
- days that are holiday should be omitted from calculations  
- add slqlite database along with xlsx file for better performance
- if database appraoch is faster, add option to update xlsx file accourding to database  
- start development in a new branch and them merge it  
- if yesterday doesn't have any reports, ask for yesterday at first and save it  
- add tag to this version and then start next version  
- add test to program to test if program is intact

## v3.0.0 what I want to change  

- organize project in more standard form

- rewrite README.md  
  - move v1 source code to another directory
  - explain what is v1 and what is v2

- add env/ to gitignore  

- add class for reviewing weekly reports in nice format --> in CLI  

- take todays report separate than several days report  

- add modifying report option  

- extract report to excel file option

- rename database.db to daily_report.sqlite  

- rename daily_time_log.xlsx to daily_report.xlsx  

- move json file from reports to data and rename data to reports_data  

- add some test to check if programs is fine  

- add more docstring to source codes  
