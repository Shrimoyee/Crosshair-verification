class BrowserHistory:
    '''Simulates a web browser's back and forward navigation using stacks.'''

    def __init__(self):
        self.back_stack = []  # Stores visited pages
        self.forward_stack = []  # Stores pages when going back

    def visit_page(self, url: str):
        '''
        Visits a new web page.
        Preconditions:
        - url must be a non-empty string.
        Postconditions:
        - The URL must be added to the back stack.
        - The forward stack must be cleared.
        '''
        assert isinstance(url, str) and url.strip(), "Precondition: URL must be a non-empty string."

        self.back_stack.append(url)
        self.forward_stack.clear()  # Clear forward history when visiting a new page

        assert self.back_stack[-1] == url, "Postcondition: Last visited URL must be the new URL."
        assert len(self.forward_stack) == 0, "Postcondition: Forward stack must be empty."

    def show_history(self):
        '''Displays the current state of browser history.'''

        print(f"\n<- Back Stack: {self.back_stack}")
        print(f"-> Forward Stack: {self.forward_stack}")

    def go_back(self) -> str:
        '''
        Navigates back in history.
        # Preconditions:
        # - The back stack must have at least two pages.
        Postconditions:
        - The previous page is returned.
        - The removed page is pushed onto the forward stack.
        '''
        #assert len(self.back_stack) >= 1, "Precondition: Must have history to go back."
        if(len(self.back_stack) <= 1):
            return "No previous page"
        current_page = self.back_stack.pop()
        self.forward_stack.append(current_page)

        assert self.forward_stack[-1] == current_page, "Postcondition: Forward stack must contain the last visited page."
        return self.back_stack[-1]  # Return new top of stack (previous page)

    def go_forward(self) -> str:
        '''
        Navigates forward in history.
        # Preconditions:
        # - The forward stack must not be empty.
        Postconditions:
        - The top page is removed from forward stack and added back to history.
        '''
        #assert len(self.forward_stack) > 0, "Precondition: Must have pages in forward stack to go forward."
        if(len(self.forward_stack) < 0):
            return "No forward page"
        
        next_page = self.forward_stack.pop()
        self.back_stack.append(next_page)

        assert self.back_stack[-1] == next_page, "Postcondition: Back stack must contain the new page."
        return next_page

#To test manually
def main():
    browser = BrowserHistory()

    print("\n*** Visiting pages: ***")
    browser.visit_page("google.com")
    browser.visit_page("youtube.com")
    browser.visit_page("github.com")
    browser.show_history()

    print("\n<- Going back:")
    print(f"Back to: {browser.go_back()}")
    browser.show_history()

    print("\n<- Going back again:")
    print(f"Back to: {browser.go_back()}")
    browser.show_history()

    print("\n-> Going forward:")
    print(f"Forward to: {browser.go_forward()}")
    browser.show_history()

    print("\n*** Visiting a new page (clears forward history): ***")
    browser.visit_page("stackoverflow.com")
    browser.show_history()

    print("\n<- Trying to go back beyond history:")
    print(f"Back to: {browser.go_back()}")
    print(f"Back to: {browser.go_back()}")
    print(f"Back to: {browser.go_back()}") 

    print("\n-> Trying to go forward beyond available pages:")
    print(f"Forward to: {browser.go_forward()}") 

# Run manual test
if __name__ == "__main__":
    main()