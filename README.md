# kanastra
pip install django

pip install djangorestframework

django-admin startproject kanastra


```
name,governmentId,email,debtAmount,debtDueDate,debtId
John Doe,11111111111,johndoe@kanastra.com.br,1000000.00,2022-10-12,1adb6ccf-ff16-467f-bea7-5f05d494280f 
```


docker compose exec backend sh
    python manage.py makemigrations
    python manage.py migrate

Para rodar a leitura do arquivo:

docker-compose exec backend python manage.py import_csv csv/test.csv
docker compose exec backend python manage.py makemigrations
docker compose exec backend python manage.py migrate


Example request using Postman:
Set the method to POST
Enter the URL: http://localhost:8000/api/charge/
Go to the Body tab, and select form-data
Add a key file, select File as its type, and choose the CSV file to upload