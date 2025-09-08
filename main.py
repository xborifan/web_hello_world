from uvicorn import run


def main():
    run("web.app:app", reload=True)

if __name__ == "__main__":
    main()
