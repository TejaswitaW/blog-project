cd .\venv\
venv> .\Scripts\activate
venv> cd ..
pip install django==3.1.5
pip freeze > requirements.txt  
django-admin startproject my_site
cd my_site
django-admin startapp blog
python .\manage.py runserver
