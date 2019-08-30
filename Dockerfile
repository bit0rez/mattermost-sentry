FROM python:3-alpine

WORKDIR /opt

# Install requirements at first.
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Run test
#RUN cp config.py.sample config.py \
#    && python test.py \
#    && rm test.py config.py.sample config.py

EXPOSE 8080
CMD ["python", "app.py"]

