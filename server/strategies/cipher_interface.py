from abc import ABC, abstractmethod

class CipherInterface(ABC):
    @abstractmethod
    def decrypt(self, text: str, key: str) -> str:
        """Mesajı deşifre eder."""
        pass