from injector import Injector

from src.config.dependency_injection.clients import ClientsModule
from src.config.dependency_injection.domain import DomainModule


container = Injector([
    DomainModule(),
    ClientsModule()
])