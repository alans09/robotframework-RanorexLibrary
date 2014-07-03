*** Settings ***
#Library    Remote    http://127.0.0.1:8270
Library    Remote    http://192.168.0.103:8270
Suite Teardown    Teardown of suite 
  
*** Keywords ***
Teardown of suite
    Click Element    /form[@processname='charmap']/?/?/button[@accessiblename='Close']

*** Test cases ***
Test of start debug
    Start Debug

Test of Run Application keyword
    Run Application    charmap.exe

Test of Wait For Element keyword
    Wait For Element    /form[@processname='charmap']    10000

Test of Wait For Element Attribute keyword
    Wait For Element Attribute    /form[@processname='charmap']/titlebar[@accessiblerole='TitleBar']    Visible    True    10000

Test of Click Element keyword
    Click Element    /form[@processname='charmap']/text[@controlid='104']

Test of Click Element keyword with location
    Click Element    /form[@processname='charmap']/text[@controlid='104']    location=36,6

Test of Input Text keyword
    Input Text     /form[@processname='charmap']/text[@controlid='104']    hello-world   

Test of Select By Index keyword
    Select By Index    /form[@processname='charmap']/combobox[@controlid='105']    5

Test of Check and Get Element Attribute keywords
    Check    	/form[@processname='charmap']/checkbox[@accessiblekeyboardshortcut='Alt+v']
    ${res} =     Get Element Attribute    /form[@processname='charmap']/checkbox[@accessiblekeyboardshortcut='Alt+v']    Checked
    Should Be True    ${res}

Test of Uncheck and Get Element Attribute keywords
    Uncheck    /form[@processname='charmap']/checkbox[@accessiblekeyboardshortcut='Alt+v']
    ${res} =     Get Element Attribute    /form[@processname='charmap']/checkbox[@accessiblekeyboardshortcut='Alt+v']    Checked
    Should Not Be True    ${res}

Test of Check If Process Is Running keyword
    Check If Process Is Running    charmap.exe

Test of Wait For Process To Start keyword
    Wait For Process To Start    charmap.exe    10000

Test of Clear Text keyword
    Clear Text    /form[@processname='charmap']/text[@controlid='104']
    ${res} =    Get Element Attribute    /form[@processname='charmap']/text[@controlid='104']    Text

Test of Double Click Element keyword
    Double Click Element    /form[@processname='charmap']/text[@controlid='104']

Test of Double Click Element keyword with location
    Double Click Element    /form[@processname='charmap']/text[@controlid='104']    location=36,5

Test of Right Click Element keyword
    Right Click Element    /form[@processname='charmap']/text[@controlid='104']

Test of Right Click Element keyword with location
    Right Click Element    /form[@processname='charmap']/text[@controlid='104']    location=36,5

Test of Run Application With Parameters keyword
    Run Application With Parameters    notepad.exe    test.txt
    Wait For Element    /form[@processname='notepad']/text[@text~'test.txt']    5000
 
Test of Send Keys keyword
    Send Keys    /form[@processname='notepad']    {Alt down}{NKey}{Alt up}
    Click Element    /form[@processname='notepad']/?/?/button[@accessiblename='Close']

Test of Run Script keyword
    ${res} =    Run Script     example/echoonly.bat
    Should Be Equal    ${res['stdout']}    hello world

Test of Run Script With Parameters keyword
    ${res} =    Run Script With Parameters    example/echoinput.bat    hello
    Should Be Equal    ${res['stdout']}    hello

Test of Take Screenshot keyword
    ${res} =    Take Screenshot    /form[@processname='charmap']
    Should Contain    ${res}   AAAA 

Test of Kill Process keyword
    Run Application     notepad.exe
    ${res}=    Kill Process    notepad.exe
    Should Be True    ${res}
