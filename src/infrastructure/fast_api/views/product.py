from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from src.domain.shared.exceptions.base import DomainException
from src.infrastructure.boto.authorization.authorization_microservice import (
    AuthorizationMicroservice,
)
from src.infrastructure.postgresql.repositories.product import ProductRepository
from src.interface_adapters.controllers.product import ProductController
from src.interface_adapters.gateways.authorization_microservice import (
    AuthorizationOutputDto,
)
from src.use_cases.product.find.find_product_dto import FindProductOutputDto
from src.use_cases.product.list.list_product_dto import ListProductOutputDto


router = APIRouter()


@router.get("/", response_model=list[ListProductOutputDto])
async def list_products(
    current_user: Annotated[
        AuthorizationOutputDto, Depends(AuthorizationMicroservice.authorize)
    ],
    category: str | None = None,
):
    try:
        return ProductController(
            ProductRepository(), current_user
        ).list_products(category)
    except UnauthorizedException as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )
    except DomainException as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/{product_uuid}/", response_model=FindProductOutputDto)
async def retrieve_product(
    product_uuid: str,
    current_user: Annotated[
        AuthorizationOutputDto, Depends(AuthorizationMicroservice.authorize)
    ],
):
    try:
        return ProductController(
            ProductRepository(), current_user
        ).retrieve_product(product_uuid)
    except UnauthorizedException as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )
    except DomainException as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )
