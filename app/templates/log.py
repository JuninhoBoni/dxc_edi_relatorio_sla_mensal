import logging
from datetime import datetime
from pathlib import Path

class Log:
    
    def carregar(self):
        agora = datetime.now()
        
        diretorio_log = f'{self.args["dados_json"]["diretorio"]["log"]}/{agora.year:04d}{agora.month:02d}{agora.day:02d}/'
        
        nome_log = f'{self.args["programa_nome"]}_{agora.hour:02d}{agora.minute:02d}.LOG'

        Path(diretorio_log).mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(filename=f'{diretorio_log}{nome_log}',
                            format='%(asctime)s -- %(message)s', datefmt='%d/%m/%Y %H:%M:%S', level=logging.DEBUG)

    def info(self, mensagem):
        print(mensagem)
        logging.info(mensagem)
        
    def error(self, mensagem):
        print(mensagem)
        logging.error(mensagem)
        erro = "X"+' PROGRAMA FINALIZADO COM ERRO '.center(120,"-")+"X"
        logging.error(erro)
        print(erro)