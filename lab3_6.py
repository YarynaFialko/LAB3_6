"""
The module implies functionality of a notebook.
"""

import datetime
import sys
# Store the next available id for all new notes
last_id = 0


class Note:
    '''Represent a note in the notebook. Match against a
    string in searches and store tags for each note.'''

    def __init__(self, memo, tags=''):
        '''initialize a note with memo and optional
        space-separated tags. Automatically set the note's
        creation date and a unique id.
        >>> n1 = Note("hello first")
        >>> n2 = Note("hello again")
        >>> n1.id
        1
        >>> n2.id
        2
        '''
        self.memo = memo
        self.tags = tags
        self.creation_date = datetime.date.today()
        global last_id
        last_id += 1
        self.id = last_id

    def match(self, filter):
        '''Determine if this note matches the filter
        text. Return True if it matches, False otherwise.

        Search is case sensitive and matches both text and
        tags.
        >>> n1 = Note("hello first")
        >>> n2 = Note("hello again")
        >>> n1.match('hello')
        True
        >>> n2.match('second')
        False
        '''
        return filter in self.memo or filter in self.tags


class Notebook:
    '''Represents a collection of notes that can be tagged,
    modified, and searched.'''

    def __init__(self):
        '''
        Initialize a notebook with an empty list.
        >>> notebook1 = Notebook()
        >>> notebook1.notes
        []
        '''
        self.notes = []

    def new_note(self, memo, tags=''):
        '''
        Create a new note and add it to the list.
        >>> nb = Notebook()
        >>> nb.new_note("hello world")
        >>> nb.new_note("hello again")
        >>> nb.notes[0].id
        8
        >>> nb.notes[1].id
        9
        >>> nb.notes[0].memo
        'hello world'
        >>> len(nb.notes)
        2
        '''
        self.notes.append(Note(memo, tags))

    def search(self, filter):
        '''Find all notes that match the given filter
        string.
        >>> nn = Notebook()
        >>> nn.new_note("hello world")
        >>> nn.new_note("hello again")
        >>> nn.search("world")[0].memo
        'hello world'
        '''
        return [note for note in self.notes if note.match(filter)]

    def _find_note(self, note_id):
        '''Locate the note with the given id.
        >>> nn = Notebook()
        >>> nn.new_note("very important note 1")
        >>> id = nn.notes[0].id
        >>> nn._find_note(id).memo
        'very important note 1'
        '''
        for note in self.notes:
            if str(note.id) == str(note_id):
                return note
        return None

    def modify_memo(self, note_id, memo):
        '''Find the note with the given id and change its
        memo to the given value.
        >>> nbook = Notebook()
        >>> nbook.new_note("hello world")
        >>> nbook.notes[0].memo
        'hello world'
        >>> id = nbook.notes[0].id
        >>> nbook.modify_memo(id, "hi world")
        True
        >>> nbook.notes[0].memo
        'hi world'
        '''
        note = self._find_note(note_id)
        if note:
            note.memo = memo
            return True
        return False

    def modify_tags(self, note_id, tags):
        '''Find the note with the given id and change its
        tags to the given value.
        >>> n = Notebook()
        >>> n.new_note("hello", ["greet", "h"])
        >>> id = n.notes[0].id
        >>> n.modify_tags(id, ["greetins", "h", "hi"])
        True
        >>> n.notes[0].tags
        ['greetins', 'h', 'hi']
        '''
        note = self._find_note(note_id)
        if note:
            note.tags = tags
            return True
        return False


class Menu:
    '''Display a menu and respond to choices when run.'''

    def __init__(self):
        """ Receives a choise of a user navigating the app."""
        self.notebook = Notebook()
        self.choices = {
            "1": self.show_notes,
            "2": self.search_notes,
            "3": self.add_note,
            "4": self.modify_note,
            "5": self.quit
        }

    def display_menu(self):
        """
        Displays the menu.
        """
        print("""
        Notebook Menu
        1. Show all Notes
        2. Search Notes
        3. Add Note
        4. Modify Note
        5. Quit
        """)

    def run(self):
        '''Display the menu and respond to choices.'''
        while True:
            self.display_menu()
            choice = input("Enter an option: ")
            action = self.choices.get(choice)
            if action:
                action()
            else:
                print("{0} is not a valid choice".format(choice))

    def show_notes(self, notes=None):
        """Shows all notes."""
        if not notes:
            notes = self.notebook.notes
        for note in notes:
            print("{0}: {1}\n{2}".format(
                note.id, note.tags, note.memo))

    def search_notes(self):
        """Searches a note by its id."""
        filter = input("Search for: ")
        notes = self.notebook.search(filter)
        self.show_notes(notes)

    def add_note(self):
        """Adds a note tp the notebook."""
        memo = input("Enter a memo: ")
        self.notebook.new_note(memo)
        print("Your note has been added.")

    def modify_note(self):
        """Modifies an existing note in the  notebook."""
        id = input("Enter a note id: ")
        memo = input("Enter a memo: ")
        tags = input("Enter tags: ")
        if memo:
            self.notebook.modify_memo(id, memo)
        if tags:
            self.notebook.modify_tags(id, tags)

    def quit(self):
        """Thanks for using the notebook and quits the app."""
        print("Thank you for using your notebook today.")
        sys.exit(0)


if __name__ == "__main__":
    Menu().run()
