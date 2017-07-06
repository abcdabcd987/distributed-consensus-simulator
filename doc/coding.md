# Coding Guide

The project is written in Python3. For clearance, I have added type hints to all functions.
It is recommended for you to write type hints for your code. See
[PEP484](https://www.python.org/dev/peps/pep-0484/) and
[`typing` module](https://docs.python.org/3/library/typing.html)
for more details.

It is recommended to use [PyCharm](https://www.jetbrains.com/pycharm/download/)
to develop this project, since the IDE can make use of
the type hints, giving good autocomplete suggestions and performing all kinds of checking.
Don't be bothered with the license issue. You can have access to all JetBrain product for free
using your school email. If you haven't, apply [here](https://www.jetbrains.com/student/).

Everybody is supposed to develop on his or her own branch or fork. The master branch is
protected, so you cannot push your code to it. If you are not familiar with git branching,
you can look into some tutorials or ask someone for help.

To run the simulation, just type the following in the console:

    python3 -m dcsim.sleepy

It will of course complains about the `NotImplementedError` for now. So let's get our hands
dirty and do your job. I'll merge your codes later.

You can refer to [the design document](design.py). It may be out-of-sync with the project itself,
but hopefully you can get the ideas. You can also refer to the interfaces provided by the
`framework` package.

- **All `raise NotImplementedError` should be replaced with your code.**
- For the framework group, you need to implement the `framework` package.
- For the honest group and the adversary group, everything you need is inside the `sleepy` package.
  You can also add some common utilities into that package.
- For the integrator group, you need to come up with the formal statement of the simulator's
  assumptions. After the coding phase is finished, you need to add
  [docstring](https://www.python.org/dev/peps/pep-0257/) to the codebase.
- **If you have any questions, please ask in the group chat. We can all have a discussion and
  finally reach a consensus :-)**
