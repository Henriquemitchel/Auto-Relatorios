from selenium import webdriver  
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime,timedelta 
from selenium.webdriver.support.ui import Select
import pyotp

secret = "EXEMPLO"
totp = pyotp.TOTP(secret)
code = totp.now()
#Pegando o codigo da autenticação de 2 fatores

navegador = webdriver.Chrome()
navegador.get("PAGINA LOGIN")
navegador.maximize_window()
#Maximiza a tela

botao_coockie = navegador.find_element("css selector", ".btn.btn-primary.aceite-cookie")
botao_coockie.click()
#Encontra o botão de aceitar coockies e clica para fechar

navegador.find_element("id", "usuario").send_keys("USUARIO") 
navegador.find_element("id", "senha").send_keys("SENHA")
navegador.find_element("id", "autenticacao_fma" ).send_keys(code)
#Insere as informações de login

secret = "EXEMPLO DE SECRET"
totp = pyotp.TOTP(secret)
code = totp.now()
print(code)

botao_entrar = navegador.find_element("css selector", ".btn.btn-primary")
botao_entrar.click()
#Clica no botão entrar pela primeira vez

botao_entrar = WebDriverWait(navegador, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".btn.btn-primary"))
)
navegador.execute_script("arguments[0].click();", botao_entrar)
#Aguarde o botão aparecer na tela novamente e clica

time.sleep(5)

navegador.get("PAGINA RELATORIOS")
#Com o login ja realizado, entra diretamente na pagina de relatorios pelo link

def periodo_relatorio():

    hoje = datetime.now()
    dia_semana = hoje.weekday()

    if dia_semana == 0:
        data_incial = hoje - timedelta(days=3)
        data_final = hoje - timedelta(days=2)
    else: 
        data_incial = hoje - timedelta(days=1)
        data_final =  hoje - timedelta(days=1)
    
    return data_incial, data_final
#Verifica se o dia atual é segunda feira. Se sim, puxa sexta e sabado, se não, puxa o dia anterior

data_incial, data_final = periodo_relatorio()

navegador.find_element("id", "dfsDataContratoInicial").send_keys(
    data_incial.strftime('%d/%m/%y'))
navegador.find_element("id", "dfsDataContratoFinal").send_keys(
    data_final.strftime('%d/%m/%y'))
#Formata as datas para inserir nos campos

navegador.find_element("id", "cmbLayoutRelatorio").click()
caixa = navegador.find_element(By.ID, "cmbLayoutRelatorio")
select = Select(caixa)
select.select_by_visible_text("FECHAMENTO DIARIO")
#Abre o modal do tipo de relatorio e seleciona

time.sleep(3)

navegador.find_element("id", "pbSalvar").click()

time.sleep(20)
 