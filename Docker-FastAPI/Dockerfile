FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./main.py /code/app/main.py

# Get secret EXAMPLE and output it to /test at buildtime
RUN --mount=type=secret,id=EXAMPLE,mode=0444,required=true \
   cat /run/secrets/EXAMPLE > /test

# Get secret SECRET_EXAMPLE and clone it as repo at buildtime
RUN --mount=type=secret,id=SECRET_EXAMPLE,mode=0444,required=true \
  git clone $(cat /run/secrets/SECRET_EXAMPLE)

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]