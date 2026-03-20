from abc import ABC, abstractmethod

class Rule(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def test(self, value):
        pass

    def evaluate(self, value):
        passed = self.test(value)
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {self.name}: {value}")
        result = passed
        return result

class MinLengthRule(Rule):
    def __init__(self, min_len):
        super().__init__(f"MinLength({min_len})")
        self.min_len = min_len

    def test(self, value):
        result = len(value) >= self.min_len
        return result

class HasUppercaseRule(Rule):
    def __init__(self):
        super().__init__("HasUppercase")

    def test(self, value):
        result = any(ch.isupper() for ch in value)
        return result

class HasSpecialCharRule(Rule):
    def __init__(self):
        super().__init__("HasSpecialChar")

    def test(self, value):
        result = any(not ch.isalnum() for ch in value)
        return result

class NoRepeatingCharsRule:
    def __init__(self):
        self.name = "NoRepeatingChars"

    def test(self, value):
        result = all(value[i] != value[i+1] for i in range(len(value)-1))
        return result

    def evaluate(self, value):
        passed = self.test(value)
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {self.name}: {value}")
        result = passed
        return result

class StrengthReport:
    def __init__(self):
        self.entries = []

    def add(self, rule_name, value, passed):
        self.entries.append((rule_name, value, passed))

    def summary(self):
        total = len(self.entries)
        passed = sum(1 for e in self.entries if e[2])
        failed = total - passed
        print(f"Total: {total}, Passed: {passed}, Failed: {failed}")
        result = (total, passed, failed)
        return result

class PasswordField:
    def __init__(self, field_name):
        self.field_name = field_name
        self.rules = []
        self.report = StrengthReport()

    def add_rule(self, rule):
        self.rules.append(rule)

    def check(self, value):
        print(f'Checking {self.field_name}: "{value}"')
        all_passed = True
        for rule in self.rules:
            passed = rule.evaluate(value)
            self.report.add(rule.name, value, passed)
            if not passed:
                all_passed = False
        result = all_passed
        return result

    def show_report(self):
        print(f"--- Report for {self.field_name} ---")
        result = self.report.summary()
        return result


password_field = PasswordField('password')
password_field.add_rule(MinLengthRule(8))
password_field.add_rule(HasUppercaseRule())
password_field.add_rule(HasSpecialCharRule())
password_field.add_rule(NoRepeatingCharsRule())

valid1 = password_field.check('Str0ng!Pw')
print(f'Valid: {valid1}\n')

valid2 = password_field.check('short')
print(f'Valid: {valid2}\n')

valid3 = password_field.check('aabbccdd!!')
print(f'Valid: {valid3}\n')

password_field.show_report()

try:
    r = Rule('test')
except TypeError:
    print('Cannot instantiate abstract class')
