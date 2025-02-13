import subprocess

def install_missing_libraries():
    with open('requirements.txt', 'r') as file:
        libraries = file.read().splitlines()
        
    for library in libraries:
        try:
            __import__(library)
            print(f"{library} is already installed.")
        except ImportError:
            subprocess.check_call(['pip', 'install', library])
            print(f"{library} is now installed.")

def run_main_project():
    subprocess.check_call(['python', 'app.py'])

if __name__ == '__main__':
    install_missing_libraries()
    run_main_project()
