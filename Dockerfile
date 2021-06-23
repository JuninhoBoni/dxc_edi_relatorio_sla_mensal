FROM python:3.9

RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "/app/main.py"]
CMD ["python", "/app/dxc_edi_relatorio_sla_mensal.py"]