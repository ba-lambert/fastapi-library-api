from pydantic import BaseModel, validator


class BookCreateSchema(BaseModel):
    title: str
    author: str
    published_year: int
    isbn: str
    description: str

    @validator('description')
    def description_length(cls, v):
        word_count = len(v.split())
        if word_count > 200:
            raise ValueError('Description must not be more than 200 characters')
        return v

    cover_url: str
    publisher: str
