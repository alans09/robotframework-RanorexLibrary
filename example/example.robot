*** Settings ***
Library    Remote    http://127.0.0.1:8270    WITH NAME    remote
Library    HelperModule 

*** Keywords ****
Run notepad and input text hello-world
    Run Application    notepad.exe    
    Click Element    /form[@title='Untitled - Notepad']/text[@controlid='15']
    Wait For Element    /form[@title='Untitled - Notepad']/text[@controlid='15']    10000
    Wait For Element Attribute    /form[@title='Untitled - Notepad']/titlebar    Text    Untitled\ -\ Notepad    10000
    Input Text    /form[@title='Untitled - Notepad']/text[@controlid='15']    hello-world
    Double Click Element    /form[@title='Untitled - Notepad']/text[@controlid='15']
    Right Click Element   /form[@title='Untitled - Notepad']/text[@controlid='15']

Check if ${titlebar_arg} in header is ${expected_value}
    ${title} =    Get Element Attribute    /form[@title='Untitled - Notepad']/titlebar    ${titlebar_arg}
    Should Be Equal    ${title}    ${expected_value}

Click close and not save
    Click Element    /form[@title='Untitled - Notepad']/?/?/button[@accessiblename='Close']
    Click Element    /form[@processname='notepad']//button[@text='Do&n''t Save' or @text='&No']

Load json from file    [Arguments]    ${path_to_json}
    ${json} =    Load Json File    ${path_to_json} 
    Log    ${json}

Run application ${browser} with parameters ${page}
    Log    ${browser}
    Log    ${page}
    Run Application With Parameters    ${browser}    ${page}
    Click Element    /form[@title='Google - Mozilla Firefox']/?/?/button[@accessiblename='Close']

Take screenshot and save it localy
    ${screen} =    Take Screenshot    /form[@title='Untitled - Notepad']
    Save Base64 Screenshot    ${screen}    saved.png

Run script on remote machine    [Arguments]    ${script_path}
    ${res} =    Run Script    ${script_path}
    Log    ${res['stdout']}
    Log    ${res['stderr']}

Run script with parameters on remote machine    [Arguments]    ${script_path}    ${arguments}
    ${res} =    Run Script With Parameters    ${script_path}    ${arguments}
    Log    ${res['stdout']}
    Log    ${res['stderr']}

Test of check function 
    Run Application    charmap.exe
    Check    /form[@title='Character Map']/checkbox[@text='Ad&vanced view']
    ${res} =    Get Element Attribute    /form[@title='Character Map']/checkbox[@text='Ad&vanced view']    Checked
    ${res} =    Convert To String    ${res}
    Should Be Equal    ${res}    True 

Test of uncheck function
    Uncheck    /form[@title='Character Map']/checkbox[@text='Ad&vanced view']
    ${res} =    Get Element Attribute    /form[@title='Character Map']/checkbox[@text='Ad&vanced view']    Checked
    ${res} =    Convert To String    ${res}
    Should Be Equal    ${res}    False
    Click Element    /form[@processname='charmap' and @class='#32770' and @instance='1']/?/?/button[@accessiblename='Close']



*** Test case ***
Basic notepad work
    Run notepad and input text hello-world
    Check if Text in header is Untitled\ -\ Notepad

Save screenshot of notepad
    Take screenshot and save it localy

Close notepad    
    Click close and not save

Load json file from disk
    Load json from file    test_data.json

Start firefox on page google.sk
    Run application firefox.exe with parameters www.google.sk

Check of run script keyword
    Run script on remote machine    EchoOnly.bat

Check of run script with parameters keyword
    Run script with parameters on remote machine    EchoInput.bat    hello world parameters 

Micro test of check function
    Test of check function

Micro test of uncheck function
    Test of uncheck function

