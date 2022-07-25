FROM python:3.9.10

WORKDIR /usr/src/CanalserviceApp

RUN apt-get update
RUN apt install -y libgl1-mesa-glx

COPY . /usr/src/CanalserviceApp/
RUN python -m venv /venv
#RUN source venv/bin/activate
ENV PATH=/venv/bin:$PATH
ENV TELEGRAM_BOT_TOKEN="PLACE_YOUR_TOKEN_HERE"
#RUN echo $TELEGRAM_BOT_TOKEN
RUN pip install -r requirements.txt

EXPOSE 3000
EXPOSE 5432/udp
EXPOSE 5432/tcp
CMD ["/venv/bin/python", "main.py"]
