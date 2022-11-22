*** Settings ***
Library    SeleniumLibrary
Resource    ../resources/common.robot
Resource    ../resources/ssh.robot
Suite Setup    Set Selenium speed   0.5s
Test Setup      Login To Company    ${BROWSER}
Test Teardown   close browser

*** Variables ***

*** Test Cases ***
Log Search With Log Seacrch String
    [Documentation]     Log search with search string
    [Teardown]  close browser
    [Tags]    smoke
    connect to linux device
    generate syslog logs    robot framework demo
#    Login To Company    ${BROWSER}
    Go To Logs Tab
    Input Log Search String     "robot framework"
    Click Search Button
    Refresh Log Search