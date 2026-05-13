*** Settings ***
Library    OperatingSystem

*** Test Cases ***
Citeste fisier
    ${content}=    Get File    data.txt
    Log    ${content}
