
*** Settings ***
Library    SeleniumLibrary
Library    OperatingSystem
Library    ../lib/selenium_utility.py

*** Variables ***
${URL}=  https://mycompnay.com/
${USERNAME}=    rfIuser
${PASSWORD}=    Password@123
${USERNAME_ID}=     id:username
${PASSWORD_ID}=     id:password
${BROWSER}=     chrome
${LOGIN_BUTTON_ID}=     id:btn-login
${CLOSE_BUTTON_XPATH}=  xpath://button[text()="Close"]
${LOGS_TAB_XPATH}=  xpath://*[@id="left-nav"]/ul/li[5]/a/span
${LOG_SEARCH_INPUT_TEXT_XPATH}=     //div[@class='ace_scroller']/descendant::div[@class='ace_layer ace_text-layer']
${SEARCH_BUTTON_XPATH}=     xpath://button[contains(@class,'query-button')]
${LOG_SEARCH_TEXT_AREA_XPATH}=  //*[@id="LMOQLEditor"]/textarea
${SEARCH_MOUSE_CLICK_XPATH}=    //div[@class='ace_scroller']
${TIME}=    2
${REFRESH_LOG_PAGE_XPATH}=  //p[contains(text(),'Last update:')]
${COMMON_SLEEP}=    10

*** Keywords ***
Login To Company
    [Documentation]     method to login to company
    [Arguments]     ${TEST_BROWSER}
     Open Browser   ${URL}  ${TEST_BROWSER}
     maximize browser window
     Wait Until Element Is Visible  ${USERNAME_ID}  timeout=${COMMON_SLEEP}
     Input Text  ${USERNAME_ID}     ${USERNAME}
     Input Password  ${PASSWORD_ID}     ${PASSWORD}
     click button    ${LOGIN_BUTTON_ID}
     wait until page contains element   ${CLOSE_BUTTON_XPATH}   ${COMMON_SLEEP}
     click button   ${CLOSE_BUTTON_XPATH}

Go To Logs Tab
    [Documentation]    keywoord to click on logs tab
    wait until element is visible    ${LOGS_TAB_XPATH}    30
    click element    ${LOGS_TAB_XPATH}
    wait_until_element_is_visible    ${LOG_SEARCH_INPUT_TEXT_XPATH}     ${COMMON_SLEEP}


Input Log Search String
    [Documentation]    INput log search string
    [Arguments]    ${SEARCH_QUERY}
     ${element}=    Get WebElement    ${SEARCH_MOUSE_CLICK_XPATH}
     mouse down    ${element}
     sleep    ${TIME}
     INPUT TEXT    ${LOG_SEARCH_TEXT_AREA_XPATH}    ${SEARCH_QUERY}

Click Search Button
    [Documentation]    Click on Search Button
    click element   ${SEARCH_BUTTON_XPATH}
    Sleep   ${COMMON_SLEEP}

Refresh Log Search
    [Documentation]    Keywod to refresh log search
    FOR    ${index}     IN RANGE    5
        click element   ${REFRESH_LOG_PAGE_XPATH}
        Sleep   ${TIME}
    END
