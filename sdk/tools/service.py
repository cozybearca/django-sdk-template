import subprocess
from typing import List

from tools.volume import Mount


class Service:
    def __init__(self, id):
        self.id: str = id

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, o) -> bool:
        return self.id == o.id

    def get_mounts(self) -> List[Mount]:
        proc = subprocess.run(
            [
                "docker",
                "inspect",
                "-f",
                "{{range .Spec.TaskTemplate.ContainerSpec.Mounts}}{{.Type}} {{.Source}} {{.Target}}\n{{end}}",
                self.id,
            ],
            capture_output=True,
            check=True,
            text=True,
        )
        mounts = []
        output = proc.stdout.strip()
        for ln in output.splitlines():
            type, src, dest = ln.split()
            mounts.append(Mount(type=type, source=src, target=dest))
        return mounts

    def get_name(self):
        return subprocess.run(
            [
                "docker",
                "inspect",
                "-f",
                r"{{.Spec.Name}}",
                self.id,
            ],
            capture_output=True,
            check=True,
            text=True,
        ).stdout.strip()

    def get_image_name(self):
        return subprocess.run(
            [
                "docker",
                "inspect",
                "-f",
                r"{{.Spec.TaskTemplate.ContainerSpec.Image}}",
                self.id,
            ],
            capture_output=True,
            check=True,
            text=True,
        ).stdout.strip()

    @staticmethod
    def all():
        proc = subprocess.run(
            ["docker", "service", "ls", "--format", r"{{.ID}}"],
            text=True,
            capture_output=True,
        )
        return [Service(id=id) for id in proc.stdout.splitlines()]

    @staticmethod
    def from_name(name) -> "Service":
        proc = subprocess.run(
            [
                "docker",
                "service",
                "ls",
                "--filter",
                f"name={name}",
                "--format",
                r"{{.ID}}",
            ],
            text=True,
            capture_output=True,
        )
        result = [Service(id=id) for id in proc.stdout.splitlines()]
        if len(result) > 1:
            raise RuntimeError(
                f"Ambiguous service name {name}, found: {[r.get_name() for r in result]}"
            )
        if len(result) == 0:
            raise RuntimeError(f"Service {name} is not found.")
        return result[0]
