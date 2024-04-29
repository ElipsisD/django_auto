echo "$1"

if [ "$1" = "celery" ]; then
    echo "Run celery WORKER..."
    celery -A autoworld worker --loglevel=info
fi

if [ "$1" = "beat" ]; then
    echo "Run celery BEAT..."
    celery -A autoworld beat --scheduler django --loglevel=info
fi

if [ "$1" = "flower" ]; then
    echo "Run celery FLOWER..."
    celery -A autoworld flower INFO -port:5555
fi

if [ "$1" = "server" ]; then
  echo "Migrate..."
  python ./manage.py migrate --noinput

  echo "Collect static"
  python ./manage.py collectstatic --noinput
  
  echo "Run server..."
  gunicorn autoworld.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 600 --reload
fi
