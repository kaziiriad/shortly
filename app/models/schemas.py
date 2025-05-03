from pydantic import BaseModel, Field

class URLSchema(BaseModel):
    short_url: str = Field(..., description="The shortened URL")
    original_url: str = Field(..., description="The original URL")
    created_at: str = Field(..., description="The date and time when the URL was created")
    visits: int = Field(..., description="The number of visits to the shortened URL")

