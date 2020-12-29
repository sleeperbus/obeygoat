from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from functional_tests.base import FunctionalTest
from functional_tests.list_page import ListPage
from functional_tests.my_lists_page import MyListPage


def quit_if_possible(browser):
    try:
        browser.quit()
    except:
        pass


class SharingTest(FunctionalTest):
    def test_can_share_a_list_with_another_user(self):
        # Edith is a logged-in user
        self.create_pre_authenticated_session('edith@example.com')
        edith_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(self.browser))

        # Her friend Oniciferous is also hanging out on the lists site
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        oni_browser = webdriver.Chrome(chrome_options=chrome_options)
        self.addCleanup(lambda: quit_if_possible(oni_browser))
        self.create_pre_authenticated_session('oniciferous@example.com')

        # Edith goes to the home page and starts a list
        self.browser = edith_browser
        self.browser.get(self.live_server_url)
        list_page = ListPage(self).add_list_item('Get help')

        # She notices a "Share this list" option
        share_box = list_page.get_share_box()
        self.assertEqual(share_box.get_attribute('placeholder'), 'your-friend@example.com')

        # She shares her list.
        # The page updates to say that it's shared with Oniciferous:
        list_page.share_list_with('oniciferous@example.com')

        # Oniciferous now goes to the lists page with his browser
        self.browser = oni_browser
        MyListPage(self).go_to_my_list_page()

        # He see Edith's list in there!
        self.browser.find_element_by_link_text('Get help').click()

        # On the list page, Oniciferous can see says that it's Edith's list
        self.wait_for(lambda: self.assertEqual(list_page.get_list_owner(), 'edith@example.com'))
