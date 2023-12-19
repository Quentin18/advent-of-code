from __future__ import annotations

from typing import NamedTuple


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
        return Rule(
            result=result,
            category=category,
            operator=operator,
            rate=int(rate),
        )

    def test(self, part: Part) -> bool:
        if self.operator == "<":
            return getattr(part, self.category) < self.rate

        if self.operator == ">":
            return getattr(part, self.category) > self.rate

        return True


class Workflow(NamedTuple):
    name: str
    rules: list[Rule]

    @staticmethod
    def parse(line: str) -> Workflow:
        name, rules = line.strip()[:-1].split("{")
        rules = [Rule.parse(rule) for rule in rules.split(",")]
        return Workflow(name=name, rules=rules)

    def get_result(self, part: Part) -> str:
        for rule in self.rules:
            if rule.test(part=part):
                return rule.result

        raise RuntimeError("all rules returned false")


class Part(NamedTuple):
    x: int
    m: int
    a: int
    s: int

    @staticmethod
    def parse(line: str) -> Part:
        ratings = line.strip()[1:-1].split(",")
        kwargs = {}
        for r in ratings:
            category, rate = r.split("=")
            kwargs[category] = int(rate)
        return Part(**kwargs)

    def accept(self, workflows: dict[str, Workflow]) -> bool:
        workflow = workflows["in"]
        result = workflow.get_result(part=self)
        while result not in "AR":
            workflow = workflows[result]
            result = workflow.get_result(part=self)
        return result == "A"

    def sum(self) -> int:
        return self.x + self.m + self.a + self.s


def main() -> None:
    blank_line = False
    workflows = {}
    parts = []

    with open("input.txt", "r", encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                blank_line = True
                continue

            if not blank_line:
                workflow = Workflow.parse(line=line)
                workflows[workflow.name] = workflow
            else:
                parts.append(Part.parse(line=line))

    result = sum(part.sum() for part in parts if part.accept(workflows=workflows))
    print(result)


if __name__ == "__main__":
    main()
