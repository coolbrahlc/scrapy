alembic revision -m "create books table"

.venv + requirements
alembic

pip freeze >>requirements2.txt
alembic init alembic
alembic revision -m "create books"
alembic upgrade head




scrapy crawl books -o file.json -t json