# Imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
import requests
import io
from PIL import Image
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
from rich.console import Console

console = Console()

# Constants
MAX_WAIT =  600
SCRIPTS_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
PARENT_DIRECTORY = os.path.abspath(os.path.join(SCRIPTS_DIRECTORY, os.pardir))
ASSETS_DIRECTORY = os.path.join(PARENT_DIRECTORY, 'assets/')
MAIN_HAND_TARGETS = [
  'https://bdocodex.com/us/weapon/longsword/',
  'https://bdocodex.com/us/weapon/longbow/',
  'https://bdocodex.com/us/weapon/amulet/',
  'https://bdocodex.com/us/weapon/axe/',
  'https://bdocodex.com/us/weapon/blade/',
  'https://bdocodex.com/us/weapon/shortsword/',
  'https://bdocodex.com/us/weapon/staff/',
  'https://bdocodex.com/us/weapon/krieg/',
  'https://bdocodex.com/us/weapon/gauntlet/',
  'https://bdocodex.com/us/weapon/pendulum/',
  'https://bdocodex.com/us/weapon/crossbow/',
  'https://bdocodex.com/us/weapon/florang/',
  'https://bdocodex.com/us/weapon/battleaxe/',
  'https://bdocodex.com/us/weapon/shamshir/',
  'https://bdocodex.com/us/weapon/morgenshtern/',
  'https://bdocodex.com/us/weapon/kyve/',
  'https://bdocodex.com/us/weapon/serenaca/',
  'https://bdocodex.com/us/weapon/slayer/'
]
SUB_HAND_TARGETS = [
  'https://bdocodex.com/us/subweapon/shield/',
  'https://bdocodex.com/us/subweapon/dagger/',
  'https://bdocodex.com/us/subweapon/talisman/',
  'https://bdocodex.com/us/subweapon/knot/',
  'https://bdocodex.com/us/subweapon/trinket/',
  'https://bdocodex.com/us/subweapon/shortbow/',
  'https://bdocodex.com/us/subweapon/kunai/',
  'https://bdocodex.com/us/subweapon/star/',
  'https://bdocodex.com/us/subweapon/vambrace/',
  'https://bdocodex.com/us/subweapon/noblesword/',
  'https://bdocodex.com/us/subweapon/harpoon/',
  'https://bdocodex.com/us/subweapon/vitclari/',
  'https://bdocodex.com/us/subweapon/haladie/',
  'https://bdocodex.com/us/subweapon/kratum/',
  'https://bdocodex.com/us/subweapon/mareca/',
  'https://bdocodex.com/us/subweapon/shard/'
]
AWAKENING_TARGETS = [
  'https://bdocodex.com/us/awakening/2hsword/',
  'https://bdocodex.com/us/awakening/scythe/',
  'https://bdocodex.com/us/awakening/handgun/',
  'https://bdocodex.com/us/awakening/elementblade/',
  'https://bdocodex.com/us/awakening/chanbon/',
  'https://bdocodex.com/us/awakening/spear/',
  'https://bdocodex.com/us/awakening/glaive/',
  'https://bdocodex.com/us/awakening/snakespear/',
  'https://bdocodex.com/us/awakening/asurablade/',
  'https://bdocodex.com/us/awakening/chakram/',
  'https://bdocodex.com/us/awakening/naturesphere/',
  'https://bdocodex.com/us/awakening/elementsphere/',
  'https://bdocodex.com/us/awakening/vediant/',
  'https://bdocodex.com/us/awakening/bracers/',
  'https://bdocodex.com/us/awakening/cestus/',
  'https://bdocodex.com/us/awakening/glaives/',
  'https://bdocodex.com/us/awakening/bow/',
  'https://bdocodex.com/us/awakening/jordun/',
  'https://bdocodex.com/us/awakening/dualglaives/',
  'https://bdocodex.com/us/awakening/sting/',
  'https://bdocodex.com/us/awakening/kibelius/',
  'https://bdocodex.com/us/awakening/patraca/'
]
ARMOR_TARGETS = [
  'https://bdocodex.com/us/armor/head/',
  'https://bdocodex.com/us/armor/body/',
  'https://bdocodex.com/us/armor/hand/',
  'https://bdocodex.com/us/armor/foot/'
]
ACCESSORY_TARGETS = [
  'https://bdocodex.com/us/accessory/ring/',
  'https://bdocodex.com/us/accessory/necklace/',
  'https://bdocodex.com/us/accessory/earring/',
  'https://bdocodex.com/us/accessory/belt/'
]
LIGHTSTONE_TARGETS = [
  'https://bdocodex.com/us/items/lightstones/fire/',
  'https://bdocodex.com/us/items/lightstones/earth/',
  'https://bdocodex.com/us/items/lightstones/wind/',
  'https://bdocodex.com/us/items/lightstones/flora/',
  'https://bdocodex.com/us/items/lightstones/special/'
]
MATERIALS_TARGETS = [
  'https://bdocodex.com/us/items/materials/ore/',
  'https://bdocodex.com/us/items/materials/plant/',
  'https://bdocodex.com/us/items/materials/seed/',
  'https://bdocodex.com/us/items/materials/skin/',
  'https://bdocodex.com/us/items/materials/blood/',
  'https://bdocodex.com/us/items/materials/meat/',
  'https://bdocodex.com/us/items/materials/seafood/',
  'https://bdocodex.com/us/items/materials/other/'
]
ENHANCEMENT_TARGETS = [
  'https://bdocodex.com/us/items/powerup/stone/',
  'https://bdocodex.com/us/items/powerup/seal/'
]
CONSUMABLE_TARGETS = [
  'https://bdocodex.com/us/items/consumables/attackpotion/',
  'https://bdocodex.com/us/items/consumables/defensepotion/',
  'https://bdocodex.com/us/items/consumables/otherpotion/',
  'https://bdocodex.com/us/items/consumables/culinary/',
  'https://bdocodex.com/us/items/consumables/hpmppotion/',
  'https://bdocodex.com/us/items/consumables/siege/',
  'https://bdocodex.com/us/items/consumables/complex/',
  'https://bdocodex.com/us/items/consumables/other/',
]
LIFE_TOOL_TARGETS = [
  'https://bdocodex.com/us/items/tools/axe/',
  'https://bdocodex.com/us/items/tools/syringe/',
  'https://bdocodex.com/us/items/tools/cleaver/',
  'https://bdocodex.com/us/items/tools/pick/',
  'https://bdocodex.com/us/items/tools/sickle/',
  'https://bdocodex.com/us/items/tools/knife/',
  'https://bdocodex.com/us/items/tools/rod/',
  'https://bdocodex.com/us/items/tools/gun/',
  'https://bdocodex.com/us/items/tools/table/',
  'https://bdocodex.com/us/items/tools/other/'
]
ALCHEMY_STONE_TARGETS = [
  'https://bdocodex.com/us/items/stones/attack/',
  'https://bdocodex.com/us/items/stones/defense/',
  'https://bdocodex.com/us/items/stones/hp/',
  'https://bdocodex.com/us/items/stones/simple/'
]
TRANSFUSION_TARGETS = [
  'https://bdocodex.com/us/items/gems/weapon/',
  'https://bdocodex.com/us/items/gems/subweapon/',
  'https://bdocodex.com/us/items/gems/awakening/',
  'https://bdocodex.com/us/items/gems/helmet/',
  'https://bdocodex.com/us/items/gems/armor/',
  'https://bdocodex.com/us/items/gems/gloves/',
  'https://bdocodex.com/us/items/gems/boots/',
  'https://bdocodex.com/us/items/gems/other/'
]
MOUNT_TARGETS = [
  'https://bdocodex.com/us/items/mounts/certificate/',
  'https://bdocodex.com/us/items/mounts/food/',
  'https://bdocodex.com/us/items/mounts/helm/',
  'https://bdocodex.com/us/items/mounts/armor/',
  'https://bdocodex.com/us/items/mounts/saddle/',
  'https://bdocodex.com/us/items/mounts/stirrup/',
  'https://bdocodex.com/us/items/mounts/horseshoe/',
  'https://bdocodex.com/us/items/mounts/elephantstirrup/',
  'https://bdocodex.com/us/items/mounts/elephantplatform/',
  'https://bdocodex.com/us/items/mounts/elephanthelm/',
  'https://bdocodex.com/us/items/mounts/elephantsaddle/',
  'https://bdocodex.com/us/items/mounts/training/'
]
SHIP_TARGETS = [
  'https://bdocodex.com/us/items/boat/certificate/',
  'https://bdocodex.com/us/items/boat/hold/',
  'https://bdocodex.com/us/items/boat/nose/',
  'https://bdocodex.com/us/items/boat/decor/',
  'https://bdocodex.com/us/items/boat/totem/',
  'https://bdocodex.com/us/items/boat/brigdecor/',
  'https://bdocodex.com/us/items/boat/hull/',
  'https://bdocodex.com/us/items/boat/cannon/',
  'https://bdocodex.com/us/items/boat/sail/'
]
WAGON_TARGETS = [
  'https://bdocodex.com/us/items/carriage/certificate/',
  'https://bdocodex.com/us/items/carriage/wheels/',
  'https://bdocodex.com/us/items/carriage/roof/',
  'https://bdocodex.com/us/items/carriage/flag/',
  'https://bdocodex.com/us/items/carriage/sign/',
  'https://bdocodex.com/us/items/carriage/lantern/'
]
FURNITURE_TARGETS = [
  'https://bdocodex.com/us/items/furniture/bed/',
  'https://bdocodex.com/us/items/furniture/table/',
  'https://bdocodex.com/us/items/furniture/cupboard/',
  'https://bdocodex.com/us/items/furniture/chair/',
  'https://bdocodex.com/us/items/furniture/chandelier/',
  'https://bdocodex.com/us/items/furniture/carpet/',
  'https://bdocodex.com/us/items/furniture/walls/',
  'https://bdocodex.com/us/items/furniture/decor/',
  'https://bdocodex.com/us/items/furniture/other/'
]

