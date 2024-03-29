from src.domain.shared.exceptions.product import (
    ProductNotFoundException,
    UnavailableProductException,
)
from src.interface_adapters.gateways.repositories.product import (
    ProductRepositoryInterface,
)
from src.use_cases.product.find.find_product_dto import (
    FindProductInputDto,
    FindProductOutputDto,
)


class FindProductUseCase:
    def __init__(
        self,
        repository: ProductRepositoryInterface,
    ):
        self._repository = repository

    def execute(
        self, input_data: FindProductInputDto
    ) -> FindProductOutputDto | None:

        product = self._repository.find(uuid=input_data.uuid)

        if product is None:
            raise ProductNotFoundException()
        if not product.is_active:
            raise UnavailableProductException()

        return FindProductOutputDto(
            name=product.name,
            category=product.category,
            price=product.price,
            description=product.description,
            image=product.image,
            is_active=product.is_active,
            uuid=product.uuid,
        )
