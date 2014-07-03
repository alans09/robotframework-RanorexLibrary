"""
    Remote ranorex library for robot framework
    All commands return True if they are executed correctly
"""
#iron python ]%imports
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
import logging
import os

logging.basicConfig(
    format="%(asctime)s::[%(name)s.%(levelname)s] %(message)s",
    datefmt="%I:%M:%S %p",
    level='DEBUG')
logging.StreamHandler(sys.__stdout__)


class RanorexLibrary(object):
    """ Basic implementation of ranorex object calls for
    robot framework
    """
    def __init__(self):
        self.debug = False
        self.model_loaded = False
        self.model = None

    def start_debug(self):
        """ Starts to show debug messages on remote connector """
        self.debug = True
################

    def __return_what_to_do(self, repository, item):
        """  Returns parsed list with command and arguments"""
        rep_file = open(repository, 'r')
        repo = rep_file.readlines()
        rep_file.close()
        sendkey = False
        location = False
        if self.debug:
            log = logging.getLogger("__return_repository_item")
        ## parse command from rest ###
        command = item[1:item.find('(', 1)]
        rest = item[item.find('(', 1)+1:-2]
        if self.debug:
            log.debug("Rest to parse: %s", rest)
            log.debug("Command to run: %s", command)
        if 'send_key' in command:
            rep_item = rest[0:rest.find('}', 1)+1]
            combination = rest[rest.find('},', 1)+2:]
            if self.debug:
                log.debug("repository item: %s", rep_item)
                log.debug("Key combination: %s", combination)
            sendkey = True
        elif 'location' in item:
            rep_item = rest.split(',')[0]
            location = item.split('=')[1]
            location = location.replace('\'', '')
            if self.debug:
                log.debug("Location is part of item")
                log.debug("Repository item: %s", rep_item)
                log.debug("Location: %s", location[:-2])
        else:
            rep_item = rest
            if self.debug:
                log.debug("rep_item: %s", rest)
            location = False
        for line in repo:
            if rep_item in line:
                if self.debug:
                    log.debug("Found match -> %s",
                              line.split('=', 1)[1].strip())
                if location:
                    return [command, line.split('=', 1)[1].strip(),
                            location[:-2]]
                elif sendkey:
                    return [command, line.split('=', 1)[1].strip(),
                            combination]
                elif not location:
                    return [command, line.split('=', 1)[1].strip()]
        if location:
            return [command, rep_item, location]
        elif sendkey:
            return [command, rep_item, combination]
        else:
            return [command, rep_item]

    def load_model(self, model, force=False):
        """ Loads model from dot file """
        if force:
            self.model_loaded = False
        if self.model_loaded:
            return True
        if self.debug:
            log = logging.getLogger("Load Model")
        try:
            from pygraph.readwrite import dot
        except Exception:
            raise AssertionError("No pygraph installed")
        data = open(model).read()
        self.model = dot.read(data)
        self.model_loaded = True
        if self.debug:
            log.debug("Model loaded!")
        return True

    def navigate_to(self, start, finish, repository=None):
        """ Navigates from start node to finish node """
        if self.debug:
            log = logging.getLogger("Navigate To")
        try:
            from pygraph.algorithms.minmax import shortest_path
        except Exception:
            raise AssertionError("Can't import shortest_path")
        s_path = shortest_path(self.model, start)
        end = finish
        path = []
        path = path + [end]
        for _ in range(0, int(s_path[1][end])-1):
            path = [s_path[0][path[0]]] + path
        path = [start] + path
        edges_to_go = [(path[i], path[i+1]) for i in range(0, len(path)-1)]
        if self.debug:
            log.debug("====Edges to go trough: %s====", edges_to_go)
        res = []
        for i in edges_to_go:
            what_to_do = self.model.edge_label(i)
            res.append(what_to_do)
            if self.debug:
                log.debug("What to do: %s", what_to_do)
                log.debug(" === Current edge: %s === ", str(i))
            wtd = self.__return_what_to_do(repository, what_to_do)
            if self.debug:
                log.debug("Going to execute: %s", wtd)
            if len(wtd) == 2:
                getattr(self, wtd[0])(wtd[1])
            elif len(wtd) == 3:
                if self.debug:
                    log.debug("Going to execute: %s", wtd)
                if "{" in wtd[2]:
                    getattr(self, wtd[0])(wtd[1], wtd[2])
                else:
                    getattr(self, wtd[0])(wtd[1], location=wtd[2])
        return True
