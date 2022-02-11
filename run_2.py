import logging
import sys

from direct.showbase.ShowBase import ShowBase
from direct.task.TaskManagerGlobal import taskMgr as TaskManager
from panda3d.core import ConfigVariableString

from server.core.attempt2.server import ServerCore

# Handle loggers
root = logging.getLogger()
root.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
root.addHandler(handler)

# No Window
ConfigVariableString("window-type", "none").setValue("none")

# If file is called directly
if __name__ == "__main__":
    app = ShowBase()

    server = ServerCore(9099, 1000)
    server()

    # Tasks
    TaskManager.add(server.taskTCPListenerPolling, "ConnectionListener")
    TaskManager.add(server.taskTCPReaderPolling, "ConnectionReader")
    TaskManager.add(
        server.client_manager.updatePlayers,
        "UpdatePlayerPositions",
        extraArgs=[server, None, "positions"],
    )

    app.run()
