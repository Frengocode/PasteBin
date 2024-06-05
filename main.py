from fastapi import FastAPI
from authentication import authentication
from router.pastebin_router import router
from databse.database import Base, engine

Base.metadata.create_all(engine)

app = FastAPI(
    title='PasteBin'
)


app.include_router(router=router)
app.include_router(authentication.router)
