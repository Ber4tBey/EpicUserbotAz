# FROM kısmını Değiştirmeyiniz Epicye DockerFile Kullanın

FROM erdembey/epicuserbot:latest
RUN git clone https://github.com/ByMisakiMey/EpicUserBotAz /root/EpicUserBotAz
WORKDIR /root/EpicUserBotAz/
RUN pip3 install -r requirements.txt
CMD ["python3", "main.py"]  
