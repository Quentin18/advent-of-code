from __future__ import annotations

import uuid
from math import prod
from typing import NamedTuple

import networkx as nx

OPPOSITE_OPERATOR = {"<": ">", ">": "<"}


class Rule(NamedTuple):
    result: str
    category: str | None = None
    operator: str | None = None
    rate: int | None = None

    @staticmethod
    def parse(rule_str: str) -> Rule:
        rule_str = rule_str.strip()

        if ":" not in rule_str:
            return Rule(result=rule_str)

        operator = "<" if "<" in rule_str else ">"
        condition, result = rule_str.split(":")
        category, rate = condition.split(operator)

        # note: we add a suffix to have a different node in the graph for each A and R result
        if result in "AR":
            result += str(uuid.uuid4())

        return Rule(
            result=result,
            category=category,
            operator=operator,
            rate=int(rate),
        )

    def make_opposite(self) -> Rule:
        operator = OPPOSITE_OPERATOR[self.operator]
        rate = self.rate + 1 if operator == "<" else self.rate - 1
        return Rule(
            result=self.result,
            category=self.category,
            operator=operator,
            rate=rate,
        )


class Workflow(NamedTuple):
    name: str
    rules: list[Rule]

    @staticmethod
    def parse(line: str) -> Workflow:
        name, rules = line.strip()[:-1].split("{")
        rules = [Rule.parse(rule) for rule in rules.split(",")]
        return Workflow(name=name, rules=rules)


class Range(NamedTuple):
    lo: int = 1
    hi: int = 4000

    @property
    def length(self) -> int:
        assert self.hi >= self.lo
        return self.hi - self.lo + 1

    def apply_rule(self, rule: Rule) -> Range:
        if rule.operator == "<":
            return Range(lo=self.lo, hi=min(self.hi, rule.rate - 1))

        if rule.operator == ">":
            return Range(lo=max(self.lo, rule.rate + 1), hi=self.hi)

        raise RuntimeError("invalid rule operator")


class Ranges:
    def __init__(self) -> None:
        self.ranges = {key: Range() for key in "xmas"}

    def apply_rule(self, rule: Rule) -> None:
        if rule.category is None:
            return

        self.ranges[rule.category] = self.ranges[rule.category].apply_rule(rule=rule)

    def number_combinations(self) -> int:
        return prod(r.length for r in self.ranges.values())

    def __str__(self) -> str:
        return str(self.ranges)

    __repr__ = __str__


def generate_graph(workflows: dict[str, Workflow]) -> nx.DiGraph:
    graph = nx.DiGraph()
    for node, workflow in workflows.items():
        graph.add_node(node, workflow=workflow)

    for node, workflow in workflows.items():
        for rule in workflow.rules:
            assert not graph.has_edge(
                node,
                rule.result,
            ), f"edge ({node}, {rule.result}) already exists"
            graph.add_edge(node, rule.result, rules=workflow.rules)

    return graph


def main() -> None:
    workflows = {}

    with open("input.txt", "r", encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                break

            workflow = Workflow.parse(line=line)
            workflows[workflow.name] = workflow

    graph = generate_graph(workflows=workflows)

    total_combinations = 0
    target = [node for node in graph.nodes if node.startswith("A")]

    for path in nx.all_simple_paths(graph, source="in", target=target):
        ranges = Ranges()
        for u, v in zip(path[:-1], path[1:]):
            edge_data = graph.get_edge_data(u, v)
            rules: list[Rule] = edge_data["rules"]
            for rule in rules:
                if rule.result == v:
                    ranges.apply_rule(rule=rule)
                    break

                ranges.apply_rule(rule=rule.make_opposite())

        number_combinations = ranges.number_combinations()
        total_combinations += number_combinations

    print(total_combinations)


if __name__ == "__main__":
    main()
