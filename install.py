import subprocess
import sys

pacotes = [
    'flask',
    'flask-sqlalchemy',
    'sqlalchemy2-stubs',
    'flask-jwt-extended',
    'flask-bcrypt'
]


if __name__ == '__main__':
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', *pacotes])
    except subprocess.CalledProcessError as e:
        print('\n\nNão foi possível instalar:', e)