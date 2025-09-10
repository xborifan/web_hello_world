from uvicorn import run


def main():
    run("web.app:app", reload=True)
    #run("web.app:app", workers=2)

if __name__ == "__main__":
    main()
