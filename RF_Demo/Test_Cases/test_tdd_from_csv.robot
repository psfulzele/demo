*** Settings ***
Library     DataDriver   ../resources/testing.csv
Test Template   Perform Addition

*** Keywords ***

Perform Addition
    [Documentation]    Keyword to perfrom addition of two numbers
    [Arguments]     ${number1}  ${number2}  ${expected_output}
    ${sum}=     Evaluate    int(${number1}) + int(${number2})
    should be equal as integers     ${sum}  ${expected_output}

*** Test Cases ***
Verify Additions of two numbers    ${number1}  ${number2}  ${expected_output}