from core.application import Application


app = Application()

if app.start():
    app.run(
        cycles=5
    )