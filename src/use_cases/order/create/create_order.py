from uuid import UUID, uuid4

from src.domain.aggregates.order.entities.order import Order
from src.domain.aggregates.order.value_objects.order_item import OrderItem
from src.interface_adapters.gateways.repositories.order import OrderRepositoryInterface
from src.interface_adapters.gateways.repositories.product import (
    ProductRepositoryInterface,
)
from src.use_cases.order.create.create_order_dto import (
    CreateOrderInputDto,
    CreateOrderItemOutputDto,
    CreateOrderOutputDto,
)


class CreateOrderUseCase:
    def __init__(
        self,
        order_repository: OrderRepositoryInterface,
        product_repository: ProductRepositoryInterface,
    ):
        self._order_repository = order_repository
        self._product_repository = product_repository

    def execute(self, input_data: CreateOrderInputDto) -> CreateOrderOutputDto:
        new_order = Order(
            items=[
                OrderItem(
                    comment=item.comment,
                    product_uuid=UUID(item.product_uuid),
                    quantity=item.quantity,
                )
                for item in input_data.items
            ],
            order_repository=self._order_repository,
            product_repository=self._product_repository,
            uuid=uuid4(),
            user_uuid=UUID(input_data.user_uuid)
            if isinstance(input_data.user_uuid, str)
            else None,
        )

        create_order_dto = CreateOrderOutputDto(
            items=[
                CreateOrderItemOutputDto(
                    comment=new_item.comment,
                    product_uuid=new_item.product_uuid,
                    quantity=new_item.quantity,
                )
                for new_item in new_order.items
            ],
            status=new_order.status,
            total_amount=new_order.total_amount,
            user_uuid=new_order.user_uuid,
            uuid=new_order.uuid,
        )

        self._order_repository.create(create_order_dto)

        return create_order_dto
