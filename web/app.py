from fastapi import FastAPI


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/users/{id}")
def get_user_info(id: int) -> dict:
    #return "hi"
    return {"user_id": id, "user_name": "boris"}
