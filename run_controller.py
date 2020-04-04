import uvicorn

import controller.networking_from_view
import networking

app = controller.networking_from_view.app

if __name__ == "__main__":
    uvicorn.run("run_controller:app", port=networking.CONTROLLER_PORT, reload=True, log_level='debug')
