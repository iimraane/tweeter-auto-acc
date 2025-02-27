from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import string
import random
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# -------------------------------------------------------------------
# FONCTION pour recréer un driver, réinitialiser le wait et relancer le signup
# -------------------------------------------------------------------
def restart_driver_and_signup():
    global driver, wait
    print("Fermeture de l'ancienne fenêtre et création d'un nouveau driver...")
    driver.quit()  # Fermer l'ancienne instance de Chrome
    driver = webdriver.Chrome()  # Créer une nouvelle instance
    wait = WebDriverWait(driver, 20)
    gen_acc()  # Relancer la création de compte


# -------------------------------------------------------------------
# FONCTION qui crée un compte (gen_acc) avec un email GuerrillaMail
# -------------------------------------------------------------------
def gen_acc():
    import requests, time, random, re, traceback
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    # --- 1. Génération de l'email temporaire via GuerrillaMail ---
    try:
        session = requests.Session()
        gm_response = session.get("https://api.guerrillamail.com/ajax.php", params={'f': 'get_email_address'})
        if gm_response.ok:
            gm_data = gm_response.json()
            temp_email = gm_data.get("email_addr")
            sid_token = gm_data.get("sid_token")
            print(f"[EMAIL]: Email temporaire généré : {temp_email}")
        else:
            print("Erreur lors de la génération de l'email temporaire.")
            return
    except Exception as e:
        print("Erreur lors de la requête GuerrillaMail :", e)
        return

    # --- 2. Remplissage du formulaire d'inscription (login normal) ---
    try:
        driver.get("https://twitter.com/i/flow/signup")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Créer un compte')]"))).click()

        wait.until(EC.presence_of_element_located((By.NAME, "name"))).send_keys("Test Nom")
        wait.until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(temp_email)
        wait.until(EC.presence_of_element_located((By.ID, "SELECTOR_1"))).send_keys("Janvier")
        wait.until(EC.presence_of_element_located((By.ID, "SELECTOR_2"))).send_keys("1")
        wait.until(EC.presence_of_element_located((By.ID, "SELECTOR_3"))).send_keys("2000")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Suivant')]"))).click()
        time.sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Suivant')]"))).click()
        time.sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Suivant')]"))).click()
        print("[Inscription] : Etape du code")
    except Exception as e:
        print("Erreur lors du remplissage du formulaire :", e)
        traceback.print_exc()
        return

    # --- 3. Attente (60 secondes maximum) de l'email de vérification envoyé par info@x.com ---
    code = None
    max_wait_time = 60  # temps d'attente maximum (en secondes)
    interval = 5        # intervalle de vérification (en secondes)
    elapsed_time = 0

    print("Attente de l'email de vérification provenant de info@x.com...")
    while elapsed_time < max_wait_time and not code:
        try:
            list_params = {'f': 'get_email_list', 'offset': 0, 'sid_token': sid_token}
            list_response = session.get("https://api.guerrillamail.com/ajax.php", params=list_params)
            if list_response.ok:
                emails = list_response.json().get("list", [])
                for email in emails:
                    mail_id = email.get("mail_id")
                    read_params = {'f': 'fetch_email', 'sid_token': sid_token, 'email_id': mail_id}
                    mail_response = session.get("https://api.guerrillamail.com/ajax.php", params=read_params)
                    if mail_response.ok:
                        mail_data = mail_response.json()
                        # On vérifie que l'email provient de "info@x.com"
                        mail_from = mail_data.get("mail_from", "").lower()
                        if "info@x.com" in mail_from:
                            mail_body = mail_data.get("mail_body", "")
                            # Recherche d'un code à 6 chiffres grâce à une regex
                            m = re.search(r'\b(\d{6})\b', mail_body)
                            if m:
                                code = m.group(1)
                                print(f"[EMAIL]: Code de vérification récupéré : {code}")
                                break
            else:
                print("Erreur lors de la récupération de la liste des emails.")
        except Exception as e:
            print("Erreur lors de la vérification des emails :", e)
        time.sleep(interval)
        elapsed_time += interval

    if not code:
        print("Aucun email de vérification provenant de info@x.com n'a été trouvé après 60 secondes.")
        return

    # --- 4. Soumission du code sur la page ---
    try:
        # On tape le code dans l'élément actif (si c'est bien le champ)
        driver.switch_to.active_element.send_keys(code)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Suivant')]"))).click()
        print("Code soumis avec succès.")
    except Exception as e:
        print("Erreur lors de la soumission du code :", e)
        traceback.print_exc()
        return
    
    # --- 5. Saisir le mot de passe ---
    try:
        password_field = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
        )
        mot_de_passe = ''.join(str(random.randint(0, 9)) for _ in range(12))
        password_field.send_keys(mot_de_passe)
        time.sleep(1)
        driver.switch_to.active_element.send_keys(Keys.ENTER)

        # Enchaînement de clics (Passer / Ignorer / etc.)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Passer pour le moment')]"))).click()
        time.sleep(0.5)

        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Ignorer pour le moment')]"))).click()
        time.sleep(0.5)

        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Passer pour le moment')]"))).click()
        time.sleep(0.5)

        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Suivant')]"))).click()
        time.sleep(0.5)

        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Musique')]"))).click()
        time.sleep(0.5)

        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Sport')]"))).click()
        time.sleep(0.5)

        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Gaming')]"))).click()
        time.sleep(0.5)

        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Suivant')]"))).click()
        time.sleep(0.5)

        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Suivant')]"))).click()
        time.sleep(0.5)

        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Suivre')]"))).click()
        time.sleep(0.5)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Suivant')]"))).click()

    except Exception as e:
        print("Erreur lors de la saisie du mot de passe ou des clics finaux :", e)
        traceback.print_exc()
        return


