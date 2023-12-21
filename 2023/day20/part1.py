from __future__ import annotations

import sys
from dataclasses import dataclass
from enum import Enum

PUSHES = 1000


class Pulse(Enum):
    HIGH = "HIGH"
    LOW = "LOW"


class ModuleType(Enum):
    FLIP_FLOP = "%"
    CONJUNCTION = "&"
    BROADCAST = "broadcaster"


@dataclass
class Module:
    name: str
    type: ModuleType | None
    input_modules: list[Module]
    destination_modules: list[Module]
    is_on: bool = False
    last_pulse: Pulse = Pulse.LOW

    def process(self, pulse: Pulse) -> list[tuple[Module, Pulse]]:
        if self.type == ModuleType.FLIP_FLOP:
            if pulse == Pulse.HIGH:
                return []

            if not self.is_on:
                self.is_on = True
                sent_pulse = Pulse.HIGH
            else:
                self.is_on = False
                sent_pulse = Pulse.LOW

        elif self.type == ModuleType.CONJUNCTION:
            sent_pulse = (
                Pulse.LOW
                if all(module.last_pulse == Pulse.HIGH for module in self.input_modules)
                else Pulse.HIGH
            )

        elif self.type == ModuleType.BROADCAST:
            sent_pulse = pulse

        else:
            return []

        tasks = []
        for module in self.destination_modules:
            tasks.append((module, sent_pulse))
            if module.type == ModuleType.CONJUNCTION:
                self.last_pulse = sent_pulse

        return tasks


@dataclass
class ProcessingState:
    low_pulses: int
    high_pulses: int
    tasks: list[tuple[Module, Pulse]]

    def update_pulses(self, pulse: Pulse) -> None:
        if pulse == Pulse.LOW:
            self.low_pulses += 1
        elif pulse == Pulse.HIGH:
            self.high_pulses += 1
        else:
            raise ValueError("invalid pulse")


def read_modules(lines: list[str]) -> dict[str, Module]:
    modules = {}

    lines_dict = dict(line.strip().split(" -> ") for line in lines)
    for name in lines_dict.keys():
        if name == "broadcaster":
            module_type = ModuleType.BROADCAST
        else:
            module_type, name = ModuleType(name[0]), name[1:]
        modules[name] = Module(
            name=name,
            type=module_type,
            input_modules=[],
            destination_modules=[],
        )

    for destination_names in lines_dict.values():
        for name in destination_names.split(", "):
            if name in modules:
                continue

            modules[name] = Module(
                name=name,
                type=None,
                input_modules=[],
                destination_modules=[],
            )

    for input_name, destination_names in lines_dict.items():
        input_name = "broadcaster" if input_name == "broadcaster" else input_name[1:]
        destination_modules = [modules[name] for name in destination_names.split(", ")]
        modules[input_name].destination_modules = destination_modules
        for module in destination_modules:
            module.input_modules.append(modules[input_name])

    return modules


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        modules = read_modules(lines=file.readlines())

    state = ProcessingState(low_pulses=0, high_pulses=0, tasks=[])

    for _ in range(PUSHES):
        state.tasks = [(modules["broadcaster"], Pulse.LOW)]

        while state.tasks:
            next_tasks = []
            for module, pulse in state.tasks:
                state.update_pulses(pulse=pulse)
                next_tasks.extend(module.process(pulse=pulse))
            state.tasks = next_tasks

    print("low =", state.low_pulses, file=sys.stderr)
    print("high =", state.high_pulses, file=sys.stderr)
    print(state.low_pulses * state.high_pulses)


if __name__ == "__main__":
    main()
