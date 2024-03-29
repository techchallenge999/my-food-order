from src.domain.aggregates.product.interfaces.product import ProductCategory
from src.interface_adapters.gateways.authorization_microservice import (
    AuthorizationOutputDto,
)
from src.interface_adapters.gateways.repositories.product import (
    ProductRepositoryInterface,
)
from src.use_cases.product.find.find_product import FindProductUseCase
from src.use_cases.product.find.find_product_dto import (
    FindProductInputDto,
    FindProductOutputDto,
)
from src.use_cases.product.list.list_product import ListProductUseCase
from src.use_cases.product.list.list_product_dto import ListProductOutputDto


class ProductController:
    def __init__(
        self,
        repository: ProductRepositoryInterface,
        current_user: AuthorizationOutputDto,
    ):
        self.repository = repository
        self.current_user = current_user

    def list_products(self, category: str | None = None) -> list[ListProductOutputDto]:
        filters = {}
        if category is not None:
            filters["category"] = ProductCategory(category).name

        list_use_case = ListProductUseCase(
            repository=self.repository
        )

        return list_use_case.execute(self.current_user.uuid, filters)

    def retrieve_product(self, product_uuid: str) -> FindProductOutputDto | None:
        find_use_case = FindProductUseCase(
            repository=self.repository
        )
        return find_use_case.execute(
            FindProductInputDto(uuid=product_uuid), self.current_user.uuid
        )
