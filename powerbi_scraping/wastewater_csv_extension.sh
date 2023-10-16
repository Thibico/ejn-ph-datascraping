curl 'https://wabi-east-asia-a-primary-api.analysis.windows.net/public/reports/querydata?synchronous=true' \
  -H 'Connection: keep-alive' \
  -H 'Pragma: no-cache' \
  -H 'Cache-Control: no-cache' \
  -H 'sec-ch-ua: "Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36' \
  -H 'ActivityId: d0a0e7e4-00e9-43da-9655-6f70f5882fde' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'RequestId: 9d5f1252-0e65-d66d-61cb-637c2537b710' \
  -H 'X-PowerBI-ResourceKey: 83a03cb5-a708-42dc-b19b-c5ec49b5eea1' \
  -H 'Content-Type: application/json;charset=UTF-8' \
  -H 'Origin: https://app.powerbi.com' \
  -H 'Sec-Fetch-Site: cross-site' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Referer: https://app.powerbi.com/' \
  -H 'Accept-Language: en-US,en;q=0.9' \
  -H 'dnt: 1' \
  -H 'sec-gpc: 1' \
  --data-binary "@test_csv_body_extension1.txt" \
  --compressed | sed 's/"jobIds":\[[^]]*\],//g' | sed 's/"jobId":"[^"]*",//g' | sed 's/"rootActivityId":"[^"]*",//g' | sed 's/"timestamp":"[^"]*",//g' | jq '.' > "./json_files/wastewater_oct15_2nd_extension.json"