from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time, datetime, random, apiai, json, codecs
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
option=Options()
option.add_argument('user-data-dir=selenium')
class Whatspy:
    def __init__(self, browser):
        browser = browser.lower()
        if browser == "firefox":
            self.driver = webdriver.Firefox()
        elif browser == "chrome":
            self.driver = webdriver.Chrome(chrome_options=option)
        else:
            raise Exception("Unknown driver")
        self.Class_ChatHead = '_1wjpf'
        self.Class_MsgHead = 'emojitext ellipsify'
        self.Class_MsgData = 'message message-chat message-in tail message-chat'
        self.Class_UnreadMsg = 'chat unread'
        self.Class_Attach = 'Attach'
        self.Class_LastSeen = '"pane-chat-header"'
        self.Class_LastSeenList = ["_3sgkv"]
        self.Class_Status = "pane-chat-header"
        self.Class_StatusList = ["selectable-text"]
        self.Class_Mute1 = "_3I_df"
        self.Class_Mute2 = "_3DeDN"
        self.Class_MuteList = ["PNlAR"]
        self.Class_Block = "_2QrOO"
        self.Class_Unblock = "_10xEB"
        self.Class_Delete = "_1Vw8y"
        self.Class_GetChat = "_9tCEa"
           
    def login(self):
        self.driver.get('https://web.whatsapp.com/')
        input("Scan QR Code to connect with whatsApp. Press Enter after scanning the QR Code.")
        print("Logging in...")
        time.sleep(2)
        print("Login Success!")

    def web_driver_quit(self):
        self.driver.quit()
        quit()

    def goto_chat_head(self, name):
        try:
            chatHeads = self.driver.find_elements_by_xpath("//span[@class='" + self.Class_ChatHead + "']")
            for head in chatHeads:
                if head.text == name:
                    head.click()
                    print("Opening chat head")
                    break
        except:
            print("Error: No user of name '" + name + "' was found")

    def send_message(self, to, msg):
        try:
            self.goto_chat_head(to)
            textField = self.driver.find_element_by_xpath("//div[@contenteditable='true']")
            textField.send_keys(msg)
            textField.send_keys(Keys.RETURN)
            print("Message Sent Successfully")
            return
        except:
            print("Error: Message not sent")
            return

    def read_last_message(self, of):
        try:
            msgs = self.driver.find_elements_by_xpath("//span[@class='" + self.Class_MsgHead + "']")
            for head in msgs:
                if head.text == of:
                    head.click()
                    break
            data = self.driver.find_elements_by_xpath("//div[@class='" + self.Class_MsgData + "']")
            msg = data[len(data) - 1].text
            print(msg[-7:])
            print(of + " sent '" + msg[:-8].replace("\\n", "") + "' at " + str(msg[-7:]))
        except:
            print("Error: Unable to read last message")

    def get_unread_chats_title(self):
        try:
            msgs = []
            element = self.driver.find_elements_by_xpath("//div[@class='"+self.Class_UnreadMsg+"']")
            for e in element:
                msgs.append(e.text)

                # data = e.text.splitlines()
                # for d in data:
                #     msgs.append(d)

            print("Most recent unread messages:")

            for msg in msgs:
                temp = msg.splitlines()

                if (len(temp) == 4):
                    print(temp[3] + " new message(s) from " + temp[0] + " (received: " + str(temp[1]) + ") saying: " +
                          temp[2])
                elif (len(temp) == 5):
                    print(temp[4] + " new message(s) from " + temp[2][:-1] + " in group " + temp[
                        0] + " (received: " + str(
                        temp[1]) + ") saying: " + temp[3])


                    # for i in range(int(len(msgs)/4)):
                    #     print(msgs[4*i+3]+" new message(s) from "+msgs[4*i]+" received at "+str(msgs[4*i+1])+" saying: "+msgs[i*4+3])
        except:
            print("Error: unable to get unread chat titles")

    def send_media(self, to, caption, filepath):
        self.goto_chat_head(to)
        time.sleep(3)
        self.driver.find_element_by_xpath('//*[@title="'+self.Class_Attach+'"]').click()
        classname = ['_10anr', 'vidHz', '_3asN5']
        for name in classname:
            try:
                self.driver.find_element_by_class_name(name).click()
            except:
                pass

        flag = False

        try:
            if not flag:
                self.driver.find_element_by_xpath("//*[@accept='image/*,video/*']").send_keys(filepath)
                flag = True
        except:
            pass

        time.sleep(3)

        web_obj = self.driver.find_element_by_xpath("//div[@contenteditable='true']")
        web_obj.send_keys(caption)
        web_obj.send_keys(Keys.RETURN)

    def spam_bomb(self, to, msg, media, number):
        try:
            for i in range(number):
                time.sleep(4)
                if (media):
                    self.send_media(to, random.choice(msg), random.choice(media))
                else:
                    self.send_message(to, random.choice(msg))
        except:
            print("Error: Something went wrong")

    def get_last_seen_of(self, of):
        try:
            self.goto_chat_head(of)
            self.driver.find_element_by_class_name(self.Class_LastSeen).click()
            time.sleep(3)
            for classname in self.Class_LastSeenList:
                print(self.driver.find_element_by_class_name(classname).text)
        except:
            print("Error: Failed to get last seen")

    def get_status_of(self, of):
        try:
            self.goto_chat_head(of)
            self.driver.find_element_by_class_name(self.Class_Status).click()
            time.sleep(3)
            for classname in self.Class_LastSeenList:
                print(self.driver.find_elements_by_css_selector('span.' + classname)[1].text)
        except:
            print("Error: Failed to get status")

    def mute_chat(self, of, muteFor):
        try:
            self.goto_chat_head(of)
            self.driver.find_element_by_class_name(self.Class_LastSeen).click()
            time.sleep(3)
            self.driver.find_element_by_class_name(self.Class_Mute1).click()
            time.sleep(0.5)
            self.driver.find_elements_by_class_name(self.Class_Mute2)[muteFor].click()
            for classname in self.Class_MuteList:
                self.driver.find_element_by_class_name(classname).click()
            print("Muted " + of)
        except:
            print("Error: Failed to mute chat")

    def unmute_chat(self, of):
        try:
            self.goto_chat_head(of)
            self.driver.find_element_by_class_name(self.Class_LastSeen).click()
            time.sleep(3)
            self.driver.find_element_by_class_name(self.Class_Mute1).click()
            time.sleep(0.5)
            for classname in self.Class_MuteList:
                self.driver.find_element_by_class_name(classname).click()
            print("Unmuted " + of)
        except:
            print("Error: Failed to un-mute chat")

    def block_contact(self, of):
        try:
            self.goto_chat_head(of)
            self.driver.find_element_by_class_name(self.Class_LastSeen).click()
            time.sleep(3)
            self.driver.find_element_by_class_name(self.Class_Block).click()
            time.sleep(0.5)
            for classname in self.Class_MuteList:
                self.driver.find_element_by_class_name(classname).click()
            print("Blocked " + of)
        except:
            print("Error: Failed to block " + of)

    def unblock_contact(self, of):

        try:
            self.goto_chat_head(of)
            self.driver.find_element_by_class_name(self.Class_LastSeen).click()
            time.sleep(3)
            self.driver.find_element_by_class_name(self.Class_Unblock).click()
            time.sleep(0.5)
            for classname in self.Class_MuteList:
                self.driver.find_element_by_class_name(classname).click()
            print("Unblocked " + of)
        except:
            print("Error: Failed to unblock " + of)

    def delete_chat(self, of):
        try:
            self.goto_chat_head(of)
            self.driver.find_element_by_class_name(self.Class_LastSeen).click()
            time.sleep(3)
            self.driver.find_elements_by_class_name(self.Class_Delete)[1].click()
            time.sleep(0.5)
            for classname in self.Class_MuteList:
                self.driver.find_element_by_class_name(classname).click()
            print("Deleted chat of " + of)
        except:
            print("Error: Failed to delete chat of " + of)

    def get_chat(self, of):
        try:
            self.goto_chat_head(of)
            time.sleep(1)
            self.driver.find_element_by_class_name(self.Class_GetChat).click()
            actions = ActionChains(self.driver)
            for i in range(3):
                time.sleep(5)
                actions.send_keys(Keys.CONTROL + Keys.HOME)
                actions.perform()
                print("Loading chat...")
            time.sleep(2)
            msgs = self.driver.find_elements_by_class_name("message")
            for msg in msgs:
                txt = msg.text.splitlines()
                lastIndex = len(txt)
                text = ''.join(str(e) for e in txt[:lastIndex - 1])
                if len(text) < 2:
                    text = "<EMOJI>"

                if len(txt) == 1:
                    text = txt[len(txt) - 1]

                if "message-call_log" in msg.get_attribute("class"):
                    print("Call Log: " + text)
                elif "message-in" in msg.get_attribute("class"):
                    print("IN[" + txt[lastIndex - 1] + "]: " + text)
                elif "message-image" in msg.get_attribute("class"):
                    print("OUT[" + txt[lastIndex - 1] + "]: <MEDIA> " + text)
                elif "message-out" in msg.get_attribute("class"):
                    print("OUT[" + txt[lastIndex - 1] + "]: " + text)
                elif "message-system" in msg.get_attribute("class"):
                    print("Chat From " + text)

        except:
            print("Error: Can't fetch the chat with " + of)

    def auto_responder(self, mode, replies, token):
        try:
            if mode == 1:
                self.establish_connection_apiai(token)
                self.listen_for_incoming_msgs(mode=mode, replies=False)
            elif mode == 2:
                self.listen_for_incoming_msgs(mode=mode, replies=replies)
        except:
            pass

    def establish_connection_apiai(self, token):
        try:
            self.CLIENT_ACCESS_TOKEN = token
            self.ai = apiai.ApiAI(self.CLIENT_ACCESS_TOKEN)
            self.request = self.ai.text_request()
            self.request.lang = 'de'  # optional, default value equal 'en'
        except:
            print("Error: Unable to connect to Dialogflow")

    def generate_reply_apiai(self, query):
        try:
            self.request.query = query
            response = self.request.getresponse()
            reader = codecs.getreader("utf-8")
            obj = json.load(reader(response))
            txt = obj['result']['fulfillment']['speech']
            return txt
        except:
            return False

    def listen_for_incoming_msgs(self, mode, replies):
        try:
            print("Starting Listening. Press ctrl+c to stop listening")
            while (True):
                time.sleep(10)
                self.driver.refresh()
                parentElement = self.driver.find_elements_by_class_name("_3j7s9")[0]
                try:
                    # time.sleep(2)
                    print("WORKING++++++++++++++++++++++++++++++++++++++++++++")
                    new_msg = parentElement.find_element_by_class_name("OUeyt")
                    sender = parentElement.text.splitlines()[0]
                    msg = parentElement.text.splitlines()[2]
                    if msg == "typing…":
                        print(sender + " is typing...")
                    else:
                        print("New msg from " + sender + ": " + msg)
                        if mode == 1:
                            print("here")
                            reply = self.generate_reply_apiai(parentElement.text[0])
                            print("Replying with: " + reply)
                            self.send_message(sender, reply)
                        elif mode == 2:
                            print("")
                            reply = random.choice(replies)
                            self.send_message(sender, reply)



                except:
                    pass
        except KeyboardInterrupt:
            print("Error...")


whatspy = Whatspy("chrome")
whatspy.login()

# whatspy.auto_responder(1, False, '7d269ea56f1242ce89349216269ee65a')


whatspy.get_chat("Munib")
# whatspy.get_chat("Munib")

# whatspy.delete_chat("Hamza Fast")
# whatspy.unmute_chat("Munib")
# choice = int(input("Enter '1' to mute for 8 Hours.\nEnter '2' to mute for 1 week.\nEnter '3' to mute for 1 year.\n"))
# while choice >= 4 and choice <= 0:
#     choice = int(
#         input(
#             "INVALID CHOICE!\nEnter '1' to mute for 8 Hours.\nEnter '2' to mute for 1 week.\nEnter '3' to mute for 1 year.\n"))
# whatspy.mute_chat("Munib",choice-1)

# whatspy.get_status_of("Munib")
# whatspy.get_unread_chats_title()
# whatspy.send_media("Munib","Jarvis Test","E:/1.jpg")
whatspy.spam_bomb("Munib", ["Abe Ja"], False, 100)
