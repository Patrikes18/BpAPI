# API pre fuzzy frakcionálne farbenie

Táto zložka obsahuje zdrojové kódy pre API. 

# Návod na nasadenie

## Docker

V zložke BpAPI/ je Dockerfile, pomocou ktorého je možne vytvoriť docker image a ten následne nasadiť na server. Návod funguje, ak má užívateľ nainštalovaný Docker a je v zložke BpAPI/.

1. Docker image vytvoríte pomocou príkazu:

```bash
docker build . -t <nazov_image>
```

2. Spustite vytvorený image a nastavte port, na ktorom bude API dostupné pomocou príkazu:

```bash
docker run -d -p <port>:5000 --name <kontajner> <image>
```

## Flask

Pre spustenie pomocou Flasku je potrebné mať nainštalovaný python3.10. Ďalej je potrebné vytvoriť si virtuálne prostredie, venv a v ňom nainštalovať všetky knižnice zo súboru requirements.txt. Potom stačí len spustiť API pomocou príkazu:

```bash
flask --app index.py run
```

Aplikácia v bežnom režime pobeží na porte 5000. Ak by bolo potrebné použiť iný port, tak sa musí pred spustením nastaviť premenná prostredia FLASK_RUN_PORT na požadovaný port.