"""Windows performance diagnostics that can be called from the chat client."""

import datetime
import os
import platform
import time
from typing import Any
from xml.parsers.expat import model
from langchain_core.tools import tool   
import psutil


def collect_windows_diagnostics(
    process_limit: int = 5,
    cpu_sample_seconds: float = 0.5,
) -> dict[str, Any]:
    """Collect a lightweight snapshot useful for investigating a slow Windows PC."""
    if platform.system() != "Windows":
        raise OSError("Windows diagnostics can only run on Windows.")
    if process_limit < 1:
        raise ValueError("process_limit must be at least 1.")

    memory = psutil.virtual_memory()
    disk = psutil.disk_usage(os.environ.get("SystemDrive", "C:") + "\\")
    processes = []

    process_handles = []
    for process in psutil.process_iter(["name", "pid", "memory_percent"]):
        try:
            process.cpu_percent(None)
            process_handles.append(process)
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            continue

    time.sleep(cpu_sample_seconds)
    for process in process_handles:
        try:
            cpu_percent = process.cpu_percent(None)
            processes.append(
                {
                    "name": process.info["name"] or "Unknown",
                    "pid": process.info["pid"],
                    "cpu_percent": round(cpu_percent, 1),
                    "memory_percent": round(
                        process.info["memory_percent"] or 0.0, 1
                    ),
                }
            )
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            continue

    return {
        "timestamp": datetime.datetime.now().astimezone().isoformat(
            timespec="seconds"
        ),
        "cpu_percent": round(psutil.cpu_percent(interval=0.2), 1),
        "cpu_count": psutil.cpu_count(),
        "memory_percent": round(memory.percent, 1),
        "memory_available_gb": round(memory.available / 1024**3, 2),
        "system_drive_percent": round(disk.percent, 1),
        "system_drive_free_gb": round(disk.free / 1024**3, 2),
        "uptime": str(
            datetime.timedelta(
                seconds=int(datetime.datetime.now().timestamp() - psutil.boot_time())
            )
        ),
        "top_cpu_processes": sorted(
            processes, key=lambda item: item["cpu_percent"], reverse=True
        )[:process_limit],
        "top_memory_processes": sorted(
            processes, key=lambda item: item["memory_percent"], reverse=True
        )[:process_limit],
    }


def format_windows_diagnostics(report: dict[str, Any]) -> str:
    """Turn a diagnostic report into concise text for a person or an AI model."""
    lines = [
        f"Windows diagnostic snapshot ({report['timestamp']})",
        f"CPU: {report['cpu_percent']}% across {report['cpu_count']} logical processors",
        (
            f"Memory: {report['memory_percent']}% used "
            f"({report['memory_available_gb']} GB available)"
        ),
        (
            f"System drive: {report['system_drive_percent']}% used "
            f"({report['system_drive_free_gb']} GB free)"
        ),
        f"Uptime: {report['uptime']}",
        "",
        "Top CPU processes:",
    ]
    lines.extend(
        f"- {process['name']} (PID {process['pid']}): "
        f"{process['cpu_percent']}% CPU, {process['memory_percent']}% memory"
        for process in report["top_cpu_processes"]
    )
    lines.append("Top memory processes:")
    lines.extend(
        f"- {process['name']} (PID {process['pid']}): "
        f"{process['cpu_percent']}% CPU, {process['memory_percent']}% memory"
        for process in report["top_memory_processes"]
    )
    return "\n".join(lines)


def run_windows_diagnostics() -> str:
    """ CRITICAL RULE: Call this tool ONLY if the user explicitly reports 
    that a Windows operating system machine is running slowly or lagging. 
    Do NOT call this tool for other OS types (Mac, Linux) or unrelated issues."""
    return format_windows_diagnostics(collect_windows_diagnostics())

results = run_windows_diagnostics()
print (results)