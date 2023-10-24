import winreg
import pathlib


QGIS = "QGIS"
QGIS_LOWER = QGIS.lower()


class Software:
    """Data class storing info about one version of QGIS app"""

    def __init__(self, full_name) -> None:
        self.full_name: str = full_name
        self.short_name: str = None
        self.nick_name: str = None
        self.version: str = None
        self.publisher: str = None
        self.path: str = None
        self.path_end_part: str = None

    def __repr__(self) -> str:
        return f"Software('{self.full_name}')"

    def __str__(self) -> str:
        return f"{self.full_name} - {self.publisher} - {self.path}"


def get_qgis_apps() -> list[Software]:
    """List QGIS apps found using the Windows registry
    Inspired by Pablo Satler (see https://gist.github.com/psatler/010b26cd57e758278823d7027c40e2a6)

    Returns:
        list[Software]: list of QGIS apps
    """

    def _update_software_list_from_default_osgeo4w_dir() -> None:
        """Add to the software list the QGIS apps found in the OSGeo4W and OSGeo4W64
        directories.
        """
        qgis_default_dir_paths = [
            r"C:\OSGeo4W64",
            r"C:\OSGeo4W",
        ]

        for qgis_default_dir_path in qgis_default_dir_paths:
            osgeo4w_bat_file = pathlib.Path(qgis_default_dir_path) / "OSGeo4W.bat"

            if not osgeo4w_bat_file.exists():
                continue

            osgeo4w_bin_dir = pathlib.Path(qgis_default_dir_path) / "bin"
            if not osgeo4w_bin_dir.exists():
                continue

            for qgis_exe_file in osgeo4w_bin_dir.glob("qgis*.exe"):
                software: Software = Software("QGIS")
                software.publisher = "OSGeo4W"
                software.path = qgis_default_dir_path

                software_list.append(software)
                break

    def _create_software_from_info_key(sub_key) -> Software:
        """Create a Software object from one key found in the Widnows registry.
        Return None if the app is not a version of QGIS.
        The app is considered to be a version of QGIS if:
        - QGIS is present in the app name
        - QGIS is present in the app publisher name

        Args:
            sub_key: Windows registry key

        Returns:
            Software: QGIS app object
        """
        software: Software = Software(winreg.QueryValueEx(sub_key, "DisplayName")[0])

        try:
            software.version = winreg.QueryValueEx(sub_key, "DisplayVersion")[0]
        except EnvironmentError:
            software.version = None

        try:
            software.publisher = winreg.QueryValueEx(sub_key, "Publisher")[0]
        except EnvironmentError:
            software.publisher = None

        if (
            QGIS_LOWER in software.full_name.lower()
            and QGIS_LOWER in software.publisher.lower()
        ):
            name_parts = software.full_name.split()
            if len(name_parts) > 0:
                software.short_name = name_parts[0]
            if len(name_parts) > 1 and not software.version:
                software.version = name_parts[1]
            if len(name_parts) > 2:
                software.nick_name = name_parts[2]

            software.path_end_part = f"{QGIS} {software.version}\\"

            return software

    def _update_software_list_from_uninstall_info(hive, flag):
        """Parse the Uninstall key of Windows registry in order to find installed QGIS apps.
        This functions updates the software_list variable.

        Args:
            hive: see winreg docs
            flag: see winreg docs
        """
        reg = winreg.ConnectRegistry(None, hive)
        key = winreg.OpenKey(
            reg,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            0,
            winreg.KEY_READ | flag,
        )

        count_sub_keys = winreg.QueryInfoKey(key)[0]

        for i in range(count_sub_keys):
            try:
                sub_key_name = winreg.EnumKey(key, i)
                sub_key = winreg.OpenKey(key, sub_key_name)

                software = _create_software_from_info_key(sub_key)
                if software:
                    software_list.append(software)

            except EnvironmentError:
                continue

    def _update_software_path_from_installer_folder_info(hive, flag):
        """Update the software list by adding a path for each of them.
        The path is found in the Installer/Folders key of the Windows registry.
        This functions updates the software_list variable.

        Args:
            hive: see winreg docs
            flag: see winreg docs
        """
        reg = winreg.ConnectRegistry(None, hive)
        key = winreg.OpenKey(
            reg,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Installer\Folders",
            0,
            winreg.KEY_READ | flag,
        )

        count = 0
        try:
            while 1:
                value_name, _, _ = winreg.EnumValue(key, count)
                if QGIS in value_name:
                    for software in software_list:
                        if software.path_end_part and value_name.endswith(
                            software.path_end_part
                        ):
                            software.path = value_name
                count = count + 1
        except WindowsError:
            pass

    software_list = []

    _update_software_list_from_default_osgeo4w_dir()

    _update_software_list_from_uninstall_info(
        winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_32KEY
    )
    _update_software_list_from_uninstall_info(
        winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY
    )
    _update_software_list_from_uninstall_info(winreg.HKEY_CURRENT_USER, 0)

    _update_software_path_from_installer_folder_info(
        winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY
    )

    return software_list


def main() -> None:
    """Print the list of QGIS apps found in the Windows registry."""
    software_list = get_qgis_apps()
    for software in software_list:
        print(
            f"Name={software.short_name}, Version={software.version}, "
            f"Nickname={software.nick_name}, Path={software.path}"
        )


if __name__ == "__main__":
    main()
