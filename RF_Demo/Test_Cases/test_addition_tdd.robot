*** Settings ***
Library    BuiltIn
Test Template   Perform Addition

*** Keywords ***

Perform Addition
    [Documentation]    Keyword to perform addition of two numbers
    [Arguments]     ${number1}  ${number2}  ${expected_outpur}
    ${sum}=     Evaluate    int(${number1}) + int(${number2})
    should be equal as integers     ${sum}  ${expected_outpur}

*** Test Cases ***      NUMBER1     NUMBER2     SUM
Add possitive Numbers   10  20      30
    [Tags]    tdd
Add negative Numbers   -10  -20    -30
    [Tags]    tdd
Add positive and negative   10  -20     -10
    [Tags]    tdd