import requests
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

sleepTimeDuration = 5
fileProfiles = "profile.txt"

username = 'nume'
password = 'parola'

def generateMessageableLinks():
    linksForProfiles = []

    for i in range(0, 5001, 50):
        link = "https://www.pbinfo.ro/solutii?start=" + str(i)
        linksForProfiles.append(link)
    return linksForProfiles

def readMessagedProfiles():
    messagedProfiles = []
    f = open(fileProfiles, 'r')
    while True:
        s = f.readline().strip()
        if not s:
            break
        messagedProfiles.append(s)
    f.close()
    return messagedProfiles

def findMessageableProfiles():
    linksForProfiles = generateMessageableLinks()
    messagedProfiles = readMessagedProfiles()
    unmessagedProfiles = []
    for link in linksForProfiles:
        page = requests.get(link)
        pageSource = page.text
        pageSource = pageSource.split('\n')
        print("URL:", link)
        print("******************\n")
        for line in pageSource:
            if line.find("<a href=\"/profil/") != -1:
                line = line[25:]
                line = line[:len(line) - 2]
                try:
                    messagedProfiles.index(line)
                except:
                    unmessagedProfiles.append(line)
                    messagedProfiles.append(line)

    print(unmessagedProfiles)
    print(len(unmessagedProfiles))
    return unmessagedProfiles

def sendMessage(driver):
    message = driver.find_element_by_xpath("//*[@id=\"mesaj\"]")
    message.send_keys("Salut! Te asteptam pe https://infonow.ro/ pentru *a invata programare*!")
    driver.find_element_by_xpath("//*[@id=\"zona-mijloc\"]/div[1]/div[4]/div[1]/form/div[2]/div[2]/input").click()

def writeProfileToFile(profile):
    f = open(fileProfiles, 'a')
    f.write(profile + '\n')
    f.close()

def logInUser(driver):
    usernameInput = driver.find_element_by_xpath("//*[@id=\"user\"]")
    passwordInput = driver.find_element_by_xpath("//*[@id=\"parola\"]")
    usernameInput.send_keys(username)
    passwordInput.send_keys(password)
    driver.find_element_by_xpath("//*[@id=\"form-login\"]/div/div[2]/div[4]/button").click()


def main():
    numberOfMessagedProfiles = 0
    profilesWithDeactivatedChat = 0

    while True:
	profilesToMessage = findMessageableProfiles()

        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get('https://www.pbinfo.ro')
        time.sleep(sleepTimeDuration)

        logInUser(driver)
        time.sleep(sleepTimeDuration)
        for profile in profilesToMessage:
            print(numberOfMessagedProfiles)
            if numberOfMessagedProfiles > 100:
                time.sleep(600)
                numberOfMessagedProfiles = 0
            chatLink = "https://www.pbinfo.ro/?pagina=conversatii&partener=" + profile
            driver.get(chatLink)
            time.sleep(sleepTimeDuration)
            try:
                sendMessage(driver)
                numberOfMessagedProfiles += 1
            except:
                profilesWithDeactivatedChat += 1
            writeProfileToFile(profile)
            time.sleep(sleepTimeDuration)

	driver.quit()


main()
