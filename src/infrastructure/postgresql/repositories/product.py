from src.domain.shared.exceptions.product import ProductNotFoundException
from src.infrastructure.postgresql.models.product import ProductModel
from src.interface_adapters.gateways.repositories.product import (
    ProductRepositoryDto,
    ProductRepositoryInterface,
)


class ProductRepository(ProductRepositoryInterface):
    def find(self, uuid):
        product = ProductModel.retrieve(uuid)
        if product is None:
            return None
        return ProductRepositoryDto(
            name=product.name,
            category=product.category,
            price=product.price,
            description=product.description,
            image=product.image,
            is_active=product.is_active,
            uuid=str(product.uuid),
        )

    def list(self, filters):
        products = ProductModel.list_filtering_by_column(filters)

        if products is None:
            return []

        return [
            ProductRepositoryDto(
                name=product[0].name,
                category=product[0].category,
                price=product[0].price,
                description=product[0].description,
                image=product[0].image,
                is_active=product[0].is_active,
                uuid=str(product[0].uuid),
            )
            for product in products
        ]
