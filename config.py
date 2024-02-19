#from selenium import webdriver
import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager
import os
import subprocess
from time import sleep
from selenium.webdriver.common.proxy import Proxy

class verifyPaths:

    def acess_to_chrome(self, path:str=fr"C:\Program Files\Google\Chrome\Application\chrome.exe") -> str:
        if os.path.isfile(path):
            return path
        else:
            return None
        
    
    def acess_to_chromedriver(self, path:str=fr"C:\Program Files\chromedriver") -> str:
        try:
            if os.path.exists(path):
                return path
            else:
                local_app_data = os.environ.get('LOCALAPPDATA')
                return local_app_data + fr"\chromedriver"
        except:
            return None
        

    def _for_path_in_path(self, paths: list) -> str:
        for path in paths:
            if os.path.isfile(path):
                print(f"O path {path} foi encontrado:")
                return path
        return False


    def is_google_chrome_installed(self, paths:list=[]) -> str:
        if paths:
            verify = self._for_path_in_path(paths)
        else:
            diretorio_atual = os.path.abspath(os.getcwd())
            possible_paths = [
                fr"{diretorio_atual}\Win_1147503_chrome-win\chrome-win\chrome.exe",
                fr"{diretorio_atual}\Selenium\Win_1147503_chrome-win\chrome-win\chrome.exe"
            ]
            verify = self._for_path_in_path(possible_paths)
        return verify
    

    def is_google_chromedriver_installed(self, paths:list=[]) -> str:
        if paths:
            verify = self._for_path_in_path(paths)
        else:
            diretorio_atual = os.path.abspath(os.getcwd())
            possible_paths = [
                fr"{diretorio_atual}\chromedriver-win32\chromedriver.exe",
                fr"{diretorio_atual}\Selenium\chromedriver-win32\chromedriver.exe"
            ]
                
        verify = self._for_path_in_path(possible_paths)
        return verify
    

