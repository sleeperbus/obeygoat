from django.contrib.auth import get_user_model
from functional_tests.base import FunctionalTest
from functional_tests.list_page import ListPage

User = get_user_model()


class MyListsTest(FunctionalTest):

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        email = 'a@b.com'
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email)

        # Edith is a logged-in user
        self.create_pre_authenticated_session(email)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(email)

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        # Edith is a logged-in user
        self.create_pre_authenticated_session('edith@example.com')

        # She goes to the home page and starts a list
        self.browser.get(self.live_server_url)
        list_page = ListPage(self)
        list_page.add_list_item('Reticulate splines')
        list_page.add_list_item('Immanentize eschaton')
        first_list_url = self.browser.current_url

        # She notices a "My lists" link, for the first time.
        self.browser.find_element_by_link_text('My lists').click()

        # She see that her list is in there, named according to its
        # first list item
        self.wait_for(lambda: self.browser.find_element_by_link_text('Reticulate splines'))

        self.browser.find_element_by_link_text('Reticulate splines').click()
        self.wait_for(lambda: self.assertEqual(self.browser.current_url, first_list_url))

        # She decides to start another list, just to see
        self.browser.get(self.live_server_url)
        list_page.add_list_item('Click cows')
        second_list_url = self.browser.current_url

        # Under "My lists", her new list appears
        self.browser.find_element_by_link_text('My lists').click()
        self.wait_for(lambda: self.browser.find_element_by_link_text('Click cows'))
        self.browser.find_element_by_link_text('Click cows').click()
        self.wait_for(lambda: self.assertEqual(second_list_url, self.browser.current_url))

        # She logs out. The "My lists" options disappears
        self.browser.find_element_by_link_text('Log out').click()
        self.wait_for(lambda: self.assertEqual(self.browser.find_elements_by_link_text('My lists'), []))
