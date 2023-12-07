import sys
import argparse
from subprocess import run, PIPE
from dataclasses import dataclass
from datetime import datetime

sys.tracebacklimit = 0  # Ignore traceback for interupts


COMMAND = "kubectl get pods -A".split() + [
    "-o=jsonpath='"
    "{range .items[*]}"
    r'{.metadata.name}{" "}{.metadata.namespace}{" "}{.status.startTime}{"\n"}'
    "{end}'"
]


@dataclass
class Pod:
    name: str
    namespace: str
    time: datetime

    @classmethod
    def from_line(cls, line: str) -> "Pod":
        name, namespace, timestamp = line.strip().split()
        return cls(
            name=name,
            namespace=namespace,
            time=datetime.fromisoformat(timestamp.replace("Z", "+00:00")),
        )


class Pods(list):
    @property
    def sorted(self) -> list[Pod]:
        """Pods sorted newest to oldest"""
        return sorted(self, key=lambda p: p.time, reverse=True)


def pod_pattern_from_args() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "pod_name_pattern", help="Prefix of the name of a pod to follow the logs for"
    )
    return parser.parse_args().pod_name_pattern


def get_pods_stdout() -> str:
    process = run(COMMAND, stdout=PIPE)
    if process.returncode != 0:
        exit(process.returncode)
    return process.stdout.decode().strip("'").rstrip("\n")


def cli() -> None:
    pattern = pod_pattern_from_args()
    pods = Pods(Pod.from_line(line) for line in get_pods_stdout().split("\n"))

    for pod in pods.sorted:
        if pod.name.startswith(pattern):
            run(f"kubectl logs {pod.name} -n {pod.namespace} -f".split())

    exit("Failed to find a matching pod")


if __name__ == "__main__":
    cli()
