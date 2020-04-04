import uvicorn as uvicorn

import view.networking
import networking

app = view.networking.app

if __name__ == "__main__":
    uvicorn.run("run_view:app", port=networking.VIEW_PORT, reload=True, log_level='debug')
