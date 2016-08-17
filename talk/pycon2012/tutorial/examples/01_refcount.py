
def wrong():
    open("file").write("data")
    assert open("file").read() == "data"

def right():
    with open("file") as f:
        f.write("data")
    # contents *will be there* by now