def initializeDriver():
  # Set Chrome webdriver options
  options = webdriver.ChromeOptions()
  options.add_argument('--ignore-certificate-errors')
  # options.add_argument('--headless')
  options.add_argument('--no-sandbox')
  options.add_argument('--disable-extensions')
  options.add_argument('--kiosk-printing')
  options.add_argument('--test-type')
  options.add_argument('--disable-gpu')
  options.add_experimental_option('excludeSwitches', ['enable-logging'])
  
  # Define webdriver
  driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
  driver.set_page_load_timeout(MAX_WAIT)
  driver.set_script_timeout(MAX_WAIT)

  return driver

def imageScraper():
  def downloadImage(download_path, url, file_name, category_list):
    try:
      image_content = requests.get(url).content
      image_file = io.BytesIO(image_content)
      image = Image.open(image_file)
      names = file_name.split('/')
      categories = category_list.split('/')
      folder_path = download_path

      # Main folders
      for category in categories[:-1]:
        folder_path = folder_path + category + '/'

        if not os.path.exists(folder_path):
          os.makedirs(folder_path)

      file_path = folder_path + names[-1]

      with open(file_path, 'wb') as img:
        image.save(img, 'WebP')
      # console.print(f'Downloaded {file_name} successfully.', style='green')
    except Exception as e:
      console.print(f'Failed to download {file_name}. Error - {e}', style='red bold')

  def getImageUrls(driver, url, delay):
    try:
      imageUrls = []
      driver.get(url)
      time.sleep(delay)

      """
      pagination = driver.find_element(By.CLASS_NAME, 'pagination')
      pages = pagination.find_elements(By.TAG_NAME, 'li')
      last_page = int(pages[-2].text)
      current_page = 1

      while current_page <= last_page:
        time.sleep(delay+2)

        thumbnails = driver.find_elements(By.CLASS_NAME, 'icon_wrapper')
        for img in thumbnails:
          image = img.find_element(By.TAG_NAME, 'img')
          if image.get_attribute('src') and 'http' in image.get_attribute('src'):
            imageUrls.append(image.get_attribute('src'))

        current_page += 1
        try:
          driver.find_element(By.ID, 'WeaponTable_next').click()
        except:
          pass
      """

      # Set page length to 200 items
      # select = Select(driver.find_element(By.NAME, 'WeaponTable_length'))
      # select = Select(driver.find_element(By.NAME, 'EquipmentTable_length'))
      # select = Select(driver.find_element(By.NAME, 'MainItemTable_length'))
      # select = Select(driver.find_element(By.NAME, 'ConsumablesTable_length'))
      # select = Select(driver.find_element(By.NAME, 'GemsTable_length'))
      select = Select(driver.find_element(By.NAME, 'FurnitureTable_length'))
      select.select_by_value('200')
      time.sleep(delay)

      # Grab image urls and add them to set
      thumbnails = driver.find_elements(By.CLASS_NAME, 'icon_wrapper')
      for img in thumbnails:
        image = img.find_element(By.TAG_NAME, 'img')
        if image.get_attribute('src') and 'http' in image.get_attribute('src'):
          imageUrls.append(image.get_attribute('src'))

      return [*set(imageUrls)]
    except Exception as e:
      console.print(f'Failed to get image urls. Error - {e}', style='red bold')

  for targets in FURNITURE_TARGETS:
    with console.status('Creating driver...', spinner='dots2'):
      driver = initializeDriver()

    with console.status("Fetching assets...", spinner='dots2'):
      urls = getImageUrls(driver, targets, 5)
      driver.quit()
    
    with console.status("Downloading assets...", spinner='dots2'):
      names = [x.replace('https://bdocodex.com/items/new_icon/', '') for x in urls]
      category = targets.replace('https://bdocodex.com/us/','')
      for x in range(0, len(urls)):
        downloadImage(ASSETS_DIRECTORY, urls[x], names[x], category)
      console.print(f'Finished downloading {len(urls)} assets.')
      
imageScraper()