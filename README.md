## Usage

This is a simple script to generate a bunch of UA-CH GREASE headers to run against top sites and look for breakage. It's probably full of bugs, and hard-codes all kinds of assumptions, so patches welcome.

```
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```

Then you can run it via `python3 fuzz.py`.
