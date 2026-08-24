Aktivace virtuálního prostředí:
source .venv/bin/activate

Základní spuštění:
python main.py

Grafická simulace:
python main.py --visual

Simulace bez grafického okna:
python main.py --headless

Jedna simulace s výpisem počtu živých buněk po každém kroku:
python main.py --single

Například 50 kroků:
python main.py --single --iterations 50

Monte Carlo simulace, například 1000 běhů:
python main.py --monte-carlo 1000

Monte Carlo 1000 běhů po 50 krocích:
python main.py --monte-carlo 1000 --iterations 50

Změna velikosti mřížky:
python main.py --visual --rows 50 --cols 50

Kombinace parametrů:
python main.py --monte-carlo 1000 --rows 50 --cols 50 --iterations 50

Výchozí hodnoty pro rows, cols a iterations jsou nastavené v constants.py.