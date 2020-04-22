# messages-gpt2

## Setup

```sh
git clone https://github.com/lolney/messenger-gpt2-chatbot.git
cd server
virtualenv -p python3.7 server
source server/bin/activate
pip install -r requirements.txt
```

## Running tests

`(cd server && python -m pytest)`

## Generating the model

1. Download your Facebook data
2. Clone Chatistics
3. Follow the instructions in the Chatistics rep to parse the Messenger data
4. `python export.py --format json`
5. `python parse_input.py`
6. `python create_model.py`

## Running the server

`python app.py`

## Pushing to Google Cloud Run

Instructions from here: https://github.com/minimaxir/gpt-2-cloud-run

```
sudo docker build . -t messenger-gpt2
sudo docker tag messenger-gpt2 gcr.io/euphoric-coral-257209/messenger-gpt2
sudo docker push gcr.io/euphoric-coral-257209/messenger-gpt2
```

Go to https://console.cloud.google.com/run and set Memory Allocated to 2 GB and Maximum Requests Per Container to 1!
