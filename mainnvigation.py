from abc import ABC, abstractmethod



class NavigationInterface(ABC):
    @abstractmethod
    def go_to_login(self):
        pass

    @abstractmethod
    def go_to_register(self):
        pass

    @abstractmethod
    def go_to_main_menu(self, user=None):
        pass

    @abstractmethod
    def go_to_login_screen(self):
        pass
