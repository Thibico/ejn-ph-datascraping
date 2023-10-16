# Wastewater Discharge Permit Dashboard
- [PowerBI Link](https://app.powerbi.com/view?r=eyJrIjoiODNhMDNjYjUtYTcwOC00MmRjLWIxOWItYzVlYzQ5YjVlZWExIiwidCI6ImY2ZjRhNjkyLTQzYjMtNDMzYi05MmIyLTY1YzRlNmNjZDkyMCIsImMiOjEwfQ%3D%3D&pageName=ReportSection)
- Total rows is over 60k. So, PowerBI REST API only allows max-30000 rows per request. So, we've to separate scraping bash scripts into 3 files.
- Running Order of Bash scripts  
    - `wastewater_csv.sh` >> `wastewater_csv_extension.sh` >> `wastewater_csv_extension2.sh`
- To be able to run each bash script , we need to modify Body text files (which is also ordered)
    - `test_csv_body.txt` for 1st bash script
    - `test_csv_body_extension1.txt` for 2nd bash script
    - `test_csv_body_extension2.txt` for 3nd bash script
- The initial results from bash scripts are json files. We used `parse_result_json.py` to convert json into csv files. But each json result had a little bit format changes. So, before we run python script, we need to adjust  `extract_raw_data()` function based on the format of resulted json file.


## Last value in oct15_2nd.json result 
- To use in ext1.txt body

[
    "datetime'2022-02-07T00:00:00'",
    "'Region IV-A'",
    "'Rsa Food Service'",
    "'MCDONALDS NUENO STORE  419'",
    "'IMUS CITY'",
    "'CAVITE'",
    "datetime'2021-02-07T00:00:00'",
    "'Approved'",
    "datetime'2020-05-21T11:35:50'"
    ]

## Another last value in oct15_2nd_extension json result
- To use in ext2.txt body
[
    "datetime'2028-09-26T00:00:00'",
    "'Region XII'",
    "'Precious Child Learning Center, Inc.'",
    "''",
    "'CITY OF KORONADAL (Capital)'",
    "'SOUTH COTABATO'",
    "datetime'2023-09-26T00:00:00'",
    "'Approved'",
    "datetime'2023-07-25T00:59:40'"
    ]