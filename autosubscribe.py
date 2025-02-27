from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import requests, time, random, re, traceback, os
import openai
from openai import OpenAI
from faker import Faker
fake = Faker('fr_FR')
client = OpenAI()

def save_account_info(email, password, username, filename="accounts.txt"):
    """
    Sauvegarde l'email, le mot de passe et le nom d'utilisateur dans un fichier texte.
    """
    with open(filename, "a") as file:
        file.write(f"{email}:{password}:{username}\n")
    print(f"[SAUVEGARDE] {email}:{password}:{username} enregistré dans {filename}")



def restart_driver_and_signup():
    global driver, wait
    print("Fermeture de l'ancienne fenêtre et création d'un nouveau driver...")
    driver.quit()  # Fermer l'ancienne instance de Chrome
    driver = webdriver.Chrome()  # Créer une nouvelle instance
    wait = WebDriverWait(driver, 20)
    gen_acc()  # Relancer la création de compte

def gen_acc():
    global mot_de_passe
    global temp_email

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

        prenom = fake.first_name()
        nom = fake.last_name()
        wait.until(EC.presence_of_element_located((By.NAME, "name"))).send_keys(f"{prenom}{nom}")
        # Générer un prénom et un nom aléatoires

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
        # Localiser l'élément (ici par exemple avec un XPath personnalisé)
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
       
        # Listes étendues
        lieu = ["Plage au coucher de soleil", "Forêt enneigée", "Rue animée d'une grande ville", "Bord de lac tranquille",
                "Jardin fleuri", "Sommet de montagne", "Café en terrasse", "Parc urbain moderne", "Bibliothèque ancienne",
                "Toit d’un gratte-ciel", "Ruelle pavée d’un vieux quartier", "Plage tropicale avec palmiers",
                "Pont en bois au-dessus d’une rivière", "Champ de tournesols", "Désert avec dunes dorées",
                "Cascade en pleine jungle", "Studio artistique", "Salle de concert vide", "Cabane en bois au bord d’un lac",
                "Port de pêche pittoresque"]

        visage = ["Visage souriant", "Visage sérieux", "Visage de profil", "Visage légèrement penché",
                "Visage masqué partiellement par des lunettes de soleil", "Visage avec barbe légère",
                "Visage avec taches de rousseur", "Visage maquillé avec un look naturel", "Visage expressif et énergique",
                "Visage doux avec un regard rêveur", "Visage rasé de près", "Visage encadré par des cheveux longs",
                "Visage caché par un chapeau", "Visage tourné vers la lumière", "Visage avec piercing discret",
                "Visage avec des mèches colorées", "Visage avec une expression curieuse",
                "Visage marqué par un large sourire", "Visage au regard intense", "Visage avec une expression pensive"]

        atmosphere = ["Mystérieuse et captivante", "Détendue et paisible", "Dynamique et vibrante",
                    "Rêveuse et romantique", "Moderne et minimaliste", "Sauvage et libre", "Énergique et inspirante",
                    "Vintage et nostalgique", "Luxueuse et sophistiquée", "Urbaine et branchée", "Bohème et artistique",
                    "Futuriste et high-tech", "Naturelle et organique", "Sombre et dramatique", "Éthérée et légère",
                    "Rustique et chaleureuse", "Festive et lumineuse", "Discrète et intime", "Sportive et active",
                    "Créative et audacieuse"]

        meteo = ["Journée ensoleillée", "Légère brume matinale", "Pluie fine", "Temps orageux avec ciel sombre",
                "Ciel clair avec quelques nuages", "Neige légère tombant doucement", "Soleil voilé par des nuages",
                "Aurore rose et violette", "Brise marine rafraîchissante", "Vent fort soulevant les cheveux",
                "Brouillard épais et mystérieux", "Arc-en-ciel dans le ciel lointain", "Soirée étoilée", "Crépuscule doré",
                "Tempête imminente", "Ciel bleu profond sans nuages", "Gouttes de pluie sur la fenêtre",
                "Orage en arrière-plan", "Flocons de neige fondants", "Coucher de soleil rougeoyant"]

        pose = ["Bras croisés regardant l’objectif", "Mains dans les poches en regardant au loin",
                "Assis sur un muret, regard pensif", "En train de marcher avec un léger sourire",
                "Debout avec une main dans les cheveux", "Penché vers l’avant, regard intense",
                "Assis en tailleur sur le sol", "Dos tourné, regard par-dessus l’épaule", "Sautant en l’air avec enthousiasme",
                "Accoudé à une rambarde, vue plongeante", "Allongé dans l’herbe, regard vers le ciel",
                "Assis sur une chaise renversée", "Bras écartés face au vent", "Main tendue vers l’objectif",
                "Courir sur une plage déserte", "Appuyé contre un mur avec désinvolture", "Sautillant sur un trottoir mouillé",
                "Étendu sur un canapé vintage", "Appuyé sur une barrière en bois", "Jouant avec ses cheveux en riant"]

        expression = ["Sourire éclatant", "Regard mystérieux", "Expression concentrée", "Légère moue malicieuse",
                    "Rire spontané", "Regard doux et accueillant", "Clin d’œil complice", "Regard intense et sérieux",
                    "Sourire timide", "Expression rêveuse", "Regard ébloui par la lumière",
                    "Froncement de sourcils intrigant", "Air surpris et amusé", "Lèvres entrouvertes dans la réflexion",
                    "Air moqueur et charmeur", "Regard lointain et inspiré", "Air détendu avec un léger sourire",
                    "Regard pénétrant plein de confiance", "Yeux plissés par un grand sourire", "Expression calme et sereine"]

        # 🎲 Génération aléatoire
        description = (
            f"Photo prise dans {random.choice(lieu)}, avec un {random.choice(visage)}. "
            f"L'atmosphère est {random.choice(atmosphere)}, sous une {random.choice(meteo)}. "
            f"La personne adopte une pose {random.choice(pose)} avec une expression {random.choice(expression)}."
        )
        print(description)
        
        response = client.images.generate(
            model="dall-e-3",
            prompt=f"{description}",
            size="1024x1024",
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url

        # 💾 3. **Téléchargement de l'image générée**
        image_path = "profile_picture.png"
        img_data = requests.get(image_url).content
        with open(image_path, 'wb') as handler:
            handler.write(img_data)

        print(f"[INFO] Image téléchargée avec succès dans : {image_path}")

       # 1) Localiser l'élément input[type='file']
        upload_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
        )

        # 2) Envoyer le chemin du fichier à l'input
        image_path = os.path.abspath("profile_picture.png")
        upload_input.send_keys(image_path)
        print(f"[INFO] ✅ Image '{image_path}' ajoutée avec succès.")

        # 🏃 3. **Attendre que l'image se charge** puis cliquer sur "Suivant"
        time.sleep(3)  # Laisser le temps à l'image de se charger
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Appliquer')]"))
        ).click()

        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Suivant')]"))).click()
        

        # Localiser le champ "Nom d'utilisateur"
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='username']"))
        )
        # Récupérer la valeur du champ
        username_value = username_input.get_attribute("value")
        print("[INFO] Nom d'utilisateur détecté :", username_value)

        save_account_info(temp_email, mot_de_passe, username_value)
        time.sleep(1)

    except Exception as e:
        print("Erreur lors de la saisie du mot de passe ou des clics finaux :", e)
        traceback.print_exc()
        return
    
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)

while True:

    restart_driver_and_signup()



    driver.get("https://x.com/WhisperEcho_")

    time.sleep(0.5)

    # 1) Localiser le champ "Phone, email, or username"
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='text']"))
    )
    email_input.send_keys(temp_email, Keys.ENTER)

    time.sleep(0.5)

    # 3) Localiser le champ "Password"
    password_input = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )
    password_input.send_keys(mot_de_passe, Keys.ENTER)

    
    # Attendre que l'élément devienne cliquable
    follow_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Follow')]"))
    )

    # Cliquer sur l'élément
    follow_button.click()
    following_xpath = (By.XPATH, "//span[contains(text(), 'Following')]")


    if following_xpath:
        continue

    time.sleep(5)