#################

    def stop_debug(self):
        """ Stops to show debug messages """
        self.debug = False

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
        if self.debug:
            log = logging.getLogger("Click Element")
            log.debug("Locator: %s", locator)
            log.debug("Location: %s", location)
        element = self.__return_type(locator)
        if self.debug:
            log.debug("Element: %s", element)
        ele = getattr(Ranorex, element)(locator)
        if self.debug:
            log.debug("Application object: %s", ele)
        try:
            if location == None:
                ele = getattr(Ranorex, element)(locator)
                ele.Click()
                return True
            else:
                if not isinstance(location, basestring):
                    raise AssertionError("Location must be a string")
                location = [int(x) for x in location.split(',')]
                ele.Click(Ranorex.Location(location[0], location[1]))
                return True
        except Exception as error:
            if self.debug:
                log.error("Failed because of %s", error)
            raise AssertionError(error)

    def check(self, locator):
        """ Check if element is checked. If not it check it.
            Only checkbox and radiobutton are supported.
            Uses Click() method to check it.
        """
        if self.debug:
            log = logging.getLogger("Check")
            log.debug("Locator: %s", locator)
        element = self.__return_type(locator)
        if self.debug:
            log.debug("Element: %s", element)
        if element == 'CheckBox' or element == 'RadioButton':
            if self.debug:
                log.debug("Element is radiobutton or checkbox")
            obj = getattr(Ranorex, element)(locator)
            if self.debug:
                log.debug("Application object: %s", obj)
            if not obj.Element.GetAttributeValue('Checked'):
                obj.Element.GetAttributeValue('Checked')
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
        if self.debug:
            log = logging.getLogger("Clear Text")
            log.debug("Locator: %s", locator)
        element = self.__return_type(locator)
        if self.debug:
            log.debug("Element: %s", element)
        if element != "Text":
            if self.debug:
                log.error("Element is not a text field")
            raise AssertionError("Only element Text is supported!")
        else:
            obj = getattr(Ranorex, element)(locator)
            if self.debug:
                log.debug("Application object: %s", obj)
            obj.PressKeys("{End}{Shift down}{Home}{Shift up}{Delete}")
            return True
        raise AssertionError("Element %s does not exists" % locator)

    def double_click_element(self, locator, location=None):
        """ Doubleclick on element identified by locator. It can click
            on desired location if requested.
        """
        if self.debug:
            log = logging.getLogger("Double Click Element")
            log.debug("Locator: %s", locator)
            log.debug("Location: %s", location)
        element = self.__return_type(locator)
        if self.debug:
            log.debug("Element: %s", element)
        obj = getattr(Ranorex, element)(locator)
        if self.debug:
            log.debug("Application object: %s", obj)
        try:
            if location == None:
                obj.DoubleClick()
                return True
            else:
                if not isinstance(location, basestring):
                    raise AssertionError("Location must be a string")
                location = [int(x) for x in location.split(',')]
                obj.DoubleClick(Ranorex.Location(location[0], location[1]))
                return True
        except Exception as error:
            raise AssertionError(error)

    def get_element_attribute(self, locator, attribute):
        """ Get specified element attribute.
        """
        if self.debug:
            log = logging.getLogger("Get Element Attribute")
            log.debug("Locator: %s", locator)
            log.debug("Attribute: %s", attribute)
        element = self.__return_type(locator)
        if self.debug:
            log.debug("Element: %s", element)
        obj = getattr(Ranorex, element)(locator)
        if self.debug:
            log.debug("Application object: %s", obj)
        found = obj.Element.GetAttributeValue(attribute)
        if self.debug:
            log.debug("Found attribute value is: %s", found)
        return found

    def input_text(self, locator, text):
        """ input texts into specified locator.
        """
        if self.debug:
            log = logging.getLogger("Input Text")
            log.debug("Locator: %s", locator)
            log.debug("Text to enter: %s", text)
        element = self.__return_type(locator)
        if self.debug:
            log.debug("Element: %s", element)
        obj = getattr(Ranorex, element)(locator)
        if self.debug:
            log.debug("Application object: %s", obj)
        obj.PressKeys(text)
        return True

    def right_click_element(self, locator, location=None):
        """ Rightclick on desired element identified by locator.
        Location of click can be used.
        """
        if self.debug:
            log = logging.getLogger("Right Click Element")
            log.debug("Locator: %s", locator)
            log.debug("Location: %s", location)
        element = self.__return_type(locator)
        if self.debug:
            log.debug("Element: %s", element)
        obj = getattr(Ranorex, element)(locator)
        if self.debug:
            log.debug("Application object: %s", obj)
        if location == None:
            obj.Click(System.Windows.Forms.MouseButtons.Right)
            return True
        else:
            if not isinstance(location, basestring):
                raise AssertionError("Locator must be a string")
            location = [int(x) for x in location.split(',')]
            obj.Click(System.Windows.Forms.MouseButtons.Right,
                      Ranorex.Location(location[0], location[1]))
            return True

    def run_application(self, app):
        """ Runs local application.
        """
        if self.debug:
            log = logging.getLogger("Run Application")
            log.debug("Application: %s", app)
            log.debug("Working dir: %s", os.getcwd())
        Ranorex.Host.Local.RunApplication(app)
        return True

    def run_application_with_parameters(self, app, params):
        """ Runs local application with parameters.
        """
        if self.debug:
            log = logging.getLogger("Run Application With Parameters")
            log.debug("Application: %s", app)
            log.debug("Parameters: %s", params)
            log.debug("Working dir: %s", os.getcwd())
        Ranorex.Host.Local.RunApplication(app, params)
        return True

    def run_script(self, script_path):
        """ Runs script on remote machine and returns stdout and stderr.
        """
        if self.debug:
            log = logging.getLogger("Run Script")
            log.debug("Script: %s", script_path)
            log.debug("Working dir: %s", os.getcwd())
        process = subprocess.Popen([script_path],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        output = process.communicate()
        return {'stdout':output[0], 'stderr':output[1]}

    def run_script_with_parameters(self, script_path, params):
        """ Runs script on remote machine and returns stdout and stderr.
        """
        if self.debug:
            log = logging.getLogger("Run Script With Parameters")
            log.debug("Script: %s", script_path)
            log.debug("Parameters: %s", params)
            log.debug("Working dir: %s", os.getcwd())
        process = subprocess.Popen([script_path, params],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        output = process.communicate()
        return {'stdout':output[0], 'stderr':output[1]}

    def select_by_index(self, locator, index):
        """ Selects item from combobox according to index.
        """
        if self.debug:
            log = logging.getLogger("Select By Index")
            log.debug("Locator: %s", locator)
            log.debug("Index: %s", index)
        element = self.__return_type(locator)
        if self.debug:
            log.debug("Element: %s", element)
        obj = getattr(Ranorex, element)(locator)
        if self.debug:
            log.debug("Application object: %s", obj)
        selected = obj.Element.GetAttributeValue("SelectedItemIndex")
        if self.debug:
            log.debug("Selected item: %s", selected)
        diff = int(selected) - int(index)
        if self.debug:
            log.debug("Diff for keypress: %s", diff)
        if diff >= 0:
            for _ in range(0, diff):
                obj.PressKeys("{up}")
        elif diff < 0:
            for _ in range(0, abs(diff)):
                obj.PressKeys("{down}")
        return True

    def send_keys(self, locator, key_seq):
        """ Send key combination to specified element.
        Also it gets focus before executing sequence
        seq according to :
        http://msdn.microsoft.com/en-us/library/system.windows.forms.keys.aspx
        """
        if self.debug:
            log = logging.getLogger("Send Keys")
            log.debug("Locator: %s", locator)
            log.debug("Key sequence: %s", key_seq)
        Ranorex.Keyboard.PrepareFocus(locator)
        Ranorex.Keyboard.Press(key_seq)
        return True

    def set_focus(self, locator):
        """ Sets focus on desired location.
        """
        if self.debug:
            log = logging.getLogger("Set Focus")
            log.debug("Locator: %s", locator)
        element = self.__return_type(locator)
        if self.debug:
            log.debug("Element: %s", element)
        obj = getattr(Ranorex, element)(locator)
        if self.debug:
            log.debug("Application object: %s", obj)
        obj.Focus()
        return obj.HasFocus

    def take_screenshot(self, locator):
        """ Takes screenshot and return it as base64.
        """
        if self.debug:
            log = logging.getLogger("Take Screenshot")
            log.debug("Locator: %s", locator)
        element = self.__return_type(locator)
        if self.debug:
            log.debug("Element: %s", element)
        obj = getattr(Ranorex, element)(locator)
        if self.debug:
            log.debug("Application object: %s", obj)
        img = obj.CaptureCompressedImage()
        return img.ToBase64String()

    def uncheck(self, locator):
        """ Check if element is checked. If yes it uncheck it
        """
        if self.debug:
            log = logging.getLogger("Uncheck")
            log.debug("Locator: %s", locator)
        element = self.__return_type(locator)
        if self.debug:
            log.debug("Element: %s", element)
        if element == 'CheckBox' or element == 'RadioButton':
            obj = getattr(Ranorex, element)(locator)
            if self.debug:
                log.debug("Application object: %s", obj)
            if obj.Element.GetAttributeValue('Checked'):
                if self.debug:
                    log.debug("Object is checked => unchecking")
                obj.Click()
                return True
        else:
            raise AssertionError("Element |%s| not supported for unchecking"
                                 % element)

    def wait_for_element(self, locator, timeout):
        """ Wait for element becomes on the screen.
        """
        if self.debug:
            log = logging.getLogger("Wait For Element")
            log.debug("Locator: %s", locator)
            log.debug("Timeout: %s", timeout)
        Ranorex.Validate.EnableReport = False
        if Ranorex.Validate.Exists(locator, int(timeout)) is None:
            return True
        raise AssertionError("Element %s does not exists" % locator)

    def wait_for_element_attribute(self, locator, attribute,
                                   expected, timeout):
        """ Wait for element attribute becomes requested value.
        """
        if self.debug:
            log = logging.getLogger("Wait For Element Attribute")
            log.debug("Locator: %s", locator)
            log.debug("Attribute: %s", attribute)
            log.debug("Expected: %s", expected)
            log.debug("Timeout: %s", timeout)
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

    def wait_for_process_to_start(self, process_name, timeout):
        """ Waits for /timeout/ seconds for process to start.
        """
        if self.debug:
            log = logging.getLogger("Wait For Process To Start")
            log.debug("Process name: %s", process_name)
            log.debug("Timeout: %s", timeout)
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
        if self.debug:
            log = logging.getLogger("Kill Process")
            log.debug("Process name: %s", process_name)
        res = self.check_if_process_is_running(process_name)
        if self.debug:
            log.debug("Process is running: %s", res)
        if not res:
            raise AssertionError("Process %s is not running" % process_name)
        proc = subprocess.Popen(['taskkill', '/im', process_name, '/f'],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = proc.communicate()
        if 'SUCCESS' in out[0]:
            if self.debug:
                log.debug("Output of killing: %s", out)
            return True
        else:
            raise AssertionError("Process %s not terminated because of: %s" %
                                 (process_name, out))

if __name__ == '__main__':
    RobotRemoteServer(RanorexLibrary(), *sys.argv[1:])
