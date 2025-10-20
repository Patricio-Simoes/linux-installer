from datetime import datetime
import logging
import packages
import os
import subprocess

SCRIPT_DIR = os.environ["SCRIPT_DIR"]
LOG_DIR = os.environ["LOG_DIR"]


class Installer:
    def __init__(self):
        """
        Initialize the installer class with environment variables, package lists, and logging configuration.

        Sets up package lists for fonts, utilities, and aggregates all packages from predefined categories.
        Initializes empty lists for apt, custom, and flatpak packages.
        Configures logging to a file in the specified log directory with the current date and time.

        Attributes
        ----------
        DISTRO : str
            The Linux distribution ID from the environment variable 'DISTRO_ID'.
        FONT_PKGS : list of str
            List of font package names to be installed.
        UTILITY_PKGS : list of str
            List of utility package names to be installed.
        all_packages : list of str
            Aggregated list of all packages from various categories.
        apt_packages : list of str
            List to store packages to be installed via apt.
        custom_packages : list of str
            List to store custom packages.
        flatpak_packages : list of str
            List to store packages to be installed via Flatpak.
        INSTALL_LOG_FILE_LOCATION : str
            Path to the log file for installation logs.
        """
        self.DISTRO = os.environ["DISTRO_ID"]
        self.FONT_PKGS = []
        self.UTILITY_PKGS = []
        for item in packages.COMMON["FONTS"]:
            if item["Distro"] == self.DISTRO:
                self.FONT_PKGS = item["Packages"]
        for item in packages.COMMON["UTILITY_PACKAGES"]:
            if item["Distro"] == self.DISTRO:
                self.UTILITY_PKGS = item["Packages"]
        self.all_packages = (
            packages.BROWSERS
            + packages.DEV_TOOLS
            + packages.EMAIL_CLIENTS
            + packages.ENCRYPTION_TOOLS
            + packages.FILE_MANAGERS
            + packages.GAMING_PACKAGES
            + packages.MULTIMEDIA_TOOLS
            + packages.NOTE_TAKING_APPS
            + packages.TERMINALS
        )
        self.apt_packages = []
        self.custom_packages = []
        self.flatpak_packages = ["com.github.tchx84.Flatseal"]
        # ? Set up logging configuration
        os.makedirs(LOG_DIR, exist_ok=True)
        CURRENT_DATE = datetime.now().strftime("%d_%m_%Y_%H-%M")
        LOG_FILE = f"Install_{CURRENT_DATE}.txt"
        self.INSTALL_LOG_FILE_LOCATION = os.path.join(LOG_DIR, LOG_FILE)
        logging.basicConfig(
            filename=self.INSTALL_LOG_FILE_LOCATION,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )

    def filter_app_packages(self, packages):
        """
        Filters and categorizes application packages based on the selected package names and the current Linux distribution.

        For each selected package name in `packages`, this function searches through `self.all_packages` to find a matching package.
        Depending on the distribution (`self.DISTRO`), it appends the appropriate package identifier to the corresponding list:
        - For Debian-based distributions, it prioritizes custom scripts, then APT packages, and finally Flatpak packages.

        Parameters
        ----------
        packages : list
            A list of package names selected for installation.

        Returns
        -------
        None

        Side Effects
        ------------
        Modifies the following instance attributes:
        - self.custom_packages : list
            Appends custom script identifiers for selected packages.
        - self.apt_packages : list
            Appends APT package names for selected packages.
        - self.flatpak_packages : list
            Appends Flatpak package names for selected packages.
        """
        for selected_pkg in packages:
            for pkg in self.all_packages:
                if selected_pkg == pkg["Name"]:
                    # ? Debian distros.
                    if self.DISTRO in ["debian"]:
                        if pkg["Custom_Script"] != "":
                            self.custom_packages.append(pkg["Custom_Script"])
                        elif pkg["APT_Package"] != "":
                            self.apt_packages.append(pkg["APT_Package"])
                        elif pkg["Flatpak_Package"] != "":
                            self.flatpak_packages.append(pkg["Flatpak_Package"])

    def build_app_install_commands(self):
        """
        Constructs the installation commands for APT and Flatpak based on the filtered package lists.

        Generates command strings for installing packages using APT and Flatpak, incorporating
        the respective package lists. The commands are formatted to be executed in a shell environment.

        :returns: Tuple containing the APT and Flatpak installation command strings.
        :rtype: tuple
        """
        APT_FONT_STR = f"sudo apt install -y {' '.join(self.FONT_PKGS)}"
        APT_UTILITY_STR = f"sudo apt install -y {' '.join(self.UTILITY_PKGS)}"
        APT_STR = f"sudo apt install -y {' '.join(self.apt_packages)}"
        CUSTOM_STR = (
            " ; ".join([f"bash {script}" for script in self.custom_packages])
            if self.custom_packages
            else ""
        )
        FLATPAK_STR = f"flatpak --user install -y {' '.join(self.flatpak_packages)}"
        return APT_FONT_STR, APT_UTILITY_STR, CUSTOM_STR, APT_STR, FLATPAK_STR

    def install_environment(self, packages):
        """
        Installs the specified environment packages on the system.

        This method first updates and upgrades the system packages,
        then installs the provided list of packages using apt.

        :param packages: List of package names to install.
        :type packages: list[str]
        """
        ENVIRONMENT_STR = "sudo apt install -y " + " ".join(packages)
        SYSTEM_UPDATE_STR = "sudo apt update --fix-missing && sudo apt upgrade -y"
        self.execute_subprocess(SYSTEM_UPDATE_STR, "Updating system packages...")
        self.execute_subprocess(
            ENVIRONMENT_STR, "Installing selected environment packages..."
        )

    def install_app_packages(self, all):
        """
        Install application packages using various package managers and custom scripts.

        This method installs font packages, utility packages, and sets up zram. 
        It also adds the Flathub repository at the user level. If the `all` parameter 
        is set to True, it executes additional installation commands for custom scripts, 
        APT packages, and Flatpak packages.

        :param all: A boolean flag indicating whether to install all packages, 
                    including custom scripts, APT packages, and Flatpak packages.
        :type all: bool
        """
        APT_FONT_STR, APT_UTILITY_STR, CUSTOM_STR, APT_STR, FLATPAK_STR = (
            self.build_app_install_commands()
        )
        self.execute_subprocess(APT_FONT_STR, "Installing font packages...")
        self.execute_subprocess(APT_UTILITY_STR, "Installing utility packages...")
        self.execute_subprocess(
            f"{SCRIPT_DIR}/scripts/custom/System_Utilities/zram.sh", "Setting up zram..."
        )
        self.execute_subprocess(
            "flatpak remote-add --if-not-exists --user flathub https://dl.flathub.org/repo/flathub.flatpakrepo",
            "Adding flathub repository at user level...",
        )
        if all:
            if CUSTOM_STR != "":
                self.execute_subprocess(
                    CUSTOM_STR, "Executing custom installation scripts..."
                )
            if APT_STR != "":
                self.execute_subprocess(APT_STR, "Installing APT packages...")
            if FLATPAK_STR != "":
                self.execute_subprocess(FLATPAK_STR, "Installing Flatpak packages...")

    def execute_subprocess(self, command, description=""):
        """
        Executes a shell command as a subprocess and logs the result.

        Parameters
        ----------
        command : str
            The shell command to execute.
        description : str, optional
            A description to display before executing the command. If not provided, the command itself is printed.

        Returns
        -------
        None

        Logs
        ----
        Logs the success or failure of the command execution, including output and error messages.

        Prints
        ------
        Prints the description or command being executed, and a message indicating success or error.
        """
        if description == "":
            print(f"Executing {command}...")
        else:
            print(description)
        result = subprocess.run(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode == 0:
            print("Command executed with success!")
            logging.info(f"SUCCESS: {command}\nOutput: {result.stdout.strip()}")
        else:
            print("Command encountered an unexpected error.")
            logging.error(
                f"ERROR: {command}\nReturn Code: {result.returncode}\nOutput: {result.stdout.strip()}\nError: {result.stderr.strip()}"
            )

    def setup_firewall(self):
        """
        Sets up the firewall by executing a custom script.

        This method runs a shell script located in the specified directory
        to configure the firewall settings. The script is executed as a
        subprocess, and a message is displayed to indicate the operation.

        Raises:
            subprocess.SubprocessError: If the subprocess execution fails.
        """
        self.execute_subprocess(
            f"{SCRIPT_DIR}/scripts/custom/Firewalls/ufw.sh",
            "Setting up the Firewall...",
        )

    def setup_dns(self, server):
        """
        Configure the DNS server by executing a custom script.

        :param server: The DNS server address to configure.
        :type server: str
        """
        self.execute_subprocess(
            f"{SCRIPT_DIR}/scripts/custom/System_Utilities/dns.sh {server}",
            f"Setting up {server} DNS...",
        )

    def setup_vpn(self, client):
        """
        Set up a VPN client by executing the corresponding setup script.

        This method runs a shell script located in the custom VPNs directory
        to configure the specified VPN client.

        :param client: The name of the VPN client to set up. This should match
                       the name of the corresponding shell script (without the .sh extension).
                       Example: 'openvpn', 'wireguard'.
        :type client: str
        :raises subprocess.CalledProcessError: If the subprocess execution fails.
        """
        self.execute_subprocess(
            f"{SCRIPT_DIR}/scripts/custom/VPNs/{client}.sh",
            f"Setting up {client.capitalize()} VPN...",
        )

    def install_nvidia_drivers(self):
        """
        Installs NVIDIA drivers by executing a custom script.

        This method runs a shell script located in the specified directory
        to install NVIDIA drivers. The script is executed as a subprocess,
        and a message is displayed to indicate the operation.

        Raises:
            subprocess.SubprocessError: If the subprocess execution fails.
        """
        self.execute_subprocess(
            f"{SCRIPT_DIR}/scripts/custom/System_Utilities/nvidia_drivers.sh",
            "Installing NVIDIA drivers...",
        )

    def setup_container_engine(self, backend, tool):
        """
        Sets up the specified container backend & tool by executing the corresponding setup scripts.

        :param backend: The name of the container backend to set up (e.g., "docker", "podman").
        :param tool: The name of the tool used to manage containers (e.g., "distrobox").
        :type backend: str
        :raises subprocess.CalledProcessError: If the setup script execution fails.
        """
        self.execute_subprocess(
            f"{SCRIPT_DIR}/scripts/custom/Containers/{backend.lower()}.sh",
            f"Setting up {backend.capitalize()}...",
        )
        self.execute_subprocess(
            f"{SCRIPT_DIR}/scripts/custom/Containers/{tool.lower()}.sh",
            f"Setting up {tool.capitalize()}...",
        )

    def install_containers(self, containers):
        """
        Sets up the specified container backend & tool by executing the corresponding setup scripts.

        :param backend: The name of the container backend to set up (e.g., "docker", "podman").
        :param tool: The name of the tool used to manage containers (e.g., "distrobox").
        :type backend: str
        :raises subprocess.CalledProcessError: If the setup script execution fails.
        """
        for container in containers:
            for cont in packages.CONTAINERS:
                if cont["Name"] == container:
                    self.execute_subprocess(
                        f"{SCRIPT_DIR}/containers/{cont['Type'].lower()}/install.sh {cont['Name'].split(' ', 1)[1]}",
                        f"Setting up {cont['Name'].split(' ', 1)[1]} container...",
                    )
