from threading import Thread
from server import app, run_analytics

if __name__ == '__main__':
    Thread(target=run_analytics).start()
    app.run()