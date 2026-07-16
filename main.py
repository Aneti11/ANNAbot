from core.dispatcher import Dispatcher
from modules.m00_test import TestModule


app = Dispatcher()

app.register_module(TestModule())

app.start()
app.run_modules()