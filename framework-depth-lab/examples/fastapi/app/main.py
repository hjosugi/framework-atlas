from itertools import count
from threading import Lock

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI(title="Framework Depth Lab Items API", version="1.0.0")


class Health(BaseModel):
    status: str


class CreateItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=100)
    price: float = Field(ge=0)


class Item(CreateItem):
    id: int = Field(ge=1)


class ItemStore:
    def __init__(self) -> None:
        self._items: dict[int, Item] = {}
        self._ids = count(1)
        self._lock = Lock()

    def create(self, request: CreateItem) -> Item:
        with self._lock:
            item = Item(id=next(self._ids), **request.model_dump())
            self._items[item.id] = item
            return item

    def get(self, item_id: int) -> Item | None:
        return self._items.get(item_id)


store = ItemStore()


@app.exception_handler(RequestValidationError)
def validation_error(_request: Request, _exception: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"code": "validation_error", "message": "request validation failed"},
    )


@app.exception_handler(HTTPException)
def http_error(_request: Request, exception: HTTPException) -> JSONResponse:
    code = "not_found" if exception.status_code == 404 else "http_error"
    return JSONResponse(
        status_code=exception.status_code,
        content={"code": code, "message": str(exception.detail)},
    )


@app.get("/healthz", response_model=Health)
def health() -> Health:
    return Health(status="ok")


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int) -> Item:
    item = store.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="item not found")
    return item


@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(request: CreateItem) -> Item:
    return store.create(request)
