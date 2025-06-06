### Installation
**1. Create a Folder where you want to save the project**

**2. Create a Virtual Environment and Activate**

Install Virtual Environment First for linux
```
$  pip install virtualenv
```

Create Virtual Environment

For Windows
```
$  python -m venv venv
```
For Mac
```
$  python3 -m venv venv
```
For Linux
```
$  virtualenv .
```

Activate Virtual Environment

For Windows
```
$  venv/scripts/activate
```

For Mac
```
$  source venv/bin/activate
```

For Linux
```
$  source bin/activate
```

**3. Clone this project**
```
$  git clone https://github.com/karnnan1947/cryptopredictions.git
```

Then, 
```
$ activate environment crypt
Enter the project
$ cd cryptopredict
```

**4. Install Requirements from ‘requirements.txt’**
```python
$  pip3 install -r requirements.txt
```

**5. Run migrations**
```python 
$  python manage.py makemigrations
```

**5.1 and Migrate**
```python 
$  python manage.py migrate
```

**6. Now Run Server**

Command for PC:
```python
$ python manage.py runserver
```

Command for Mac:
```python
$ python3 manage.py runserver
```

Command for Linux:
```python
$ python3 manage.py runserver
```

**7. Login Credentials**

Create Super User 
Command for PC:
```
$  python manage.py createsuperuser
```

Command for Mac:
```
$  python3 manage.py createsuperuser
```

Command for Linux:
```
$  python3 manage.py createsuperuser
```

<video width="640" height="360" controls>
  <source src="https://raw.githubusercontent.com/karnnan1947/cryptopredictions/mains/demovideo.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

[CryptoCurrency Price Prediction Demo Video](https://drive.google.com/file/d/1EkajLSd3esur-UQwrIbmV8Vbn4X8sIqY/view)