class ConfigSelenium(verifyPaths):
    def __init__(self, paths=[]):
        super().__init__()
        self.lista = []
        self.driver = None
        self.verificar = False
        self.paths = paths
        self.options = uc.ChromeOptions()

    
    def __SetarPathPadraoChrome(self, comand:str="C:\Program Files\Google\Chrome\Application") -> str:
        path = self.is_google_chrome_installed(self.paths)
        if path:
            navegador = self.acess_to_chrome(path)
            if not navegador:
                navegador = self.acess_to_chrome(comand)
            return navegador
        else:
            return None
        
    
    def __SetarPathPadraoChromedriver(self, comand:str=fr"C:\Program Files\chromedriver") -> str:
        path = self.is_google_chromedriver_installed(self.paths)
        if path:
            driver = self.acess_to_chromedriver(path)
            if not driver:
                driver = self.acess_to_chromedriver(comand)
            return driver
        else:
            return None
        

    def __ExecuteOptions(self, options) -> True:
        if options:
            if isinstance(options[0], dict):
                for op in options[0]:
                    for value in op.items():
                        self.options.add_argument(value)
            elif isinstance(options[0], list):
                for op in options[0]:
                    self.options.add_argument(op)
            else:
                for op in options:
                    self.options.add_argument(op)
            return True
        else:
            print("SEM OPÇÕES CHAMADAS")
            return False


    def __ExecuteProxy(self, proxy:Proxy) -> True:
        if proxy:
            proxy.add_to_capabilities(self.options.to_capabilities())
            return True
        else:
            print("Não há proxys chamados")
            return False


    def ConfigChrome(self, *options: tuple, install_chrome_driver:bool=False, proxy:Proxy=None) -> None:
        if install_chrome_driver:
            d = self.__SetarPathPadraoChromedriver()
            if d:
                if os.path.exists(d):
                    self.__ExecuteOptions(options)
                    self.__ExecuteProxy(proxy)
            else:
                print("Chromedriver não encontrado.")
                # Crie uma instância personalizada de ChromeDriverManager com o caminho personalizado
                custom_chromedriver_manager = ChromeDriverManager().install()

                print(f"O diretório padrão do chromedriver é: {custom_chromedriver_manager}")
                print(f"Pode setá-lo em seu diretório")
                # Após a instalação, chromedriver deve estar disponível no PATH
                print("Chromedriver instalado com sucesso!")
            print("Abrindo a configuração do CHROME via driver")
            self.driver = uc.Chrome(options=self.options, driver_executable_path=d)
            return True
        else:
            d = self.__SetarPathPadraoChrome()
            if os.path.exists(d):
                self.options.binary_location = d
                self.__ExecuteOptions(options)
                self.__ExecuteProxy(proxy)
            else:
                print("Binário do chrome não encontrado")
                return None
            print("Abrindo a configuração do CHROME via binário")
            self.driver = uc.Chrome(options=self.options)
            return True
        

    def __FecharViaTerminal(self, view_text=False):
        try:
            subprocess.run(['taskkill', '/f', '/im', 'chrome.exe'], check=True)
            if view_text:
                print("processos removidos com êxito")
            return True
        except:
            print("Não há processos abertos!")
            return False


    def __FecharViaDriver(self):
        try:
            self.driver.close()
            sleep(5)
            self.driver.quit()
            return True
        except:
            return False


    def CloseTheDriver(self, remove_exe:bool=False, force_remove:bool=False) -> None:
        verify = False
        if remove_exe and force_remove == False:
           verify = self.__FecharViaDriver()
        elif force_remove and remove_exe == False:
            verify = self.__FecharViaTerminal(view_text=True)
        else:
            from prettytable import PrettyTable
            print("Fechando o navegador e o exe")
            x = self.__FecharViaDriver()
            y = self.__FecharViaTerminal()
            dados = [["remove_exe=True", "force_remove=True"], [f"Fechou via Driver: {x}", f"Fechou via Terminal: {y}"]]
            tabela = PrettyTable()
            tabela.field_names = ["Remover Via Selenium", "Remover via terminal"]
            # Adicione os dados à tabela
            for linha in dados:
                tabela.add_row(linha)

            print(tabela)
            verify = True if dados[1][0] or dados[1][1] else False
        print("Terminando processo de fechamaneto de execução")
        return verify


def ConfigOptions(*keys, tamanho=[], language="pt-BR", view_keys=False):
    options = {
        0: "--disable-notifications",
        1: "--ignore-certificate-errors",
        2: "--headless", 
        3: f"--window-size={str(tamanho[0])},{str(tamanho[1])}" if tamanho else "--start-maximized",
        4: "--disable-gpu",
        5: "--disable-extensions",
        6: "--disable-infobars",
        7: "--disable-popup-blocking",
        8: "--no-sandbox",
        9: "--disable-logging",
        10: "--disable-background-networking",
        11: f"--lang={language}",
        12: "--enable-javascript",
    }
    if view_keys:
        print("OPÇÕES DISPONÍVEIS:")
        for c, v in options.items():
            if c == 3:
                print(f"Insira a chave {c} para gerar a opção padrão --start-maximized")
                print(f"Insira a chave {c} com parâmetro tamanho para gerar: --window-size=str(tamanho[0]),str(tamanho[1])")
            else:
                print(f"Insira a chave {c} para gerar a opção {v}")
        print("Caso queira todas as opções, ele será retornado por padrão!")
    if keys:
        l = []
        for k in keys:
            l.append(options[k])
        return l
    return options


def ConfigProxy(proxy_host, proxy_port):
    # Criando objeto Proxy
    proxy = Proxy({
        'proxyType': 'manual',
        'httpProxy': f"{proxy_host}:{proxy_port}",
        'sslProxy': f"{proxy_host}:{proxy_port}",
    })
    return proxy


if __name__ == "__main__":
    v = ConfigSelenium()
    print(v.ConfigChrome())
    print(v.CloseTheDriver(True, True))
