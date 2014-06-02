""" Remote ranorex library for robot framework
Implemented keywords:
    Click Element -> Click on element identified by xpath
    Check -> If checkbox/radiobutton is checked, do nothing else check
    Double Click Element -> Double clicks on element identified by xpath
    Get Element Attribute -> Gets desired attribute of element identified
        by xpath
    Input Text -> Inputs desired text into element identified by xpath
    Right Click Element -> Right click on element identified by xpath
    Run Application -> Starts application
    Run Application With Parameters -> Start application with added parameters
    Run Script -> Run script and return {'stdout':'<stdout>',
        'stderr':'<stderr>'}
    Run Script With Parameters -> Run script with parameters
        and returns {'stdout':'<stdout>', 'stderr':'<stderr>'}
    Select By Index -> Select value from combobox according to index
    Take Screenshot -> Takes screenshot of desired element identified by xpath
        and returns base64 encoded string
    Uncheck -> Checks if radiobutton/checkbox is checked.. if so it uncheck it
    Wait For Element -> Waits for desired element for desired time
    Wait For Element Attribute -> Waits for specified attribute of desired
        element
"""
import clr
clr.AddReference('Ranorex.Core')
clr.AddReference('System.Windows.Forms')
import System.Windows.Forms
import Ranorex
import sys
import os
sys.path.append(os.path.abspath('..'))
from src.robotremoteserver import RobotRemoteServer


