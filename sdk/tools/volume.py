from subprocess import run
from typing import Dict


class Mount:
    def __init__(self, type, source, target):
        self.type: str = type
        self.source: str = source
        self.target: str = target


class Volume:
    size_cache: Dict[str, str] = {}

    def __init__(self, name):
        self.name = name

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, o) -> bool:
        return self.name == o.name

    @staticmethod
    def all():
        proc = run(
            ["docker", "volume", "ls", "--format", r"{{.Name}}"],
            text=True,
            capture_output=True,
        )
        return [Volume(n) for n in proc.stdout.splitlines()]

    def get_size(self):
        if self.name in self.size_cache:
            return self.size_cache[self.name]
        else:
            proc = run(
                [
                    "docker",
                    "system",
                    "df",
                    "-v",
                    "--format",
                    r"{{range .Volumes}}{{.Name}} {{.Size}}\n{{end}}",
                ],
                text=True,
                capture_output=True,
            )
            for ln in proc.stdout.splitlines():
                name, size = ln.split()
                self.size_cache[name] = size
            return self.size_cache[self.name]
