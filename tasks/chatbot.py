#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException

from facebook import *
import cleverbot3
import humanRandom

def main(username,password):
    """ Opens FacebookClient and chats with random person """
    # Setup
    fb = FacebookClient(username,password)
    chatbot = cleverbot3.Session()
    # choose random "friend" to chat with
    chat_list = fb.browser.find_element(By.CSS_SELECTOR,"ul.fbChatOrderedList.clearfix")
    items = chat_list.find_elements(By.TAG_NAME,"li")
    n = random.randint(0,len(items)-1)
    items[n].find_element(By.TAG_NAME,"a").click()
    # initiate coversation
    chat_tabs_pagelet = fb.browser.find_element(By.ID,"ChatTabsPagelet")
    textarea = chat_tabs_pagelet.find_element(By.TAG_NAME,"textarea")
    textarea.send_keys("Hi!")
    textarea.send_keys(Keys.RETURN)
    # track conversation for 5 minutes
    conversation_div = fb.browser.find_element(By.CSS_SELECTOR,"div.conversation")
    conversation = conversation_div.find_element(By.CSS_SELECTOR,"div").text
    current = conversation.split('\n')
    start = time.time()
    # trolling
    while (time.time() - start) < 300:
        conversation_div = fb.browser.find_element(By.CSS_SELECTOR,"div.conversation")
        conversation = conversation_div.find_element(By.CSS_SELECTOR,"div").text
        lines = conversation.split('\n')
        # check for changes in conversation
        if len(lines) != len(current):
            new_lines = lines[len(current):len(lines)-1]
            question = ""
            for new_line in new_lines:
                question += new_line + " "
            print(question)
            answer = chatbot.Ask(question)
            textarea.send_keys(answer)
            textarea.send_keys(Keys.RETURN)
            conversation_div = fb.browser.find_element(By.CSS_SELECTOR,"div.conversation")
            conversation = conversation_div.find_element(By.CSS_SELECTOR,"div").text
            current = conversation.split('\n')
        time.sleep(10)
    # end conversation
    textarea.send_keys("I g2g! Peace out g fowg!")
    textarea.send_keys(Keys.RETURN)
    # close browser
    fb.destroy()

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
