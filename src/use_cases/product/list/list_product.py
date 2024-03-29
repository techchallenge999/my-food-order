from src.domain.aggregates.product.interfaces.product import ProductCategory
from src.domain.shared.exceptions.product import InvalidProductCategoryException
from src.interface_adapters.gateways.repositories.product import (
    ProductRepositoryInterface,
)
from src.use_cases.product.list.list_product_dto import ListProductOutputDto


class ListProductUseCase:
    def __init__(
        self,
        repository: ProductRepositoryInterface,
    ):
        self._repository = repository

    def execute(
        self, filters: dict = {}
    ) -> list[ListProductOutputDto]:
        if "category" in filters.keys():
            try:
                ProductCategory[filters["category"]]
            except ValueError as err:
                raise InvalidProductCategoryException(err.args[0])

        product_list = self._repository.list(filters)

        if product_list is None:
            return []

        return [
            ListProductOutputDto(
                name=product.name,
                category=product.category,
                price=product.price,
                description=product.description,
                image=product.image,
                is_active=product.is_active,
                uuid=product.uuid,
            )
            for product in product_list
        ]