class RanorexLibrary(object):
    """ Basic implementation of ranorex object calls for
    robot framework
    """
    @classmethod
    def __return_type(cls, locator):
        """ Function serves as translator from xpath into
        .net object that is recognized by ranorex.
        Inputs:
            locator -> xpath to element
        Output:
            string with .net object type
        """
        supported_types = ['AbbrTag', 'AcronymTag', 'AddressTag', 'AreaTag',
                           'ArticleTag', 'AsideTag', 'ATag', 'AudioTag',
                           'BaseFontTag', 'BaseTag', 'BdoTag', 'BigTag',
                           'BodyTag', 'BrTag', 'BTag', 'Button',
                           'ButtonTag', 'CanvasTag', 'Cell', 'CenterTag',
                           'CheckBox', 'CiteTag', 'CodeTag', 'ColGroupTag',
                           'ColTag', 'Column', 'ComboBox', 'CommandTag',
                           'ContextMenu', 'DataListTag', 'DdTag', 'DelTag',
                           'DetailsTag', 'DfnTag', 'DirTag', 'DivTag',
                           'DlTag', 'EmbedTag', 'EmTag', 'FieldSetTag',
                           'FigureTag', 'FontTag', 'Form', 'FormTag',
                           'Link', 'List', 'ListItem', 'MenuBar',
                           'MenuItem', 'Picture', 'ProgressBar',
                           'RadioButton', 'Row', 'ScrollBar', 'Slider',
                           'StatusBar', 'Text', 'TitleBar', 'ToggleButton',
                           'Tree', 'TreeItem', 'Unknown']
        splitted_locator = locator.split('/')
        if "[" in splitted_locator[-1]:
            ele = splitted_locator[-1].split('[')[0]
        else:
            ele = splitted_locator[-1]
        for item in supported_types:
            if ele.lower() == item.lower():
                return item
            elif ele.lower() == '':
                raise AssertionError("No element entered")
        raise AssertionError("Element is not supported. Entered element: %s" %
                             ele)

    def click_element(self, locator):
        """ Clicks on element located on location.
        Inputs:
            locator ->  xpath to object
        Output:
            Nothing if success, else RanorexException raised
        """
        element = self.__return_type(locator)
        getattr(Ranorex, element)(locator).Click()

    def check(self, locator):
        """ Check if element is checked. If not it check it
        Inputs:
            locator -> xpath to object
        Output:
            Nothing if success
            If other element than CheckBox / RadioButton error
            else RanorexException
        """
        element = self.__return_type(locator)
        if element == 'CheckBox' or element == 'RadioButton':
            obj = getattr(Ranorex, element)(locator)
            if not obj.Element.GetAttributeValue('Checked'):
                obj.Click()
        else:
            raise AssertionError("Element |%s| is not supported for checking" %
                                 element)

    def clear_text(self, locator):
        """ Clears text from text box. Only element Text is supported.
        Inputs:
            locator -> xpath to object
        Output:
            Nothing if ok
            AssertionError if not supported element
            else RanorexException
        """
        element = self.__return_type(locator)
        if element != "Text":
            raise AssertionError("Only element Text is supported!")
        else:
            obj = getattr(Ranorex, element)(locator)
            obj.PressKeys("{End}{Shift down}{Home}{Shift up}{Delete}")

    def double_click_element(self, locator):
        """ Doubleclick on element identified by xpath.
        Inputs:
            locator -> xpath to object
        Output:
            Nothing if success
            else RanorexException
        """
        element = self.__return_type(locator)
        getattr(Ranorex, element)(locator).DoubleClick()

    def get_element_attribute(self, locator, attribute):
        """ Get specified element attribute.
        Inputs:
            locator -> xpath to object
            attribute -> attribute to get
        Outputs:
            If attribute exists output its value
            else RanorexException"""
        element = self.__return_type(locator)
        obj = getattr(Ranorex, element)(locator)
        return obj.Element.GetAttributeValue(attribute)

    def input_text(self, locator, text):
        """ input texts into specified locator.
        Inputs:
            locator -> xpath to object
            text -> text to enter
        Outputs:
            Nothing if success
            else RanorexException
        """
        element = self.__return_type(locator)
        getattr(Ranorex, element)(locator).PressKeys(text)

    def right_click_element(self, locator):
        """ Rightclick on desired element.
        Inputs:
            locator -> xpath to object
        Outputs:
            Nothing if success
            else RanorexException
        """
        element = self.__return_type(locator)
        obj = getattr(Ranorex, element)(locator)
        obj.Click(System.Windows.Forms.MouseButtons.Right)

    @classmethod
    def run_application(cls, app):
        """ Runs local application.
        Inputs:
            app -> application to start (path to it)
        Outputs:
            nothing if success
            else RanorexException
        """
        Ranorex.Host.Local.RunApplication(app)

    @classmethod
    def run_application_with_parameters(cls, app, params):
        """ Runs local application with parameters.
        Inputs:
            app -> application to start
            params -> parameters for this application
        Outputs:
            Nothing if success
            else RanorexException
        """
        Ranorex.Host.Local.RunApplication(app, params)

    @classmethod
    def run_script(cls, script_path):
        """ Runs script on remote machine and returns stdout and stderr.
        Inputs:
            script_path -> path to script on local harddisk
        Outputs:
            dictionary {'stdout':<stdout>, 'stderr':<stderr>}
        """
        import subprocess
        process = subprocess.Popen([script_path],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        output = process.communicate()
        return {'stdout':output[0], 'stderr':output[1]}

    @classmethod
    def run_script_with_parameters(cls, script_path, params):
        """ Runs script on remote machine and returns stdout and stderr.
        Inputs:
            script_path -> path to script on local harddisk
            params -> parameters to it
        Outputs:
            dictionary {'stdout':<stdout>, 'stderr':<stderr>}
        """
        import subprocess
        process = subprocess.Popen([script_path, params],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        output = process.communicate()
        return {'stdout':output[0], 'stderr':output[1]}

    def select_by_index(self, locator, index):
        """ Selects item from combobox according to index.
        Inputs:
            locator -> xpath to object
            index -> index in combobox
        Outputs:
            Nothing if success
            else RanorexException
        """
        element = self.__return_type(locator)
        obj = getattr(Ranorex, element)(locator)
        selected = obj.Element.GetAttributeValue("SelectedItemIndex")
        diff = int(selected) - int(index)
        if diff >= 0:
            for _ in range(0, diff):
                obj.PressKeys("{up}")
        elif diff < 0:
            for _ in range(0, abs(diff)):
                obj.PressKeys("{down}")
        return diff

    @classmethod
    def send_keys(cls, locator, key_seq):
        """ Send key combination to specified element.
        Also it gets focus before executing sequence
        seq according to :
        http://msdn.microsoft.com/en-us/library/system.windows.forms.keys.aspx
        Inputs:
            locator -> xpath to object
            key_seq -> key sequence e.g. {Control down}{SKey}{Control up}
        Output:
            Nothing if success
            else RanorexException
        """
        Ranorex.Keyboard.PrepareFocus(locator)
        Ranorex.Keyboard.Press(key_seq)

    def set_focus(self, locator):
        """ Sets focus on desired location.
        Inputs:
            locator -> xpath to object
        Outputs:
            True if focus is set 
            else RanorexException
        """
        element = self.__return_type(locator)
        obj = getattr(Ranorex, element)(locator)
        obj.Focus()
        return obj.HasFocus

    def take_screenshot(self, locator):
        """ Takes screenshot and return it as base64.
        Inputs:
            locator -> xpath to object
        Outputs:
            base64string if success
            else RanorexException
        """
        element = self.__return_type(locator)
        obj = getattr(Ranorex, element)(locator)
        img = obj.CaptureCompressedImage()
        return img.ToBase64String()

    def uncheck(self, locator):
        """ Check if element is checked. If yes it uncheck it
        Inputs:
            locator -> xpath to object
        Output:
            Nothing if success
            Error not supported element if other than CheckBox/RadioButton
            else RanorexException
        """
        element = self.__return_type(locator)
        if element == 'CheckBox' or element == 'RadioButton':
            obj = getattr(Ranorex, element)(locator)
            if obj.Element.GetAttributeValue('Checked'):
                obj.Click()
        else:
            raise AssertionError("Element |%s| not supported for unchecking"
                                 % element)

    @classmethod
    def wait_for_element(cls, locator, timeout):
        """ Wait for element becomes on the screen.
        Inputs:
            locator -> xpath to object
            timeout -> timeout in ms to wait
        Outputs:
            Element <name> exists if success
            else RanorexException
        """
        Ranorex.Validate.EnableReport = False
        if Ranorex.Validate.Exists(locator, int(timeout)):
            return 'Element %s exists' % locator

    def wait_for_element_attribute(self, locator, attribute,
                                   expected, timeout):
        """ Wait for element attribute becomes requested value.
        Inputs:
            locator -> xpath to object
            attribute -> object attribute
            expected -> expected value of attribute
            timeout -> timeout in ms to wait for object
        Outputs:
            True if success
            FAIL if not found
            else RanorexException
        """
        import time
        curr_time = 0
        timeout = int(timeout)/1000
        while curr_time != timeout:
            value = self.get_element_attribute(locator, attribute)
            if str(value) == str(expected):
                return True
            time.sleep(1)
            curr_time += 1
        return 'FAIL'


if __name__ == '__main__':
    RobotRemoteServer(RanorexLibrary(), *sys.argv[1:])
