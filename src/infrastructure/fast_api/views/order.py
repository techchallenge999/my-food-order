from typing import Annotated

from fastapi import APIRouter, HTTPException, status as status_code, Depends

from src.domain.shared.exceptions.base import DomainException
from src.infrastructure.boto.authorization.authorization_microservice import (
    AuthorizationMicroservice,
)
from src.infrastructure.postgresql.repositories.order import OrderRepository
from src.infrastructure.postgresql.repositories.product import ProductRepository
from src.interface_adapters.controllers.order import OrderController
from src.interface_adapters.gateways.authorization_microservice import (
    AuthorizationOutputDto,
)
from src.interface_adapters.gateways.order_parser import CreateOrderParser
from src.use_cases.order.create.create_order_dto import (
    CreateOrderInputDto,
    CreateOrderOutputDto,
)
from src.use_cases.order.delete.delete_order_dto import DeleteOrderOutputDto
from src.use_cases.order.find.find_order_dto import FindOrderOutputDto
from src.use_cases.order.list.list_order_dto import ListOrderOutputDto
from src.use_cases.order.update.update_order_dto import (
    UpdateOrderItemsInputDto,
    UpdateOrderOutputDto,
)


router = APIRouter()


@router.post("/", status_code=201, response_model=CreateOrderOutputDto)
async def create_order(
    input_data: CreateOrderInputDto,
    current_user: Annotated[
        AuthorizationOutputDto, Depends(AuthorizationMicroservice.authorize)
    ],
):
    try:
        return OrderController(OrderRepository()).create_order(
            input_data,
            CreateOrderParser(),
            ProductRepository(),
            current_user,
        )
    except DomainException as err:
        raise HTTPException(
            status_code=status_code.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/", status_code=200, response_model=list[ListOrderOutputDto])
async def list_orders():
    try:
        return OrderController(OrderRepository()).list_orders()
    except DomainException as err:
        raise HTTPException(
            status_code=status_code.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/{order_uuid}/", status_code=200, response_model=FindOrderOutputDto)
async def retireve_order(order_uuid: str):
    try:
        return OrderController(OrderRepository()).retireve_order(order_uuid)
    except DomainException as err:
        raise HTTPException(
            status_code=status_code.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.put(
    "/{order_uuid}/update-items/", status_code=200, response_model=UpdateOrderOutputDto
)
async def update_order_items(
    order_uuid: str,
    input_data: UpdateOrderItemsInputDto,
):
    try:
        return OrderController(OrderRepository()).update_order_items(
            order_uuid,
            input_data,
            ProductRepository(),
        )
    except DomainException as err:
        raise HTTPException(
            status_code=status_code.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.put(
    "/{order_uuid}/progress-status/",
    status_code=200,
    response_model=UpdateOrderOutputDto,
)
async def progress_order_status(order_uuid: str):
    try:
        return OrderController(OrderRepository()).progress_order_status(
            order_uuid,
            ProductRepository(),
        )
    except DomainException as err:
        raise HTTPException(
            status_code=status_code.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.put(
    "/{order_uuid}/cancel/", status_code=200, response_model=UpdateOrderOutputDto
)
async def cancel_order(order_uuid: str):
    try:
        return OrderController(OrderRepository()).cancel_order(
            order_uuid,
            ProductRepository(),
        )
    except DomainException as err:
        raise HTTPException(
            status_code=status_code.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.delete("/{order_uuid}/", status_code=200, response_model=DeleteOrderOutputDto)
async def delete_order(order_uuid: str):
    try:
        return OrderController(OrderRepository()).delete_order(order_uuid)
    except DomainException as err:
        raise HTTPException(
            status_code=status_code.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )
