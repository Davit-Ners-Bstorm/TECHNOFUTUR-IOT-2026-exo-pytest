# Smart IoT Environment Monitor

Support pédagogique Python 3.12+ pour une journée consacrée à PyTest. Le projet simule des capteurs de température, d'humidité et de qualité de l'air, sans réseau ni matériel réel.

## Ce que le projet permet de tester

- règles métier et valeurs frontières ;
- `pytest.raises` et exceptions personnalisées ;
- `pytest.mark.parametrize` ;
- fixtures locales et partagées via `conftest.py` ;
- `unittest.mock.Mock`, `return_value`, `side_effect` et assertions d'appels ;
- collecte multi-appareils, tolérance aux pannes et alertes ;
- marqueurs `unit`, `integration` et `hardware` ;
- exemples secondaires de `skip` et `xfail`.

## Installation

Sous PowerShell :

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Sous macOS ou Linux :

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Lancer les tests

Privilégier `python -m pytest` : cela utilise avec certitude l'interpréteur actif.

```bash
python -m pytest
python -m pytest -v
python -m pytest -m unit
python -m pytest -m integration
python -m pytest tests/test_device.py
python -m pytest tests/test_device.py::test_read_sensor_returns_hardware_value
python -m pytest -k boundary
```

## Lancer la démonstration

```bash
python demo.py
```

Le script crée deux capteurs purement simulés, affiche une alerte et produit un rapport de flotte. Il ne nécessite aucun matériel.

## Architecture

```text
iot/
├── sensors.py       # frontières simulant le matériel
├── models.py        # enums partagées
├── temperature.py   # règles de température
├── humidity.py      # règles d'humidité
├── air_quality.py   # règles AQI simplifiées
├── battery.py       # règles de batterie
├── alerts.py        # décision, message et notifier
├── device.py        # entité IoT et exceptions
└── controller.py    # flotte, collecte et rapport
tests/               # correction complète du formateur
```

Le capteur expose un `measurement_type`, ce qui permet au contrôleur de choisir la bonne classification. Le contrôleur isole les erreurs par appareil : une panne n'empêche pas les autres lectures.

Exemple de résultat :

```python
{
    "SENSOR-001": {
        "value": 35.2,
        "status": "CRITICAL",
        "battery": 80,
        "battery_status": "OK",
        "alert_sent": True,
    }
}
```

## Utilisation en formation

La version présente contient la correction. Avant distribution, le formateur peut masquer ou retirer `tests/`, puis donner `STUDENT_INSTRUCTIONS.md`. `TEACHER_GUIDE.md` propose le déroulé de la journée et `TEACHER_BUGS.md` décrit sept mutations volontaires. Aucun bug pédagogique n'est actif dans la version livrée.

## Choix volontairement simples

Il n'y a ni API web, ni base de données, ni MQTT, ni Docker. Les classes de `sensors.py` et `Notifier` sont des frontières abstraites destinées aux mocks ; elles ne parlent à aucun matériel réel.
