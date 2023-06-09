# ikeaoffers

👀 Watching at IKEA offers...

![Logo Ikea](./ikea_logo.svg)

> This tool lets you track some IKEA products and be notified when any offer appears.

## Setup

1. Create a Python virtualenv (>=3.10)
2. `pip install -r requirements.txt`
3. Add custom values in `.env` file for the following params:
   - `SENDGRID_APIKEY`
   - `SENDGRID_FROM_ADDR`
   - `SENDGRID_FROM_NAME`
4. Add tracking info in `config.yaml`:

```yaml
users:
  - name: Bart
    email: bart@simpsons.org
    track:
      - https://www.islas.ikea.es/tenerife/es/pd/ronninge-odger-mesa-y-4-sillas-antracita-spr-09429059
      - https://www.islas.ikea.es/tenerife/es/pd/vedbo-mesa-de-comedor-160cm-de-longitud-blanco-art-10417456
  - name: Lisa
    email: lisa@simpsons.org
    track:
      - https://www.islas.ikea.es/tenerife/es/pd/sunneby-molnart-lampara-techo-bombilla-spr-09491225
      - https://www.islas.ikea.es/tenerife/es/pd/skurup-lampara-de-techo-turquesa-art-20508106
```

## Usage

1. Launch application:

```console
$ python main.py run
```

> You can change loglevel using: `-linfo` `-ldebug` `-lerror`

2. Clear temp database:

```console
$ python main.py clear
```

> A bunch of files `tracking.dbm*` are created to store notifications. You can remove these files. Do it under your own responsibility.
