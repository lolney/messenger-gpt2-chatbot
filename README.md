messages-gpt2

## Setup

```sh
git clone <...>
cd server
virtualenv -p python3.7 server
source server/bin/activate
```

## Running tests

`(cd server && python -m unittest discover --pattern "\*\_test.py")`

## Generating the model

1. Download your Facebook data
2. Clone Chatistics
3. Follow the instructions in the Chatistics rep to parse the Messenger data
4. `python export.py --format json`
5. `python parse_input.py`
6. `python create_model.py`

## Running the server

`python app.py`
