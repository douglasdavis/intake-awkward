from setuptools import setup

setup(
    entry_points={"intake.drivers": ["awkward_json = intake_awkward.json:JSONSource"]}
)
