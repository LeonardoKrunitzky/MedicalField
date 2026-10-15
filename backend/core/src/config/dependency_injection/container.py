from injector import Injector

from backend.core.src.config.dependency_injection.domain import DomainModule


container = Injector([
    DomainModule(),
])