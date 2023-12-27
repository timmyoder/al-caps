FROM python:3.11

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . ./

EXPOSE 2222
CMD gunicorn -b 0.0.0.0:8000 app:server

# docker build -t al-caps .
# docker tag al-caps tybirthright.azurecr.io/al-caps
# docker run -p 8000:8000 --restart always --name meter-cost -d meter-cost
# az login
# az acr login --name tybirthright
# docker push tybirthright.azurecr.io/al-caps