### Codename Wolves

* [Instagram Account](https://www.instagram.com/codename.wolves/)

<br>

#### Used

* Python 3.11.2
* Images: [PRAW - Reddit API Wrapper](https://praw.readthedocs.io/en/stable/)
* Instagram: [InstagrAPI](https://adw0rd.github.io/instagrapi/)
* Image Prompt+Caption: [OpenAI - ChatGPT API](https://openai.com/blog/openai-api)
* AI Image Generation: [TryLeapAI](https://www.tryleap.ai/)

<br>

#### Creds

* `ig_user`: Instagram username
* `ig_pass`: Instagram password
* `leapai_key`: TryLeapAI API Key
* `openai_key`: OpenAI API Key

<br>

* Setup

```bash
# copy to correct name and fill in with creds
cp _config.py config.py
```

<br>

#### Improvements

* Automate IG account creation and validation
* IG growth strategy - can automate via Instagrapi package
* Getting images, where to get them?
* Types of images, influencers, vibes?
* How to handle image model prompting?
* How to increase variation

<br>

#### Process

* Install deps

```bash
pip3 install -r requirements.txt
```

* Generate model tuning images from subreddit (`r/battlestations`)

```bash
python3 get_imgs.py -s battlestations
```

* Tune model

```bash
python3 img_model.py -p battlestations_imgs -k @desk -t battlestation_model_v1
```

* Create image and post to IG

```bash
python3 influence.py -m <model_id> -s battlestations -k @desk
```