# -------------------------------------------------------------------
# FONCTION pour vérifier les pop-ups
# -------------------------------------------------------------------
def click_if_popup_exists(driver, timeout=3):
    try:
        # 1) Popup "Got it"
        popup_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Got it')]"))
        )
        popup_button.click()
        print("Pop-up 'Got it' détectée et fermée.")
    except TimeoutException:
        pass

    try:
        # 2) Popup "This request looks like it might be automated"
        error_element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(
                (By.XPATH,"//*[contains(text(), 'This request looks like it might be automated')]")
            )
        )
        if error_element:
            print("Détection du message 'might be automated' – on relance le signup avec un nouveau driver.")
            restart_driver_and_signup()
    except TimeoutException:
        pass


# -------------------------------------------------------------------
# INITIALISATION DU DRIVER PRINCIPAL
# -------------------------------------------------------------------
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)

# Quelques variables globales
characters = string.ascii_letters + string.digits
post = 1

# Créer un premier compte
gen_acc()

# -------------------------------------------------------------------
# BOUCLE PRINCIPALE
# -------------------------------------------------------------------
while True:
    # Attendre que la zone de texte soit présente (pour poster un tweet)
    textarea = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweetTextarea_0"]'))
    )

    random_string = ''.join(random.choices(characters, k=50))
    message = (
        f"Repost numéro {post}, créé par @El_Titano_, "
        f"voici une suite de caractères hasardeuse pour l'anti bot : {random_string}. \n"
        "https://x.com/NetflixFR/status/1892874964782526917"
    )

    # Cliquer sur la zone de texte et écrire le message
    textarea.click()
    textarea.send_keys(message)

    # Simuler Ctrl + Entrée pour publier le tweet
    textarea.send_keys(Keys.CONTROL, Keys.RETURN)
    time.sleep(random.uniform(1.5, 4.5))

    # Vérifier si une pop-up apparaît
    click_if_popup_exists(driver, 0.5)

    post += 1

    # Tous les 150 posts, on crée un nouveau compte
    if post % 150 == 0:
        print(f"Atteint {post} posts. Création d'un nouveau compte...")
        restart_driver_and_signup()
