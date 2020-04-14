import uvicorn

import controller.__init__
import networking

app = controller.__init__.app

if __name__ == "__main__":
    uvicorn.run("run_controller:app", port=networking.CONTROLLER_PORT, reload=True, log_level='debug')
