from decimal import Decimal
from uuid import UUID

from src.domain.aggregates.order.interfaces.order import (
    OrderInterface,
    OrderItemInterface,
)
from src.domain.aggregates.order.validators.order import OrderValidator
from src.domain.aggregates.order.value_objects.order_status import OrderStatus
from src.interface_adapters.gateways.repositories.order import OrderRepositoryInterface
from src.interface_adapters.gateways.repositories.product import (
    ProductRepositoryInterface,
)


class Order(OrderInterface):
    def __init__(
        self,
        items: list[OrderItemInterface],
        order_repository: OrderRepositoryInterface,
        payment_uuid: UUID,
        product_repository: ProductRepositoryInterface,
        uuid: UUID,
        status: OrderStatus = OrderStatus.PENDING_PAYMENT,
        user_uuid: UUID | None = None,
    ):
        self._items = items
        self._payment_uuid = payment_uuid
        self._status = status
        self._total_amount = self._get_total_amount(product_repository)
        self._user_uuid = user_uuid
        self._uuid = uuid
        self._validator = OrderValidator(
            self, order_repository, product_repository
        )
        self.validator.validate()

    @property
    def items(self):
        return self._items

    @property
    def status(self):
        return self._status

    @property
    def total_amount(self):
        return self._total_amount

    @property
    def user_uuid(self):
        if isinstance(self._user_uuid, UUID):
            return str(self._user_uuid)
        return None

    @property
    def uuid(self):
        return str(self._uuid)

    @property
    def validator(self):
        return self._validator

    def _get_total_amount(self, product_repository: ProductRepositoryInterface) -> str:
        total_amount = Decimal("0")
        for item in self.items:
            product = product_repository.find(item.product_uuid)
            total_amount += Decimal(str(item.quantity)) * Decimal(str(product.price))
        return str(total_amount)
