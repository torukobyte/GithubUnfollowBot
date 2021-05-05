from userInfo import username, password
from selenium import webdriver
import selenium
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time


class Github:
    def __init__(self, username, password, flag=True, followers=[], following=[]):
        self.browser = webdriver.Chrome()
        self.username = username
        self.password = password
        self.flag = flag
        self.followers = followers
        self.following = following

    def signIn(self):

        # github login page
        self.browser.get("https://github.com/login")
        time.sleep(3)

        # we are getting username and password inputs
        usernameInput = self.browser.find_element_by_xpath('//*[@id="login_field"]')
        passwordInput = self.browser.find_element_by_xpath('//*[@id="password"]')

        # out imported userinfos -> sending to inputs
        usernameInput.send_keys(self.username)
        passwordInput.send_keys(self.password)

        # pressing enter to complete login
        passwordInput.send_keys(Keys.ENTER)
        time.sleep(3)

    def getFollowers(self):

        # going our followers tab to get our followers data
        self.browser.get("https://github.com/" + self.username + "?tab=followers")

        # getting follower count so we can run loop that much
        followerCount = self.browser.find_element_by_xpath(
            '//*[@id="js-pjax-container"]/div[2]/div/div[1]/div/div[4]/div[2]/div[3]/div/a[1]/span').text
        followerCount = int(followerCount)

        # getting our followers name
        for i in range(1, followerCount + 1):
            try:
                followerName = self.browser.find_element_by_xpath(
                    '//*[@id="js-pjax-container"]/div[2]/div/div[2]/div[2]/div/div[' + str(
                        i) + ']/div[2]/a/span[2]').text
                # appending to our empty follower list
                self.followers.append(followerName + "\n")
            except selenium.common.exceptions.NoSuchElementException:
                print("Your followers count not updated plz try again later..")
                self.flag = False

    def getFollowing(self):
        time.sleep(3)
        # going our following tab to get our followings data
        self.browser.get("https://github.com/" + self.username + "?tab=following")

        # getting following count so we can run loop that much
        followingCount = self.browser.find_element_by_xpath(
            '//*[@id="js-pjax-container"]/div[2]/div/div[1]/div/div[4]/div[2]/div[3]/div/a[2]/span').text
        followingCount = int(followingCount)

        # getting our followings name
        for i in range(1, followingCount + 1):
            try:
                followingName = self.browser.find_element_by_xpath(
                    '//*[@id="js-pjax-container"]/div[2]/div/div[2]/div[2]/div/div[' + str(
                        i) + ']/div[2]/a/span[2]').text
                # appending to our empty following list
                self.following.append(followingName + "\n")
            except selenium.common.exceptions.NoSuchElementException:
                print("Your following count not updated plz try again later..")
                self.flag = False

    def unfollow(self):
        self.getFollowers()
        self.getFollowing()

        if self.flag:
            notFollowing = []

            for i in self.following:
                if i not in self.followers:
                    notFollowing.append(i)

            if notFollowing != []:
                for i in notFollowing:
                    self.browser.get('https://github.com/' + i.strip())
                    time.sleep(3)
                    try:
                        unfollowButton = self.browser.find_element_by_xpath(
                            '//*[@id="js-pjax-container"]/div[2]/div/div[1]/div/div[3]/div[1]/div/div/span/form['
                            '2]/input[2]')
                        unfollowButton.click()
                        time.sleep(3)
                    except NoSuchElementException:
                        unfollowButton = self.browser.find_element_by_xpath(
                            '//*[@id="js-pjax-container"]/div[2]/div/div[1]/div/div[4]/div[1]/div/div/span/form['
                            '2]/input[2]')
                        unfollowButton.click()
                        time.sleep(3)

                self.browser.close()
                print("task completed!")
            else:
                print("Everyone you are following also following you :)")
                self.browser.close()
        else:
            self.browser.close()


github = Github(username, password)
github.signIn()
github.unfollow()
