*** Settings ***
Library    SeleniumLibrary
Resource    ../resources/common.robot
Library    DataDriver   ../resources/login.csv
Test Template    Verify invalid username and passwords
Suite Teardown    Close All Browsers
Test Teardown    close browser

*** Variables ***
${ALERT_MSG}=   Could not log you into the system - Username cannot be empty Password cannot be empty


*** Keywords ***
Verify invalid username and passwords
    [Documentation]     method to login to company
    [Arguments]     ${username}     ${password}     ${error_msg}
     Open Browser   ${URL}  ${BROWSER}
     set selenium speed    0.5s
     maximize browser window
     Wait Until Element Is Visible  ${USERNAME_ID}  timeout=5
     Input Text  ${USERNAME_ID}     ${username}
     Input Password  ${PASSWORD_ID}     ${password}
     click button    ${LOGIN_BUTTON_ID}
     alert should be present    ${error_msg}

*** Test Cases ***
Verify logins   ${username}     ${password}     ${error_msg}
    [Tags]    tdd
