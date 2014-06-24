"""
    Remote ranorex library for robot framework
    All commands return True if they are executed correctly
"""
#iron python imports
import clr
clr.AddReference('Ranorex.Core')
clr.AddReference('System.Windows.Forms')
import System.Windows.Forms
import Ranorex
#python imports
import sys
import subprocess
import time
from robotremoteserver import RobotRemoteServer


class RanorexLibrary(object):
    """ Basic implementation of ranorex object calls for
    robot framework
    """
    @classmethod
    def __return_type(cls, locator):
        """ Function serves as translator from xpath into
        .net object that is recognized by ranorex.
        Returns supported object type.
        """
        Ranorex.Validate.EnableReport = False
        Ranorex.Adapter.DefaultUseEnsureVisible = True
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

    def click_element(self, locator, location=None):
        """ Clicks on element identified by locator and location
        """
        element = self.__return_type(locator)
        try:
            if location == None:
                getattr(Ranorex, element)(locator).Click()
                return True
            else:
                if not isinstance(location, basestring):
                    raise AssertionError("Location must be a string")
                location = [int(x) for x in location.split(',')]
                ele = getattr(Ranorex, element)(locator)
                ele.Click(Ranorex.Location(location[0], location[1]))
                return True
        except Exception as error:
            raise AssertionError(error)

    def check(self, locator):
        """ Check if element is checked. If not it check it.
            Only checkbox and radiobutton are supported.
            Uses Click() method to check it.
        """
        element = self.__return_type(locator)
        if element == 'CheckBox' or element == 'RadioButton':
            obj = getattr(Ranorex, element)(locator)
            if not obj.Element.GetAttributeValue('Checked'):
                obj.Click()
                return True
        else:
            raise AssertionError("Element |%s| is not supported for checking" %
                                 element)

    @classmethod
    def check_if_process_is_running(cls, process_name):
        """ Check if process with desired name is running.
            Returns name of process if running
        """
        proc = subprocess.Popen(['tasklist'], stdout=subprocess.PIPE)
        out = proc.communicate()[0]
        return out.find(process_name) != -1 if out else False

    def clear_text(self, locator):
        """ Clears text from text box. Only element Text is supported.
        """
        element = self.__return_type(locator)
        if element != "Text":
            raise AssertionError("Only element Text is supported!")
        else:
            obj = getattr(Ranorex, element)(locator)
            obj.PressKeys("{End}{Shift down}{Home}{Shift up}{Delete}")
            return True
        raise AssertionError("Element %s does not exists" % locator) 

    def double_click_element(self, locator, location=None):
        """ Doubleclick on element identified by locator. It can click
            on desired location if requested.
        """
        element = self.__return_type(locator)
        try:
            if location == None:
                getattr(Ranorex, element)(locator).DoubleClick()
                return True
            else:
                if not isinstance(location, basestring):
                    raise AssertionError("Location must be a string")
                location = [int(x) for x in location.split(',')]
                ele = getattr(Ranorex, element)(locator)
                ele.DoubleClick(Ranorex.Location(location[0], location[1]))
                return True
        except Exception as error:
            raise AssertionError(error)

    def get_element_attribute(self, locator, attribute):
        """ Get specified element attribute.
        """
        element = self.__return_type(locator)
        obj = getattr(Ranorex, element)(locator)
        return obj.Element.GetAttributeValue(attribute)

    def input_text(self, locator, text):
        """ input texts into specified locator.
        """
        element = self.__return_type(locator)
        getattr(Ranorex, element)(locator).PressKeys(text)
        return True

    def right_click_element(self, locator, location=None):
        """ Rightclick on desired element identified by locator.
        Location of click can be used.
        """
        element = self.__return_type(locator)
        obj = getattr(Ranorex, element)(locator)
        if location == None:
            obj.Click(System.Windows.Forms.MouseButtons.Right)
            return True
        else:
            if not isinstance(location, basestring):
                rtatus:q
                ise AssertionError("Locator must be a string")
            location = [int(x) for x in location.split(',')]
            obj.Click(System.Windows.Forms.MouseButtons.Right,
                      Ranorex.Location(location[0], location[1]))
            return True

    @classmethod
    def run_application(cls, app):
        """ Runs local application.
        """
        Ranorex.Host.Local.RunApplication(app)
        return True

    @classmethod
    def run_application_with_parameters(cls, app, params):
        """ Runs local application with parameters.
        """
        Ranorex.Host.Local.RunApplication(app, params)
        return True

    @classmethod
    def run_script(cls, script_path):
        """ Runs script on remote machine and returns stdout and stderr.
        """
        process = subprocess.Popen([script_path],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        output = process.communicate()
        return {'stdout':output[0], 'stderr':output[1]}

    @classmethod
    def run_script_with_parameters(cls, script_path, params):
        """ Runs script on remote machine and returns stdout and stderr.
        """
        process = subprocess.Popen([script_path, params],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        output = process.communicate()
        return {'stdout':output[0], 'stderr':output[1]}

    def select_by_index(self, locator, index):
        """ Selects item from combobox according to index.
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
        return True

    @classmethod
    def send_keys(cls, locator, key_seq):
        """ Send key combination to specified element.
        Also it gets focus before executing sequence
        seq according to :
        http://msdn.microsoft.com/en-us/library/system.windows.forms.keys.aspx
        """
        Ranorex.Keyboard.PrepareFocus(locator)
        Ranorex.Keyboard.Press(key_seq)
        return True

    def set_focus(self, locator):
        """ Sets focus on desired location.
        """
        element = self.__return_type(locator)
        obj = getattr(Ranorex, element)(locator)
        obj.Focus()
        return obj.HasFocus

    def take_screenshot(self, locator):
        """ Takes screenshot and return it as base64.
        """
        element = self.__return_type(locator)
        obj = getattr(Ranorex, element)(locator)
        img = obj.CaptureCompressedImage()
        return img.ToBase64String()

    def uncheck(self, locator):
        """ Check if element is checked. If yes it uncheck it
        """
        element = self.__return_type(locator)
        if element == 'CheckBox' or element == 'RadioButton':
            obj = getattr(Ranorex, element)(locator)
            if obj.Element.GetAttributeValue('Checked'):
                obj.Click()
                return True
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
            return True
        raise AssertionError("Element %s does not exists" % locator)

    def wait_for_element_attribute(self, locator, attribute,
                                   expected, timeout):
        """ Wait for element attribute becomes requested value.
        """
        curr_time = 0
        timeout = int(timeout)/1000
        while curr_time != timeout:
            value = self.get_element_attribute(locator, attribute)
            if str(value) == str(expected):
                return True
            time.sleep(5)
            curr_time += 5
        raise AssertionError("Object at location %s could not be found"
                             % locator)

    @classmethod
    def wait_for_process_to_start(cls, process_name, timeout):
        """ Waits for /timeout/ seconds for process to start.
        """
        curr_time = 0
        timeout = int(timeout)/1000
        while curr_time <= timeout:
            proc = subprocess.Popen(['tasklist'], stdout=subprocess.PIPE)
            out = proc.communicate()[0]
            res = out.find(process_name) != -1 if out else False
            if res:
                return True
            else:
                curr_time += 5
                time.sleep(5)
        raise AssertionError("Process %s not found within %ss" % (process_name,
                                                                  timeout))

    def kill_process(self, process_name):
        """ Kills process identified by process_name
        """
        if not self.check_if_process_is_running(process_name):
            raise AssertionError("Process %s is not running" % process_name)
        proc = subprocess.Popen(['taskkill', '/im', process_name, '/f'],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = proc.communicate()
        if 'SUCCESS' in out[0]:
            return True
        else:
            raise AssertionError("Process %s not terminated because of: %s" %
                                 (process_name, out))

if __name__ == '__main__':
    RobotRemoteServer(RanorexLibrary(), *sys.argv[1:])
