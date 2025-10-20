from installer import Installer
import packages
from screen import Screen


def read_input(list, multiple_allowed):
    input = screen.display_categories(list, multiple=multiple_allowed)
    if not input:
        return read_input(list)
    return input


def install():
    installer.setup_firewall()

    if dns != "":
        installer.setup_dns(dns)

    if env_pkgs != []:
        installer.install_environment(list(env_pkgs))

    install_all_pkgs = True if app_pkgs != [] else False

    installer.filter_app_packages(app_pkgs)
    installer.install_app_packages(all=install_all_pkgs)

    if nvidia:
        installer.install_nvidia_drivers()

    if container_backend != "" and container_tool != "":
        installer.setup_container_engine(container_backend, container_tool)
        if "0. Exit" not in containers:
            installer.install_containers(containers)

    if vpn != "":
        installer.setup_vpn(vpn)


screen = Screen()
installer = Installer()

STARTING_INSTRUCTIONS = [
    "Pick what you would like to install!",
    "Press 'Space' toggle selection.",
    "Press 'Enter' to select packages.",
]

dns = ""
vpn = ""
nvidia = False
container_backend = ""

env_pkgs = []
browsers = []
environment = []
dev_tools = []
email_clients = []
encryption_tools = []
file_managers = []
gaming_packages = []
multimedia_tools = []
note_taking_apps = []
terminals = []

app_pkgs = []

environment = screen.display_menu(packages.ENVIRONMENTS, STARTING_INSTRUCTIONS)

if environment[0] != "0. Skip":
    for env in packages.ENVIRONMENTS:
        if environment[0] == env["Name"]:
            env_pkgs = env["Debian_Packages"]

while True:
    input = read_input(packages.CATEGORIES, multiple_allowed=False)

    match input:
        case "0. Exit":
            break
        case "1. Applications":
            while True:
                input = read_input(packages.APP_CATEGORIES, multiple_allowed=False)
                if input == "0. Exit":
                    break
                match input:
                    case "1. Browsers":
                        browsers = screen.display_menu(
                            packages.BROWSERS, STARTING_INSTRUCTIONS
                        )
                    case "2. Dev Tools":
                        dev_tools = screen.display_menu(
                            packages.DEV_TOOLS, STARTING_INSTRUCTIONS
                        )
                    case "3. E-mail Clients":
                        email_clients = screen.display_menu(
                            packages.EMAIL_CLIENTS, STARTING_INSTRUCTIONS
                        )
                    case "4. Encryption Tools":
                        encryption_tools = screen.display_menu(
                            packages.ENCRYPTION_TOOLS, STARTING_INSTRUCTIONS
                        )
                    case "5. File Managers":
                        file_managers = screen.display_menu(
                            packages.FILE_MANAGERS, STARTING_INSTRUCTIONS
                        )
                    case "6. Gaming Packages":
                        gaming_packages = screen.display_menu(
                            packages.GAMING_PACKAGES, STARTING_INSTRUCTIONS
                        )
                    case "7. Multimedia Tools":
                        multimedia_tools = screen.display_menu(
                            packages.MULTIMEDIA_TOOLS, STARTING_INSTRUCTIONS
                        )
                    case "8. Note Taking Tools":
                        note_taking_apps = screen.display_menu(
                            packages.NOTE_TAKING_APPS, STARTING_INSTRUCTIONS
                        )
                    case "9. Terminals":
                        terminals = screen.display_menu(
                            packages.TERMINALS, STARTING_INSTRUCTIONS
                        )
                    case _:
                        pass
        case "2. Containers":
            container_backend = ""
            container_tool = ""
            input = read_input(packages.CONTAINER_BACKENDS, multiple_allowed=False)
            if input != "0. Exit":
                container_backend = input.split("(")[-1].strip(" )")
                container_tool = input.split()[1]
                container_list = ["0. Exit"]
                for container in packages.CONTAINERS:
                    if container["Type"] == container_tool:
                        container_list.append(container["Name"])
                containers = input = read_input(container_list, multiple_allowed=True)
        case "3. DNS Servers":
            input = read_input(packages.DNS_SERVERS, multiple_allowed=False)
            if input != "0. Exit":
                dns = input.split(" ", 1)[1]
        case "4. System Utilities":
            input = read_input(packages.SYSTEM_UTILITIES, multiple_allowed=False)
            if input != "0. Exit":
                nvidia = True
        case "5. VPN Clients":
            input = read_input(packages.VPN_CLIENTS, multiple_allowed=False)
            if input != "0. Exit":
                vpn = (input.split(" ", 1)[1]).lower()

app_pkgs = (
    browsers
    + dev_tools
    + email_clients
    + encryption_tools
    + file_managers
    + gaming_packages
    + multimedia_tools
    + note_taking_apps
    + terminals
)

install()

print(
    f"Installation complete!\n"
    "Check install logs under logs/\n"
    "Please restart your computer."
)
