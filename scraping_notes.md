# Scraping w/ PlayWright
- Create Virtual Environment
- Install with pip

# Tasks to do
- For every web page, I need to click all to expand hidden row.

# Useful Commands
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

