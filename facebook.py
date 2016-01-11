#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Anthony Lazzaro, and Stefan Safranek"
__copyright__ = "Copyright 2015, Anti-Search Project"
__credits__ = ["Anthony Lazzaro", "Stefan Safranek"]

__license__ = "The MIT License (MIT)"
__version__ = "0.0.5"
__maintainer__ = "Stefan Safranek"
__email__ = "sjsafranek@gmail.com"
__status__ = "Development"

import time
import os
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException


class FacebookClient(object):
    """ Facebook Selenium Interface """
    def __init__(self, username, password):
        self.browser = webdriver.Firefox()
        self.url = "https://www.facebook.com/"
        self.username = username
        self.password = password
        self.browser.implicitly_wait(5)
        self.browser.maximize_window()
        self.login()

    def login(self):
        """ Uses username and password to log into Facebook """
        self.browser.get(self.url)
        username = self.browser.find_element(By.ID,"email")
        username.send_keys(self.username)
        password = self.browser.find_element(By.ID,"pass")
        password.send_keys(self.password)
        login = self.browser.find_element(By.ID,"loginbutton")
        login = login.find_element(By.TAG_NAME,"input")
        login.click()

    def screenshot(self, filename=None):
        """ Saves a screenshot png """
        if not filename:
            filename = str(time.time())
        if '.png' not in filename:
            filename += '.png'
        savefile = os.path.join('screenshots',filename)
        self.browser.save_screenshot(savefile)

    def _slow_type(self,word,elem):
        """ Mimics a human user typing """
        typing_speed = 42 #50 #wpm
        for letter in word:
            elem.send_keys(letter)
            time.sleep(random.random()*10.0/typing_speed)
        elem.send_keys(Keys.ENTER)

    def post(self,text):
        """ Makes a facebook post """
        self.browser.get("https://www.facebook.com/?ref=tn_tnmn")
        pagelet_composer = self.browser.find_element(By.ID,"pagelet_composer")
        forms = pagelet_composer.find_elements(By.TAG_NAME,"form")
        form = forms[1]
        wrap = form.find_element(By.CSS_SELECTOR,"div.wrap")
        innerWrap = wrap.find_element(By.CSS_SELECTOR,"div.innerWrap")
        textarea = innerWrap.find_element(By.CSS_SELECTOR,"textarea")
        self._slow_type(text,textarea)
        buttons = self.browser.find_elements(By.CSS_SELECTOR,"button")
        for button in buttons:
            if "Post" in button.text:
                button.click()
                break

    def set_status(self):
        """ sets a facebook status """
        self.browser.get("https://www.facebook.com/?ref=tn_tnmn")
        pagelet_composer = self.browser.find_element(By.ID,"pagelet_composer")
        forms = pagelet_composer.find_elements(By.TAG_NAME,"form")
        form = forms[1]
        wrap = form.find_element(By.CSS_SELECTOR,"div.wrap")
        innerWrap = wrap.find_element(By.CSS_SELECTOR,"div.innerWrap")
        textarea = innerWrap.find_element(By.CSS_SELECTOR,"textarea")
        options = [
            "Good times","Having fun",
            "Oy vey","Awesome",
            "Totally Tubular","Bitchen",
            "Radical","Groovy",
            "Having a good day",
            "Rock n Roll!" 
        ]
        text = options[random.randint(0,len(options)-1)]
        self._slow_type(text,textarea)
        # LOCATION
        self.browser.find_element(By.ID,"composerCityTagger").click()
        textinputs = self.browser.find_elements(By.CSS_SELECTOR,"input.inputtext.textInput")
        for textinput in textinputs:
            if textinput.get_attribute("aria-label") == "Where are you?":
                textinput.send_keys("Eugene Oregon")
                break
        time.sleep(2)
        places = self.browser.find_element(By.CSS_SELECTOR,"div.PlacesTypeaheadViewList")
        places = places.find_elements(By.CSS_SELECTOR,"li")
        n = random.randint(0,len(places)-1)
        places[n].click()
        # ACTIONS
        time.sleep(2)
        self.browser.find_element(By.ID,"composerActionTagger").click()
        actions = self.browser.find_elements(By.CSS_SELECTOR,"li.action_type")
        n = random.randint(0,len(actions)-1)
        action = actions[n]
        action.click()
        try:
            pages = self.browser.find_elements(By.CSS_SELECTOR,"li.page")
            n = random.randint(0,len(pages)-1)
            page = pages[n]
            page.click()
        except:
            pass
        buttons = self.browser.find_elements(By.CSS_SELECTOR,"button")
        for button in buttons:
            if "Post" in button.text:
                button.click()
                break

    def like_all(self):
        likes = self.browser.find_elements(By.CSS_SELECTOR,"a.UFILikeLink")
        for like in likes:
            if like.text == "Like":
                like.click()

    def close_ads(self):
        section = self.browser.find_element(By.CSS_SELECTOR,"div.ego_unit_container")
        start = time.time()
        while time.time() - start > 60:
            try:
                elements = section.find_elements(By.CSS_SELECTOR, 'a.ego_x.uiCloseButton.uiCloseButtonSmall')
                if len(elements) != 0:
                    section.find_elements(By.CSS_SELECTOR, 'a.ego_x.uiCloseButton.uiCloseButtonSmall')[0].click()
                else:
                    break
                time.sleep(0.75)
            except:
                pass

    def happy_birthdays(self):
        self.browser.get('https://www.facebook.com/events/birthdays')
        div = self.browser.find_element(By.ID,"events_birthday_view")
        text_areas = div.find_elements(By.CSS_SELECTOR,"textarea.enter_submit.uiTextareaNoResize.uiTextareaAutogrow.uiStreamInlineTextarea.inlineReplyTextArea.mentionsTextarea.textInput")
        for textarea in text_areas:
            textarea.send_keys("HAPPY BIRTHDAY!!" + Keys.RETURN)

    def logout(self):
        self.browser.get("https://www.facebook.com/?ref=tn_tnmn")
        self.browser.find_element(By.ID,"userNavigationLabel").click()
        for item in self.browser.find_elements(By.CSS_SELECTOR,"li.navSubmenu.__MenuItem"):
            if "Log Out" == item.text:
                item.click()
                break

    def destroy(self):
        try:
            self.logout()
        except:
            pass
        self.browser.quit()

    def __repr__(self):
        return "Facebook %s" % self.username


