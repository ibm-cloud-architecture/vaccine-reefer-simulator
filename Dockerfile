FROM node:12 AS frontend

WORKDIR /usr/src/app

COPY ./ui/package.json ./
COPY ./ui/yarn.lock ./

RUN yarn install

COPY ./ui .

RUN yarn build


FROM python:3.7.4-stretch
ENV PATH=/root/.local/bin:$PATH

ENV PYTHONPATH=/app

WORKDIR /app

RUN pip install --upgrade pip \
  && pip install pipenv flask gunicorn

COPY Pipfile .
COPY Pipfile.lock .
COPY requirements.txt .

# First we get the dependencies for the stack itself
RUN pipenv lock -r > requirements.txt
RUN pip install -r requirements.txt

COPY . /app
COPY --from=frontend /usr/src/app/dist /app/api/dist/

EXPOSE 5000
CMD ["gunicorn", "-w 4", "-b 0.0.0.0:5000", "app:app"]
