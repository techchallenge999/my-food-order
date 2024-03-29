from abc import abstractmethod
from dataclasses import dataclass

from src.domain.aggregates.product.interfaces.product import ProductCategory
from src.domain.shared.interfaces.repository import RepositoryInterface


@dataclass
class ProductRepositoryDto:
    name: str
    category: ProductCategory
    price: float
    description: str
    image: bytes
    is_active: bool
    uuid: str


class ProductRepositoryInterface(RepositoryInterface):
    @abstractmethod
    def find(self, uuid: str) -> ProductRepositoryDto | None:
        pass

    @abstractmethod
    def list(self, filters: dict) -> list[ProductRepositoryDto]:
        pass
