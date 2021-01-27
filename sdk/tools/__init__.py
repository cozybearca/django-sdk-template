import os
import subprocess
from logging import getLogger
from pathlib import Path

from tools.task import Task

from .common import run

LOG = getLogger(__name__)
PROJ_NAME = os.environ["PROJ_NAME"]


def get_info_for_service(service, include_stopped=False):
    found = []
    for ln in run(
        ["docker", "stack", "ps", PROJ_NAME], capture_output=True, check=True, text=True
    ).stdout.split("\n"):
        if f"{PROJ_NAME}_{service}" in ln and ("Running" in ln or include_stopped):
            row = ln.split()
            task_id = row[0]
            task = Task(task_id)
            service_name = row[1]
            image_name = row[2]
            node_hostname = row[3]
            try:
                container_id = task.get_container_id()
                node_id = task.get_node_id()
                node_ip = ""
                for attempts, key in enumerate(
                    [r"{{.ManagerStatus.Addr}}", r"{{.Status.Addr}}"]
                ):
                    try:
                        node_ip = (
                            subprocess.run(
                                ["docker", "inspect", "-f", key, node_id],
                                capture_output=True,
                                check=True,
                                text=True,
                            )
                            .stdout.strip()
                            .split(":")[0]
                        )
                    except subprocess.CalledProcessError:
                        pass
                if not node_ip:
                    raise RuntimeError(f"Cannot find node ip for {service_name}")
                found.append(
                    {
                        "service_name": service_name,
                        "node_hostname": node_hostname,
                        "node_id": node_id,
                        "container_id": container_id,
                        "node_ip": node_ip,
                        "image_name": image_name,
                    }
                )
            except subprocess.CalledProcessError:
                if not include_stopped:
                    raise
    return found


def execute_docker_cp(info, src, dest, new_owner=None):
    # must use node_ip instead of hostname becuase ip is internal network
    # while hostname is external. For security reasons internal network
    # must be used
    cmd = ["docker", "-H", info["node_ip"], "cp"]
    cmd += [src, dest]
    print(cmd, flush=True)
    return run(cmd, stderr=subprocess.STDOUT, check=True)


def execute_docker_chown(info, file, owner=None):
    if not owner:
        owner = execute_docker_exec(
            info,
            user=None,
            cmd=["whoami"],
            run_kwargs=dict(capture_output=True, text=True),
        ).stdout.strip()
    return execute_docker_exec(
        info, user="root", cmd=["chown", f"{owner}:{owner}", file]
    )


def execute_docker_exec(info, cmd, user=None, it=True, run_kwargs={}):
    _cmd = ["docker", "-H", info["node_ip"], "exec"]
    if it:
        _cmd += ["-it"]
    if user:
        _cmd += ["--user", user]
    _cmd += [info["container_id"], *cmd]
    print(_cmd, flush=True)
    return run(_cmd, check=True, **run_kwargs)


def execute_docker_run(image, cmd, user=None, it=True, run_kwargs={}):
    _cmd = ["docker", "run", "--rm"]
    if it:
        _cmd += ["-it"]
    if user:
        _cmd += ["--user", user]
    _cmd += [image, *cmd]
    print(_cmd, flush=True)
    return run(_cmd, check=True, **run_kwargs)


def handle_get_info_for_service(service, node, include_stopped=False):
    instances = get_info_for_service(service, include_stopped=include_stopped)
    if not instances and not include_stopped:
        exit(f"Cannot find running an instance of {PROJ_NAME}_{service}")
    instances.sort(key=lambda x: x["node_hostname"])
    if not include_stopped:
        for idx, info in enumerate(instances, 1):
            print(" ", idx, info, flush=True)
        print(flush=True)
    if len(instances) > 1 and not include_stopped:
        if node is None:
            exit(
                f"found {len(instances)} running instances, please specify a node number."
            )
        else:
            return instances[node - 1]
    else:
        return instances[0]
