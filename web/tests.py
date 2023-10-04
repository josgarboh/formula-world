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

# TEST PUNTUACIONES
    # No aparece votar si no login
    # NO PODER votar si no login
    # Aparece para votar si login
    # Votar OK
    # Desvotar

class TestPuntuacion(TestCase):

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
        super().setUp()

    def tearDown(self):
        super().tearDown()


    #CERRAR SESIÓN EN LA APP ANTES DE EJECUTAR

    # TEST: Botón oculto para usuario no logueado.
    # No permite votar.
    def test_noVotaNoLogueado(self):
        self.driver.get("http://127.0.0.1:8000/")
        self.driver.set_window_size(1382, 754)
        self.driver.get("http://127.0.0.1:8000/logout/")
        self.driver.get("http://127.0.0.1:8000/circuito/62") #Red Bull Ring

        try:
            # Intenta encontrar el botón (no lo hará)
            boton_votar = self.driver.find_element(By.CLASS_NAME, "boton-votar")
        
            # Verifica si el botón está visible (esto fallará si está presente)
            self.assertFalse(boton_votar.is_displayed(), "El botón está visible")
        except NoSuchElementException:
            # El botón no se encontró, lo que es lo esperado
            pass

        #Comprobamos además que no puede votar (redirige a login)
        self.driver.get("http://127.0.0.1:8000/votar/circuito/62/")
        self.assertEqual(self.driver.current_url, "http://127.0.0.1:8000/login/?next=/votar/circuito/62/")
        # Ha redirigido a login desde dicho circuito


    #TEST: Aparece botón si está logueado, comprobamos voto y quitar voto
    def test_votarok(self):
        self.driver.get("http://127.0.0.1:8000/")
        self.driver.set_window_size(1382, 754)
        self.driver.get("http://127.0.0.1:8000/logout/")

        self.driver.get("http://127.0.0.1:8000/login/")
        self.driver.find_element(By.ID, "username_or_email").click()
        self.driver.find_element(By.ID, "username_or_email").send_keys("testvoto")
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("estoesunacontrasena")
        self.driver.find_element(By.ID, "password").send_keys(Keys.ENTER)
        self.driver.get("http://127.0.0.1:8000/circuito/62")
        #Checkeamos previamente que no haya votos:
        if self.driver.find_element(By.CLASS_NAME ,"boton-votar").get_attribute("value") == "vota_no":
            self.driver.find_element(By.CSS_SELECTOR, ".bi").click() # QUITAR VOTO

        #Comprobamos que no ha votado aun (es un usuario de prueba)
        boton = self.driver.find_element(By.CLASS_NAME ,"boton-votar")
        self.assertEqual(boton.get_attribute("value"), "vota_si") #Aparece el voton de votar_si -> no ha votado


        self.driver.find_element(By.CSS_SELECTOR, ".bi").click() # VOTO POSITIVO

        #Comprobamos que se ha votado (el botón ha cambiado a vota_no)
        boton = self.driver.find_element(By.CLASS_NAME ,"boton-votar")
        self.assertEqual(boton.get_attribute("value"), "vota_no")

        self.driver.find_element(By.CSS_SELECTOR, ".bi").click() # QUITAR VOTO

        #Volvemos a quitar el voto
        boton = self.driver.find_element(By.CLASS_NAME ,"boton-votar")
        self.assertEqual(boton.get_attribute("value"), "vota_si")

        self.driver.get("http://127.0.0.1:8000/logout/")
        self.driver.quit()