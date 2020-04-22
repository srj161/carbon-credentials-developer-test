# carbon-credentials-developer-test

## Installation
From the carbon-credentials-developer-test directory, run the following to build a vitualenv and install requirements.
```bash
pip install virtualenv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

To run migrations:
```bash
make init
```

To run tests:
```bash
make test
```

To run django server:
```bash
make run
```
This is then accessible from your browser at http://127.0.0.1:8000/
