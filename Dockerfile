FROM python:3-alpine
RUN apk add alpine-sdk postgresql python-dev postgresql-dev --update
RUN pip3 install dash && \
  pip3 install dash-renderer && \
  pip3 install dash-html-components && \
  pip3 install dash-core-components && \
  pip3 install plotly

RUN pip3 install --upgrade setuptools && pip3 install --default-timeout=100 psycopg2 numpy

# RUN pip3 install numpy
COPY *.py /src/
EXPOSE 8080 8050
CMD ["python3", "/src/application.py"]
