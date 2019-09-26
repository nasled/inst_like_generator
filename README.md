# inst_like_generator
GUI bot that scrolls Instagram feed and sets Like to each post (if not set yet) to save time.

The script uses Selenium (geckodriver), CV2, numpy, Beautifulsoup and pyautogui librares. 

## How to Deploy

### Shell into Virtual Environment
```
pipenv shell
```

### Install Dependencies
```
pipenv install
```

## How to Use

Adjust LOGIN, PASSWORD and SCROLL_TO_PX variables for your needs.

```
LOGIN = "347123456"
PASSWORD = "password"
SCROLL_TO_PX = 30000
```

### Run Script
```
python ./main.py
```
   
### Enjoy!