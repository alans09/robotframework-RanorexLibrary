""" Remote Ranorex library for Robot Framework """
import clr
clr.AddReference('Ranorex.Core')
clr.AddReference('System.Windows.Forms')
import System.Windows.Forms
import Ranorex
import sys
from robotremoteserver import RobotRemoteServer


class RanorexLibrary(object):
    """ Basic ranorex class library for robot framework """
    def __return_type(self, locator):
        """ Translate xpath into element type """
        try:
            supported_types = ['AbbrTag', 'AcronymTag', 'AddressTag', 'AreaTag',
                               'ArticleTag', 'AsideTag', 'ATag', 'AudioTag',
                               'BaseFontTag', 'BaseTag', 'BdoTag', 'BigTag',
                               'BodyTag', 'BrTag', 'BTag', 'Button', 'ButtonTag',
                               'CanvasTag', 'Cell', 'CenterTag', 'CheckBox', 'CiteTag',
                               'CodeTag', 'ColGroupTag', 'ColTag', 'Column', 'ComboBox',
                               'CommandTag', 'ContextMenu', 'DataListTag', 'DdTag', 'DelTag',
                               'DetailsTag', 'DfnTag', 'DirTag', 'DivTag', 'DlTag', 'EmbedTag',
                               'EmTag', 'FieldSetTag', 'FigureTag', 'FontTag', 'Form',
                               'FormTag', 'Link', 'List', 'ListItem', 'MenuBar', 'MenuItem',
                               'Picture', 'ProgressBar', 'RadioButton', 'Row', 'ScrollBar', 
                               'Slider', 'StatusBar', 'Text', 'TitleBar', 'ToggleButton', 
                               'Tree', 'TreeItem', 'Unknown']
            splitted_locator = locator.split('/')
            if "[" in splitted_locator[-1]:
                ele = splitted_locator[-1].split('[')[0]
            else:
                ele = splitted_locator[-1]
            for item in supported_types:
                if ele.lower() == item.lower():
                    return item
            return "Element is not supported"
        except Exception as error:
            return "Element not supported\n%s" % error

    def click_element(self, locator):
        """ Clicks on element located on location : locator.
        locator:  xpath to object
        """
        element = self.__return_type(locator)
        getattr(Ranorex, element)(locator).Click()

    def check(self, locator):
        """ Check if element is checked. If not it check it """
        element = self.__return_type(locator)
        if element == 'CheckBox' or element == 'RadioButton':
            obj = getattr(Ranorex, element)(locator)
            if obj.Element.GetAttributeValue('Checked'):
                obj.Click()
        else:
            return "Element not supported for checking"

    def double_click_element(self, locator):
        """ Doubleclick on desired element """
        element = self.__return_type(locator)
        getattr(Ranorex, element)(locator).DoubleClick()

    def get_element_attribute(self, locator, attribute):
        """ Get specified element attribute """
        element = self.__return_type(locator)
        obj = getattr(Ranorex, element)(locator)
        return obj.Element.GetAttributeValue(attribute)

    def input_text(self, locator, text):
        """ input texts into specified locator
        locator: xpath to object
        text: text to enter
        """
        element = self.__return_type(locator)
        getattr(Ranorex, element)(locator).PressKeys(text)

    def right_click_element(self, locator):
       """ Rightclick on desired element """
       element = self.__return_type(locator)
       getattr(Ranorex, element)(locator).Click(System.Windows.Forms.MouseButtons.Right)

    def run_application(self, app):
        """ Runs local application """
        Ranorex.Host.Local.RunApplication(app)

    def run_application_with_parameters(self, app, params):
        """ Runs local application with parameters """
        Ranorex.Host.Local.RunApplication(app, params)
 
    def run_script(self, script_path):
        """ Runs script on remote machine and returns stdout and stderr """
        import subprocess
        process = subprocess.Popen([script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = process.communicate()
        return {'stdout':output[0], 'stderr':output[1]}

    def run_script_with_parameters(self, script_path, params):
        """ Runs script on remote machine and returns stdout and stderr """
        import subprocess
        process = subprocess.Popen([script_path, params], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = process.communicate()
        return {'stdout':output[0], 'stderr':output[1]}

    def select_by_index(self, locator, index):
        """ Selects item from combobox according to index"""
        try:
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
        except Exception as error:
            return error

    def take_screenshot(self, locator):
        """ Takes screenshot and return it as base64 """
        element = self.__return_type(locator)
        obj = getattr(Ranorex, element)(locator)
        img = obj.CaptureCompressedImage()
        return img.ToBase64String()

    def uncheck(self, locator):
        """ Check if element is checked. If yes it uncheck it """
        element = self.__return_type(locator)
        if element == 'CheckBox' or element == 'RadioButton':
            obj = getattr(Ranorex, element)(locator)
            if not obj.Element.GetAttributeValue('Checked'):
                obj.Click()
        else:
            return "Element not supported for unchecking"

    def wait_for_element(self, locator, timeout):
        """ Wait for element becomes on the screen """
        Ranorex.Validate.EnableReport = False
        if Ranorex.Validate.Exists(locator, int(timeout)):
            return 'Element %s exists' % locator

    def wait_for_element_attribute(self, locator, attribute,
                                   expected, timeout):
        """ Wait for element attribute becomes requested """
        import time
        curr_time = 0
        timeout = int(timeout)/1000
        while curr_time != timeout:
            value = self.get_element_attribute(locator, attribute)
            if str(value) == str(expected):
                return True
            time.sleep(1)
            curr_time += 1
        raise(Exception("No value match within %ss" % timeout))


if __name__ == '__main__':
    RobotRemoteServer(RanorexLibrary(), *sys.argv[1:])
