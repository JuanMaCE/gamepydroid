from abc import ABC, abstractmethod



class NavigationInterface(ABC):
    @abstractmethod
    def go_to_login(self):
        pass

    @abstractmethod
    def go_to_register(self):
        pass

    @abstractmethod
    def go_to_main_menu(self, id: int | None):
        pass

    @abstractmethod
    def go_to_login_screen(self):
        pass

    @abstractmethod
    def go_to_play(self):
        pass

    @abstractmethod
    def go_to_ranking(self):
        pass