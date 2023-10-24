import platform
import os
import subprocess
import tempfile
import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from prompt_toolkit import prompt, print_formatted_text, HTML, PromptSession
from prompt_toolkit.completion import WordCompleter

from qgis_apps import get_qgis_apps, Software


class DontContinueException(Exception):
    pass


class NotOnWindowsException(Exception):
    pass


def _install_python_packages_for_qgis_app(qgis_app: Software):
    """Install the Python packages:
    - create a temp dir in order to store temporary reachable from OSGeo4W
    - create the requirements.txt file
    - create the .bat file from a template
    - run the .bat file within the OSGeo4W shell

    Args:
        qgis_app (Software): QGIS app description (with name, version, path...)
    """

    # Set the new working directory (root directory of QGIS)
    os.chdir(qgis_app.path)

    try:
        # Copy config files in temp dir in order to make them accessible from subprocesses

        # Compute path to temp dir and files
        temp_dir = tempfile.TemporaryDirectory()
        temp_install_bat_file_path = Path(temp_dir.name) / "pip-install.bat"
        temp_requirements_file_path = Path(temp_dir.name) / "requirements.txt"

        # Create temp requirements.txt file
        requirements_file_path = Path(__file__) / ".." / "config" / "requirements.txt"
        shutil.copy(requirements_file_path, temp_requirements_file_path)

        # Create temp bat file
        jinja_template_dir_path = Path(__file__) / ".." / "config" / "templates"
        jinja_template_dir_path = jinja_template_dir_path.resolve()
        env = Environment(
            loader=FileSystemLoader(jinja_template_dir_path),
            autoescape=select_autoescape(),
        )
        install_bat_template = env.get_template("pip-install.bat")
        temp_install_bat_content = install_bat_template.render(
            file_path=temp_requirements_file_path,
        )

        with open(temp_install_bat_file_path, "w") as temp_install_bat_file:
            temp_install_bat_file.write(temp_install_bat_content)

        # Install Python packages in the QGIS Python distribution
        # Needs to be done through the OSGeo4W terminal
        subprocess.run([r"OSGeo4W.bat", temp_install_bat_file_path])
    finally:
        temp_dir.cleanup()


def install_python_packages_in_qgis():
    """List QGIS apps installed, ask for which one the Python packages should be installed and then
    install the packages.
    """
    print_formatted_text(
        HTML("<gold>Programme d'installation de modules Python pour QGIS</gold>")
    )
    print_formatted_text("")
    print_formatted_text(
        """Il a été développé spécifiquement pour installer les modules Python
requis pour les plugins de Gécosat."""
    )
    print_formatted_text("")

    last_cwd = None

    try:
        if platform.system() != "Windows":
            raise NotOnWindowsException

        # Ask the user what to do
        yes_no_completer = WordCompleter(["oui", "non", "yes", "no"], ignore_case=True)
        session = PromptSession(completer=yes_no_completer)
        text = session.prompt("Voulez-vous continuer ? > ")
        if text.lower() in ["o", "oui", "y", "yes"]:
            pass
        elif text.lower() in ["n", "non", "no"]:
            raise DontContinueException
        else:
            raise DontContinueException

        # Save the current working directory in order to be able to reset it at the end of
        # the function
        last_cwd = os.getcwd()

        qgis_apps: list[Software] = get_qgis_apps()
        nb_qgis_app = len(qgis_apps)

        if nb_qgis_app == 0:
            print_formatted_text(
                """Aucune version de QGIS n'a été trouvée sur votre ordinateur.
Les modules Python ne peuvent pas être installés de manière automatique.
Veuillez vous rapprocher d'un administrateurs qui pourra réaliser l'installation
de manière manuelle."""
            )
        elif nb_qgis_app == 1:
            qgis_app = qgis_apps[-1]
            print_formatted_text(
                "Une version de QGIS a été trouvée sur votre ordinateur :"
            )
            print_formatted_text(f"{qgis_app}")

            # Install packages for the specified QGIS app
            _install_python_packages_for_qgis_app(qgis_app)

        else:
            print_formatted_text(
                "Liste des versions de QGIS trouvées sur votre ordinateur :"
            )
            for index, qgis_app in enumerate(qgis_apps):
                print_formatted_text(f"{index+1} - {qgis_app}")

            version_completer = WordCompleter(
                [f"{index+1} - {qgis_app}" for index, qgis_app in enumerate(qgis_apps)],
                ignore_case=True,
            )
            session = PromptSession(completer=version_completer)
            text = session.prompt(
                "Pour quelle version de QGIS voulez-vous installer les modules Python ? > "
            )
            qgis_app_index = int(text[0])
            if qgis_app_index == 0:
                raise DontContinueException
            elif qgis_app_index > nb_qgis_app:
                raise DontContinueException
            else:
                qgis_app = qgis_apps[qgis_app_index - 1]
                print_formatted_text(f"Vous avez choisi {qgis_app} :")
                _install_python_packages_for_qgis_app(qgis_app)

    except DontContinueException:
        pass
    except NotOnWindowsException:
        print_formatted_text("Ce programme ne peut fonctionner que sous Windows.")
        print_formatted_text("Vous ne semblez pas utiliser Windows.")

    # Set back the current working directory
    if last_cwd:
        os.chdir(last_cwd)

    # End message
    print_formatted_text("")
    print_formatted_text("Fin du programme")

    prompt("Pressez la touche entrée pour quitter...")


def main():
    install_python_packages_in_qgis()


if __name__ == "__main__":
    main()
