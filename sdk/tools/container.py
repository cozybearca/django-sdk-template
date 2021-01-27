import subprocess
from typing import List

from tools.volume import Mount


class Container:
    def __init__(self, id):
        self.id = id

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, o) -> bool:
        return self.id == o.id

    def get_name(self) -> str:
        return (
            subprocess.run(
                [
                    "docker",
                    "inspect",
                    "-f",
                    r"{{.Name}}",
                    self.id,
                ],
                capture_output=True,
                check=True,
                text=True,
            )
            .stdout.strip()
            .lstrip("/")
        )

    def get_mounts(self) -> List[Mount]:
        proc = subprocess.run(
            [
                "docker",
                "container",
                "inspect",
                "--format",
                "{{range .Mounts}}{{.Type}},{{.Source}},{{.Name}},{{.Destination}}\n{{end}}",
                self.id,
            ],
            capture_output=True,
            check=True,
            text=True,
        )
        mounts = []
        output = proc.stdout.strip()
        for ln in output.splitlines():
            type, src, name, dest = ln.split(",")
            if type == "bind":
                mounts.append(Mount(type=type, source=src, target=dest))
            elif type == "volume":
                mounts.append(Mount(type=type, source=name, target=dest))
            else:
                raise ValueError(type)
        return mounts

    @staticmethod
    def all_local():
        proc = subprocess.run(
            ["docker", "container", "ls", "--all", "--format", r"{{.ID}}"],
            text=True,
            capture_output=True,
        )
        return [Container(id=id) for id in proc.stdout.splitlines()]
