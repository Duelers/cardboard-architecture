import uvicorn as uvicorn

import view.__init__
import networking

app = view.__init__.app

if __name__ == "__main__":
    uvicorn.run("run_view:app", port=networking.VIEW_PORT, reload=True, log_level='debug')
