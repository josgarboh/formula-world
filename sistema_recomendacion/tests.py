from django.conf import settings
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
# For Chrome testing
from selenium.webdriver.chrome.webdriver import WebDriver as SeleniumWebDriver
# For Firefox testing
# from selenium.webdriver.firefox.webdriver import WebDriver as SeleniumWebDriver

from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


# Create your tests here.

# TEST SISTEMA DE RECOMENDACION
    # Acceder sin loguear y que redireccione a login
    # Loguearme y no votar aún -> Mensaje de información
#
    # Votar Circuito con usuario testvoto
    # Acceder a Circuito (ponderaciones predeterminadas) y obtener el primer elemento
    # Acceder al formulario de ponderaciones y ponerlas todas a 1
    # Comprobar que cambia el primero por ejemplo

class TestSR(TestCase):

    print("Usando la base de datos:", settings.DATABASES['default']['NAME'])
    #Usaremos la base de datos normal, ya que no creamos ni eliminamos nada más allá del voto del usuario
     
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()
        cls.selenium = SeleniumWebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        cls.driver = webdriver.Chrome()
        super().tearDownClass()

    def setUp(self):
        self.driver.get("http://127.0.0.1:8000/logout/") #antes de cada prueba
        super().setUp()

    def tearDown(self):
        super().tearDown()


    #CERRAR SESIÓN/BORRAR VOTOS EN LA APP ANTES DE EJECUTAR

    # TEST: Redirige a login si no tienes votos del modelo.
    def test_noLogNoSR(self):
        self.driver.get("http://127.0.0.1:8000/")
        self.driver.set_window_size(1382, 754)
        self.driver.get("http://127.0.0.1:8000/logout/")

        self.driver.get("http://127.0.0.1:8000/recomendacionCircuitos")
        titulo_login = self.driver.find_element(By.XPATH, "/html/body/div/form/h1")
        self.assertEqual(titulo_login.text, "Inicio de sesión")

        self.driver.get("http://127.0.0.1:8000/recomendacionPilotos")
        titulo_login2 = self.driver.find_element(By.XPATH, "/html/body/div/form/h1")
        self.assertEqual(titulo_login2.text, "Inicio de sesión")

        self.driver.get("http://127.0.0.1:8000/recomendacionEquipos")
        titulo_login3 = self.driver.find_element(By.XPATH, "/html/body/div/form/h1")
        self.assertEqual(titulo_login3.text, "Inicio de sesión")


    #TEST: Loguearse y, sin haber votado nada, comprobar que sale el mensaje de info    
    def test_sinVotosMensajeInfo(self):
        self.driver.get("http://127.0.0.1:8000/")
        self.driver.set_window_size(1382, 754)
        self.driver.get("http://127.0.0.1:8000/logout/")

        self.driver.get("http://127.0.0.1:8000/login/")
        self.driver.find_element(By.ID, "username_or_email").click()
        self.driver.find_element(By.ID, "username_or_email").send_keys("testvoto")
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("estoesunacontrasena")
        self.driver.find_element(By.ID, "password").send_keys(Keys.ENTER)

        #Comprobación no votos
        self.driver.get("http://127.0.0.1:8000/circuito/62")
        #Comprobamos que no haya voto, en caso contrario, lo quitamos.
        if self.driver.find_element(By.CLASS_NAME ,"boton-votar").get_attribute("value") == "vota_no":
            self.driver.find_element(By.CSS_SELECTOR, ".bi").click() # QUITAR VOTO
        

        #Sin votar, buscamos recomendaciones
        self.driver.get("http://127.0.0.1:8000/recomendacionCircuitos")
        mensajeCircuitos = self.driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/div/h3")
        self.assertEqual(mensajeCircuitos.text, "No has votado ningún circuito, ¡no podemos recomendarte nada aún!")

        #Sin votar, buscamos recomendaciones
        self.driver.get("http://127.0.0.1:8000/recomendacionEquipos")
        mensajeEquipos = self.driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/div/h3")
        self.assertEqual(mensajeEquipos.text, "No has votado ningún equipo, ¡no podemos recomendarte nada aún!")

        #Sin votar, buscamos recomendaciones
        self.driver.get("http://127.0.0.1:8000/recomendacionPilotos")
        mensajePilotos = self.driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/div/h3")
        self.assertEqual(mensajePilotos.text, "No has votado ningún piloto, ¡no podemos recomendarte nada aún!")

        self.driver.get("http://127.0.0.1:8000/logout/")


    #TEST: Loguearse votar, acceder a SR, comprobar que se ve.
    # Además -> Cambiar ponderaciones y comprobar que cambia el primero (caso voto Red Bull Ring)    
    def test_accesoSRFuncional(self):
        self.driver.get("http://127.0.0.1:8000/")
        self.driver.set_window_size(1382, 754)
        self.driver.get("http://127.0.0.1:8000/logout/")

        self.driver.get("http://127.0.0.1:8000/login/")
        self.driver.find_element(By.ID, "username_or_email").click()
        self.driver.find_element(By.ID, "username_or_email").send_keys("testvoto")
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("estoesunacontrasena")
        self.driver.find_element(By.ID, "password").send_keys(Keys.ENTER)

        #Si no está votado, votamos (comprobación)
        self.driver.get("http://127.0.0.1:8000/circuito/62") #Red Bull Ring
        if self.driver.find_element(By.CLASS_NAME ,"boton-votar").get_attribute("value") == "vota_si":
            self.driver.find_element(By.CSS_SELECTOR, ".bi").click() # Votamos en caso de que no exista el voto
        self.driver.get("http://127.0.0.1:8000/recomendacionCircuitos")

        #Comprobación -> El mensaje anterior ya no sale (si hay voto)
        try:
            mensajeCircuitos = self.driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/div/h3")
            self.assertIsNotNone(mensajeCircuitos.text, "El mensaje de aviso se ve")
        except NoSuchElementException: #No lo encuentra -> OK
            pass

        #SPRINT 4: Cambio de ponderaciones
        recomendacion_inicial = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/div/div/div[4]/a')
        href_antes = recomendacion_inicial.get_attribute("href")

        #Cambiamos ponderaciones y comprobamos que la recomendación cambia
        self.driver.find_element(By.ID, "botonFormulario").click()
        self.driver.find_element(By.ID, "id_ponderacion_tipo").clear()
        self.driver.find_element(By.ID, "id_ponderacion_tipo").send_keys("0")
        self.driver.find_element(By.ID, "id_ponderacion_longitud").clear()
        self.driver.find_element(By.ID, "id_ponderacion_longitud").send_keys("5")
        self.driver.find_element(By.ID, "id_ponderacion_ediciones").clear()
        self.driver.find_element(By.ID, "id_ponderacion_ediciones").send_keys("5")
        self.driver.find_element(By.ID, "id_ponderacion_ediciones").send_keys(Keys.ENTER)

        recomendacion_despues = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/div/div/div[4]/a')
        #Comprobamos que ambas son diferentes
        self.assertNotEqual(href_antes, recomendacion_despues.get_attribute("href"))

        #Revertimos el voto y cerramos sesión
        self.driver.get("http://127.0.0.1:8000/circuito/62") #Red Bull Ring
        self.driver.find_element(By.CSS_SELECTOR, ".bi").click() # ELIMINAMOS VOTO
        self.driver.get("http://127.0.0.1:8000/logout/")

