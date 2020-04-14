import controller.__init__
import controller.load_resources
import view.__init__


class App:
    def __init__(self):
        self.view, self.controller = self._init_view_and_controller()

        self._start()

    def _init_view_and_controller(self):
        _view = view.View()
        _controller = controller.Controller()

        _view.set_controller(_controller)
        _controller.set_view(_view)

        return _view, _controller

    def _start(self):
        deck_ids = ('deck0', 'deck0')
        master_decks = tuple(controller.load_resources.get_master_deck(deck_id) for deck_id in deck_ids)
        self.controller.start(master_decks)


if __name__ == '__main__':
    app = App()

    # app.controller.request_action()

    print("fin")
