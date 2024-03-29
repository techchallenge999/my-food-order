from uuid import UUID

from src.domain.aggregates.order.interfaces.order import OrderInterface
from src.domain.aggregates.order.value_objects.order_status import OrderStatus
from src.domain.shared.exceptions.base import InvalidUUIDException
from src.domain.shared.exceptions.order import InvalidOrderStatusException
from src.domain.shared.exceptions.product import UnavailableProductException
from src.domain.shared.interfaces.validator import ValidatorInterface
from src.interface_adapters.gateways.repositories.order import OrderRepositoryInterface
from src.interface_adapters.gateways.repositories.product import (
    ProductRepositoryInterface,
)


class OrderValidator(ValidatorInterface):
    def __init__(
        self,
        domain_object: OrderInterface,
        order_repository: OrderRepositoryInterface,
        product_repository: ProductRepositoryInterface,
    ):
        self._order = domain_object
        self._order_repository = order_repository
        self._product_repository = product_repository

    def validate(self):
        self._raise_if_has_unavailable_product()
        self._raise_if_invalid_order_status()
        self._raise_if_invalid_uuid()

    def _raise_if_has_unavailable_product(self) -> None:
        if self._has_unavailable_product():
            raise UnavailableProductException()

    def _raise_if_invalid_order_status(self) -> None:
        if self._is_invalid_order_status():
            raise InvalidOrderStatusException()

    def _raise_if_invalid_uuid(self) -> None:
        if self._is_invalid_uuid():
            raise InvalidUUIDException()

    def _has_unavailable_product(self) -> bool:
        for item in self._order.items:
            if self._product_repository.find(item.product_uuid) is None:
                return True
        return False

    def _is_invalid_order_status(self) -> bool:
        return not isinstance(self._order.status, OrderStatus)

    def _is_invalid_uuid(self) -> bool:
        try:
            return not isinstance(UUID(self._order.uuid), UUID)
        except ValueError:
            return True
