import uvicorn
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv(".env")
    uvicorn.run("app:app", reload=True)
