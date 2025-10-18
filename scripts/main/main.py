from installer import Installer
import packages
from screen import Screen

def read_input(list, multiple_allowed):
    input = screen.display_categories(list, multiple=multiple_allowed)
    if not input:
        return read_input(list)
    return input

def install():
    installer.filter_app_packages(PACKAGES)

    installer.setup_firewall()
    if DNS != "":
        installer.setup_dns(DNS)

    installer.install_environment(list(env_pkgs))
    installer.install_app_packages()
    
    if VPN != "":
        installer.setup_vpn(VPN)

screen = Screen()
installer = Installer()

STARTING_INSTRUCTIONS = [
    "Pick what you would like to install!",
    "Press 'Space' toggle selection.",
    "Press 'Enter' to select packages."
]

DNS = ""
VPN = ""

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

environment = screen.display_menu(packages.ENVIRONMENTS, STARTING_INSTRUCTIONS)

for env in packages.ENVIRONMENTS:
    if environment[0] == env["Name"]:
        env_pkgs = env["Debian_Packages"]

while True:
    input = read_input(packages.CATEGORIES, multiple_allowed=False)
    with open('output.txt', 'w') as file:
        file.write(f"Input was: {input}\n")

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
                        browsers = screen.display_menu(packages.BROWSERS, STARTING_INSTRUCTIONS)
                    case "2. Dev Tools":
                        dev_tools = screen.display_menu(packages.DEV_TOOLS, STARTING_INSTRUCTIONS)
                    case "3. E-mail Clients":
                        email_clients = screen.display_menu(packages.EMAIL_CLIENTS, STARTING_INSTRUCTIONS)
                    case "4. Encryption Tools":
                        encryption_tools = screen.display_menu(packages.ENCRYPTION_TOOLS, STARTING_INSTRUCTIONS)
                    case "5. File Managers":
                        file_managers = screen.display_menu(packages.FILE_MANAGERS, STARTING_INSTRUCTIONS)
                    case "6. Gaming Packages":
                        gaming_packages = screen.display_menu(packages.GAMING_PACKAGES, STARTING_INSTRUCTIONS)
                    case "7. Multimedia Tools":
                        multimedia_tools = screen.display_menu(packages.MULTIMEDIA_TOOLS, STARTING_INSTRUCTIONS)
                    case "8. Note Taking Tools":
                        note_taking_apps = screen.display_menu(packages.NOTE_TAKING_APPS, STARTING_INSTRUCTIONS)
                    case "9. Terminals":
                        terminals = screen.display_menu(packages.TERMINALS, STARTING_INSTRUCTIONS)
                    case _:
                        pass
        case "2. DNS Servers":
            while True:
                input = read_input(packages.DNS_SERVERS, multiple_allowed=False)
                if input == "0. Exit":
                    break
                DNS = input.split(" ", 1)[1]
                break
        case "3. VPN Clients":
            while True:
                input = read_input(packages.VPN_CLIENTS, multiple_allowed=False)
                if input == "0. Exit":
                    break
                VPN = (input.split(" ", 1)[1]).lower()
                break

ENVIRONMENT_PACKAGES = list(env_pkgs)
PACKAGES =  browsers + dev_tools + email_clients + encryption_tools + file_managers + gaming_packages + multimedia_tools + note_taking_apps + terminals

install()

print(f"Installation complete!\n"
      "Check install logs under logs/\n"
      "Please restart your computer.")