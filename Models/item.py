from fastapi import UploadFile

class Item:
    id: int
    type: str
    description: str
    tags: str
    image: UploadFile
