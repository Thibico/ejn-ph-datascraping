# PowerBI Dashboards Scraping
## Wastewater Discharge Permit
- More detailed documentation - [Note](./powerbi_scraping/wastewater_scraping_note.md)

## Projected Waste Generation
- To scrape data from PowerBI [Dashboard](https://app.powerbi.com/view?r=eyJrIjoiNjc4OTE2OTktMDdhMC00YzM1LTkwMjEtYWUxMDIyMjI0MWMwIiwidCI6ImY2ZjRhNjkyLTQzYjMtNDMzYi05MmIyLTY1YzRlNmNjZDkyMCIsImMiOjEwfQ%3D%3D&pageName=ReportSection&fbclid=IwAR264Sfm3ocnSBovLnpGgdSKXljXQeGAx9JpZIxcAS3YyV4voqVpHzPTBNw)
- PowerBI has POST api to pull the data. So, we need to use bash script to scrape.

- Give permission to run bash file
```cmd
chmod +x bash_filename.sh
```

- Command to run bash
```cmd
sh final_aste_scraping.sh
```

## Result parsing w/ Python
- PowerBI api result is nested JSON structure and it's quite complex. We need to parse it using Python.

*****

# Scraping data for Philippines Port Authority website
- Create Virtual Environment
- Install with pip
- Initially planned to use to scrape PPA website with playwright , but no need it anymore. Worked with requests + bs4.

## Tasks to do
- For every web page, I need to click all to expand hidden row.

## Useful Commands
```
pip3 install playwright
```
- Create a folder to store browser packages and install firefox.

```cmd
PLAYWRIGHT_BROWSERS_PATH=./pw_browsers python -m 
playwright install firefox
```

- Playwright Codegen w/ custom Firefox

```cmd
PLAYWRIGHT_BROWSERS_PATH=./pw_browsers python3 -m playwright codegen https://ppp.gov.ph/project-database/ -b firefox
```

- Run Python script with custom browser

```cmd
PLAYWRIGHT_BROWSERS_PATH=./pw_browsers python3 scraping_ppa.py
```

