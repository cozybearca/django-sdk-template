import subprocess
from typing import List

from tools.volume import Mount


def get_all_stacks():
    # stacks have no IDs
    proc = subprocess.run(
        ["docker", "stack", "ls", "--format", r"{{.Name}}"],
        text=True,
        capture_output=True,
    )
    return proc.stdout.splitlines()


class Task:
    def __init__(self, id):
        self.id = id
        self.node_id = None
        self.container_id = None
        self.service_name = None
        self.node_hostname = None
        self.image_name = None

    def get_container_id(self):
        return subprocess.run(
            [
                "docker",
                "inspect",
                "-f",
                r"{{.Status.ContainerStatus.ContainerID}}",
                self.id,
            ],
            capture_output=True,
            check=True,
            text=True,
        ).stdout.strip()

    def get_node_id(self):
        return subprocess.run(
            ["docker", "inspect", "-f", r"{{.NodeID}}", self.id],
            capture_output=True,
            check=True,
            text=True,
        ).stdout.strip()

    def get_mounts(self) -> List[Mount]:
        proc = subprocess.run(
            [
                "docker",
                "inspect",
                "-f",
                r"{{range .ContainerSpec.Mounts}}{{.Type}} {{.Source}} {{.Target}}{{end}}",
                self.id,
            ],
            capture_output=True,
            check=True,
            text=True,
        ).stdout.strip()
        mounts = []
        for ln in proc.stdout:
            type, src, dest = ln.split()
            mounts.append(Mount(type=type, source=src, target=dest))
        return mounts
