import uvicorn

import controller.action_networking
import networking

app = controller.action_networking.app

if __name__ == "__main__":
    uvicorn.run("run_controller:app", port=networking.CONTROLLER_PORT, reload=True, log_level='debug')
