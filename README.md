## Codename Wolves

* [Instagram Account](https://www.instagram.com/codename.wolves/)

#### Used

* Python 3.11.2
* reddit api -> https://github.com/praw-dev/praw
* instagram api -> https://github.com/adw0rd/instagrapi
* image generator -> tryleap.ai

#### Creds

#### Process

* Generate model tuning images from subreddit (`r/battlestations`)

```bash
python3 get_imgs.py -s battlestations
```

* Tune model

```bash
python3 img_model.py -p battlestations_imgs -k @desk -t battlestation_model_v1
```
