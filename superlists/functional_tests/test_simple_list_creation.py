from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edit heard about a new online todo app. She goes to check out the homepage.
        self.browser.get(self.server_url)

        # She notices page title and header mentions to-do lists
        assert 'To-Do' in self.browser.title

        # She is invited to enter a to-do item.
        inputbox = self.get_item_input_box()
        assert inputbox.get_attribute("placeholder") == "Enter a to-do item"

        # She types "Buy peacock feathers" into a text box.
        buy_peacock_text = "Buy peacock feathers"
        inputbox.send_keys(buy_peacock_text)

        # When she hits enter, she is taken to a new URL and
        # the page updates and lists "1: Buy peacock feathers."
        inputbox.send_keys(Keys.ENTER)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, "/lists/.+")
        self.check_for_row_in_list_table("1: {0}".format(buy_peacock_text))

        # There is still a text box that invites her to add another item.
        # She enters "Use peacock feathers to make a fly."
        inputbox = self.get_item_input_box()
        make_fly_text = "Use peacock feathers to make a fly."
        inputbox.send_keys(make_fly_text)
        inputbox.send_keys(Keys.ENTER)

        # The page updates again and shows both items on her list.
        self.check_for_row_in_list_table("1: {0}".format(buy_peacock_text))
        self.check_for_row_in_list_table("2: {0}".format(make_fly_text))

        # Now a new user, Francis, comes along to the site.
        # (We use a new browser session to make sure that none of the info)
        # (from Edith's session is leaking through cookies, etc.)
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the home page and there is no sign of Edith's list.
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name("body").text
        assert buy_peacock_text not in page_text
        assert make_fly_text not in page_text

        # Francis starts a new list by entering a new item.
        inputbox = self.get_item_input_box()
        inputbox.send_keys("Buy milk")
        inputbox.send_keys(Keys.ENTER)

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, "/lists/.+")
        assert francis_list_url != edith_list_url

        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name("body").text
        assert buy_peacock_text not in page_text
        assert "Buy milk" in page_text

        # Satisfied, they both go back to sleep.
