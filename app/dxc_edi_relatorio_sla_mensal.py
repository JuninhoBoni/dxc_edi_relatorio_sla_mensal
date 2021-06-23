versao = '0.1'

import json
import os
import sys
import win32api
import win32con
import win32security
from datetime import *
from Include.log import Log
import pandas as pd
from pathlib import Path

import smtplib, time, os, requests
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


class Email:
    def enviar(self):
        path, file = os.path.split(self.filename)
        self.linha = '<b>Pedimos a gentileza que nos encaminhe a última listagem de BINs AMEX atualizada em formato Excel para que possamos atualizar nosso Sistema.</b>'
        
        self.assinatura = 'Atenciosamente<br>DXC - Cards'
        self.termos = 'DXC Technology Company -- This message is transmitted to you by or on behalf of DXC Technology Company or one of its affiliates. It is intended exclusively for the addressee. The substance of this message, along with any attachments, may contain proprietary, confidential or privileged information or information that is otherwise legally exempt from disclosure. Any unauthorized review, use, disclosure or distribution is prohibited. If you are not the intended recipient of this message, you are not authorized to read, print, retain, copy or disseminate any part of this message. If you have received this message in error, please destroy and delete all copies and notify the sender by return e-mail. Regardless of content, this e-mail shall not operate to bind DXC Technology Company or any of its affiliates to any order or other contract unless pursuant to explicit written agreement or government initiative expressly permitting the use of e-mail for such purpose. --. '
        self.toaddrs = args['dados_json']['emails']
    
        msg = MIMEMultipart()
        msg['Subject'] = self.assunto
        msg['From'] = self.From
        #msg['To'] = ', '.join(self.emailTo.split(','))
        #msg['CC'] = ', '.join(self.emailCC.split(','))
        #msg['CCO'] = ', '.join(self.emailCCO.split(','))

        friendMsg = saudacao(int(time.strftime('%H')))
        
        html = f'''
        <html>
        <head>
        <meta http-equiv='Content-Type' content='text/html; charset='CP1252'>
        </head>
        <body>
            <div style='margin: 30; padding: .2em;'>
                <img src='cid:dxc.png' width='91' height='89' align='left'>                     
            </div>
            <br />
            <br />
            <br />
            <br />
            <br />
            <br />
            <div style='margin: 30; padding: .2em; font-family: Verdana, Geneva, sans-serif; font-size: 11px;'>
                <h3>{friendMsg} {self.args["dados_json"]["destino_name"]},</h3>
                <br /><br />
                {self.mensagem01}
                <br /><br />
                {self.mensagem02}
                <br /><br />
                Grato,
                <br /><br />
                {self.assinatura},
                <br />
                <br />
                <!-- <span style='font-size: 8px';>> Essa é uma mensagem automática, gentileza não responder.</span> -->
                <br />
                {self.termos}
            </div>
        </body>
        </html>
        ''' 
        #html = self.html
        msg.attach(MIMEText(html, 'html'))
        
        fp = open(f'{self.args["dados_json"]["diretorio"]["dirImg"]}/dxc.png', 'rb')
        msgImgDXC = MIMEImage(fp.read())
        fp.close()
        
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(self.filename, 'rb').read())
        part.add_header('Content-Disposition', 'attachment; filename=' + file + '')

        msgImgDXC.add_header('Content-ID', '<dxc.png>')

        msg.attach(msgImgDXC)
        msg.attach(part)
        try:
            server = smtplib.SMTP('smtp.svcs.entsvcs.com')
            server.sendmail(self.From, self.toaddrs, msg.as_string())
        except:
            log.info('ERRO NO SERVIDOR smtp.svcs.entsvcs.com. USANDO O SERVIDOR 138.35.24.152 COMO ALTERNATIVA')
            server = smtplib.SMTP('138.35.24.152')
            server.sendmail(self.From, self.toaddrs, msg.as_string())

        server.quit()

def saudacao(hour_now):
    if 6 < hour_now < 12:
        friendMsg = "Bom dia"
    elif 18 > hour_now >= 12:
        friendMsg = "Boa tarde"
    elif hour_now >= 18 or 0 <= hour_now <= 6:
        friendMsg = "Boa noite"
    return friendMsg


