

## Image
![image](https://www.uplooder.net/img/image/65/7d3ab5d0eb8a405d6d64c284c1184547/image-2023-04-20-071456327.png)





___Clone This Project (Make Sure You Have Git Installed)___
``` git
git clone https://github.com/itdevx/Blog-technology.git
```
___Create Virtualenv___
```
cd Blog-technology
python -m venv venv
```
___Activate virtualenv___
```
cd venv/Script/activate
```
___Install Dependencies___
```
pip install -r requirements.txt
```
___Set Database (Make Sure you are in directory same as manage.py)___
```
python manage.py makemigrations
python manage.py migrate
```
___Create SuperUser___
```
python manage.py createsuperuser
```
### After all these steps , you can start testing and developing this project.