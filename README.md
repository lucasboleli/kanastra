# kanastra
pip install django
pip install djangorestframework
django-admin startproject kanastra

```
name,governmentId,email,debtAmount,debtDueDate,debtId
John Doe,11111111111,johndoe@kanastra.com.br,1000000.00,2022-10-12,1adb6ccf-ff16-467f-bea7-5f05d494280f 
```
docker-compose exec backend python manage.py import_csv path/to/yourfile.csv


docker compose exec backend sh
    python manage.py makemigrations
    python manage.py migrate