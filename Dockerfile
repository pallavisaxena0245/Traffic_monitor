# Dockerfile
FROM python:3.10-slim

#Install mitmproxy and other tools
RUN apt-get update && apt-get install -y tcpdump && apt-get clean && pip install mitmproxy

# Create a directory for 
RUN mkdir /logs

#Set default command for mitmproxy
CMD ["mitmdump","--mode","transparent", "showhost", "--save-stream-file", "/logs/traffic.log"]