if __name__ == '__main__':
    args = {}
    args['inicio'] = datetime.now()
    args['programa_nome'] = os.path.basename(__file__)
    args['programa_diretorio'] = sys.path[0]

    with open(f'{args["programa_diretorio"]}/{args["programa_nome"][:-3]}.json', 'r') as json_file:
        args['dados_json'] = json.load(json_file)

    log = Log()
    log.args = args
    args['log'] = log
    log.carregar()
    log.info("X" + f' PROGRAMA {args["programa_nome"][:-3]} - v.{versao} - INICIADO'.center(120, "-") + "X")


    try:
        programa_diretorio = os.path.basename(__file__)
        log.info(
            "X" + f' DATA DE COMPILAÇÃO - {datetime.fromtimestamp(os.path.getctime(programa_diretorio))} '.center(120,
                                                                                                                  "-") + "X")
    except:
        programa_diretorio = f'{sys.path[0]}/{args["programa_nome"][:-3]}.exe'
        log.info(
            "X" + f' DATA DE COMPILAÇÃO - {datetime.fromtimestamp(os.path.getctime(programa_diretorio))} '.center(120,
                                                                                                                  "-") + "X")

    sd = win32security.GetFileSecurity(programa_diretorio, win32security.OWNER_SECURITY_INFORMATION)
    owner_sid = sd.GetSecurityDescriptorOwner()
    name, domain, type = win32security.LookupAccountSid(None, owner_sid)
    log.info("X" + f' PROMOVIDO POR: - {domain}//{name} '.center(120, "-") + "X")
    log.info(
        "X" + f' USUÁRIO EXECUÇÃO ATUAL - {win32api.GetUserNameEx(win32con.NameSamCompatible)} '.center(120, "-") + "X")
    
    log.info('INICIANDO REQUEST')
    try:
        #r = requests.get('http://127.0.0.1:5000/edistatusmensal/')
        r = requests.get('http://127.0.0.1:5000/edistatusmensalsqlserver/')
        retorno = r.json()
    except:
        tempo_exec = datetime.now() - args['inicio']
        log.info("X"+f' TEMPO DE EXECUÇÃO: {tempo_exec} '.center(120, "-")+"X")
        log.error("X"+f' VERIFICAR API '.center(120, "-")+"X")
        sys.exit(2)

    if retorno[0]['status'] == 'sucesso':
        log.info('REQUEST RETORNADA COM SUCESSO')
    
        info = retorno[2]

        parametros = retorno[1]['parametros']
        de_yyyymmdd = str(parametros['datainicio'])
        ate_yyyymmdd = str(parametros['datafim'])

        de = datetime.strptime(de_yyyymmdd, '%Y%m%d').strftime('%d/%m/%Y')
        ate = datetime.strptime(ate_yyyymmdd, '%Y%m%d').strftime('%d/%m/%Y')

        df = pd.json_normalize(info['retorno'])

        email = Email()
        email.args = args
        dirTemp = args["dados_json"]["diretorio"]["dirTemp"]
        Path(dirTemp).mkdir(parents=True, exist_ok=True)
        
        if not df.empty:
            df = df.drop(["INICIO_CONTEUDO", "FIM_CONTEUDO", "INICIO_ZERADOS", "FIM_ZERADOS"], axis=1)
            

        for adquirerid in args["dados_json"]["acquirersIds"]:
            log.info(f'INICIANDO PROCESSO PARA O ADQUIRENTE - {adquirerid}')
            filename = f'{dirTemp}/Relatorio_EDI_Conteudo_Zerado_{adquirerid}_{ate_yyyymmdd[:-2]}.csv'

            df_envio = df
            email.mensagem02 = f'No período solicitado acima, não há dados para exibir.'
            if not df.empty:
                df_envio = df.query(f'ACQUIRERID == {adquirerid}')
                email.mensagem02 = f'Quantidade de dados: {df_envio[df_envio.columns[0]].count()}.'

            df_envio.to_csv(filename, index=False, sep=';', decimal=',', encoding='cp1252')
            
            email.filename = filename
            email.assunto = f'[RELATÓRIO][EDI][{adquirerid}] - ARQUIVOS COM CONTEÚDO E ZERADO'
            email.mensagem01 = f'Segue relatório mensal do adquirente {adquirerid} com dados de {de} até {ate}.'
            email.From = 'NAO_RESPONDER <nao-responder@dxc.com>'
            log.info('INICIANDO ENVIO DE E-MAIL')
            email.enviar()
            os.remove(filename)
            log.info('E-MAIL ENVIADO COM SUCESSO')
            log.info(f'FIM DO PROCESSO PARA O ADQUIRENTE - {adquirerid}')
    else:
        tempo_exec = datetime.now() - args['inicio']
        log.info("X"+f' TEMPO DE EXECUÇÃO: {tempo_exec} '.center(120, "-")+"X")
        log.error("X"+f' VERIFICAR SERVIDOR SMTP '.center(120, "-")+"X")
        sys.exit(1)
        


    tempo_exec = datetime.now() - args['inicio']
    log.info("X"+f' TEMPO DE EXECUÇÃO: {tempo_exec} '.center(120, "-")+"X")
    log.info("X"+' PROGRAMA FINALIZADO COM SUCESSO '.center(120, "-")+"X")