from setuptools import setup

extras = {
    "test": ["pytest>=6.0"],
}
extras["complete"] = sum(extras.values(), [])


setup(
    entry_points={"intake.drivers": ["awkward_json = intake_awkward.json:JSONSource"]},
    extras_require=extras,
)
