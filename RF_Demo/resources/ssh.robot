*** Settings ***
Library    ../lib/ssh_library.py    ssh
Library    String
*** Variables ***
${host}=    10.55.3.153
${ssh_username}=    root
${ssh_password}=    lmqa@098

*** Keywords ***

connect to linux device
    [Documentation]    Keyword to connect to Linux Device using ssh
     ${client}=     create_ssh_connection   ${host}     ${ssh_username}     ${ssh_password}
    log    ${client}

generate syslog logs
    [Documentation]    Method to generate syslog log using logger utility
    [Arguments]    ${message}
    FOR    ${index}     IN RANGE    5
        ${random}=  Generate Random String
        ${result}=  execute command    logger ${message}_${random}:${index}
        log    ${result}
    END
