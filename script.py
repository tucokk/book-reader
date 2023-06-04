from undetected_chromedriver import Chrome
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import configparser
import os, sys

class WebDriver:
    def __init__(self) -> None:
        
        path = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
        self.DRIVER = Chrome(use_subprocess=True, browser_executable_path=path); # Driver que será utilizado    

class ConfigReader:
    def __init__(self) -> None:

        self.EMAIL    = "" # E-mail que será utilizado para log-in na plataforma
        self.PSW      = "" # Senha que será utilizado para log-in na plataforma
        self.PAGETIME = "" # Tempo em que o script lerá cada página

        self.read()
    
    def read(self):
        parser = configparser.ConfigParser()
        path = Path().absolute()
        try:
            parser.read(rf'{path}\\config.ini')
        
            temp_email    = parser.get('Configs', 'email')       # Lê o e-mail descrito no arquivo de configuração
            temp_psw      = parser.get('Configs', 'psw')         # Lê a senha descrita no arquivo de configuração
            temp_pagetime = parser.getint('Configs', 'pagetime') # Lê o tempo de página descrito no arquivo de configuração

            if not temp_email == '' and not temp_email == 'email@email.com':
                self.EMAIL = temp_email
            else:
                return
            
            if not temp_psw == '' and not temp_psw == 'senha12345':
                self.PSW = temp_psw
            else:
                return

            if not temp_pagetime == '' and temp_pagetime >= 5:
                self.PAGETIME = temp_pagetime
            else:
                return  
        except:
            return

class WebPage(WebDriver, ConfigReader):
    def __init__(self) -> None:
        self.DRIVER = WebDriver().DRIVER # Driver que será utilizado    
        self.URL    = "https://leiaparana.odilo.us/?locale=pt" # URL da plataforma

        self.EMAIL    = ConfigReader().EMAIL    # E-mail que será utilizado para log-in na plataforma
        self.PSW      = ConfigReader().PSW      # Senha que será utilizado para log-in na plataforma
        self.PAGETIME = ConfigReader().PAGETIME # Tempo em que o script lerá cada página
        
        print(self.EMAIL   )
        print(self.PSW     )
        print(self.PAGETIME)
        self.browse()
    
    def browse(self):
        self.DRIVER.get(self.URL)
    
    def click(self, strpath): # Função de clicar
        WebDriverWait(self.DRIVER, 20).until(
            EC.visibility_of_element_located((By.XPATH, strpath))
        ).click()
    
    def write(self, type, strpath, strtext): # Função de escrever
        if   type == "xpath":
            WebDriverWait(self.DRIVER, 20).until(
                EC.visibility_of_element_located((By.XPATH, strpath))
            ).send_keys(f'{strtext}\n')
        elif type == "name":
            WebDriverWait(self.DRIVER, 20).until(
                EC.visibility_of_element_located((By.NAME, strpath))
            ).send_keys(f'{strtext}\n')
        
    def read(self, strpath): # Função de ler
        return self.DRIVER.find_element(By.XPATH, strpath).text

    def switch_window(self):
        self.DRIVER.switch_to.window(self.DRIVER.window_handles[-1])

if __name__ == "__main__":

    ###### Abrindo o objeto de classe ######
    webpage = WebPage()

    ###### Recusando o aviso de cookies ######
    sleep(1) 
    webpage.click('//*[@id="mat-dialog-0"]/app-cookies-dialog/div/div[2]/div/button[1]') # Recusa Cookies
    webpage.click('/html/body/app-root/div[2]/app-header/mat-toolbar/mat-toolbar-row/button[3]/span/span[2]') # Clica em "identificar-se"
    
    ###### Realizando o log-in na plataforma pela Google ######
    webpage.write('name', 'identifier', webpage.EMAIL) # Escreve o e-mail na caixa de texto
    webpage.write('xpath', '//*[@id="password"]/div[1]/div/div[1]/input', webpage.PSW) # Escreve a senha na caixa de texto
    
    ###### Acessando a área de empréstimos ######
    sleep(5)
    webpage.URL = 'https://leiaparana.odilo.us/user/checkouts' # Seta o novo link
    webpage.browse() # Redireciona a aba para a página de empréstimos

    ###### Acessando o livro ######
    sleep(2)
    webpage.click('/html/body/app-root/div[3]/app-user/div/div[2]/app-user-checkouts/div/app-record-card-grid/div/app-user-checkout-item/app-card-item/app-record-card-generic/div/div[2]/div[2]/app-record-buttons/div/app-download-button/button') # Clica em "acessar"

    ###### Lê o livro ######
    sleep(10)
    webpage.switch_window() # Foca o script na aba do livro

    while True:
        sleep(webpage.PAGETIME)

        percent = webpage.read('//*[@id="main"]/div[3]/div/div[1]/div[3]')
        if percent == '100%':
            break
            
        webpage.click('//*[@id="right-page-btn"]')
