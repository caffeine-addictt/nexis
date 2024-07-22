# Code Style

The following is a general guide on how to style your work so that the project
remains consistent throughout all files. Please read this document in it's entirety
and refer to it throughout the development of your contribution.

1. [General Guidelines](#general-guidelines)
2. [Markdown Guidelines](#markdown-guidelines)

## General Guidelines

Listed is a example class used demonstrate general rules you should follow
throughout the development of your contribution.
Please ensure that your code passes linting before merging a Pull Request.

> [!NOTE] Nexis uses [editor-config](https://editorconfig.org)
> Please ensure that your editor uses the same settings as the project.

### Golang

- Docstrings are to follow _Replace this with what style Docstrings should follow_.
- Private attributes are to be prefixed with an underscore.

```go
// This is documentation for the following function
// I can also make it multiline
func MyFunc() {}

// And also can document just about anything
package test
```

### Python

- Docstrings are to follow reST (reStructuredText Docstring Format)
  as specified in [PEP 287](https://peps.python.org/pep-0287/)
- Private attributes are to be prefixed with an underscore
- Use of [typing](https://docs.python.org/3/library/typing.html) type hints

```python
class ExampleClass:
    """
    ExampleClass
    ------------
    Example class for CODESTYLE.md
    """
    # ^^^ reST Docstring Format

    _private_attribute : int # private attributes begin with a lowercase
    public_attribute   : int # type hint for integer is defined here

    def __init__(
        self,
        public_attribute: int # type hint for parameters
    ) -> None: # the expected return value of method
        """
        Initializes a ExampleClass

        Parameters
        ----------
        :param public_attribute: example attribute
        """
        self.public_attribute = public_attribute
        self.private_attribute = square(public_attribute)

    def square(self, value: int) -> int:
        """
        Example method that square roots a value

        Parameters
        ----------
        :param value: value that you want squared
        """
        return value**2
```

## Markdown Guidelines

Currently, documentation for this project resides in markdown files.

- Use of HTML is permitted
- Use of HTML comments is appreciated
- Exceedingly long lines are to be broken
- [reference style links][reference-style-links] are not required by are appreciated

```markdown
<!--example markdown document-->

# Section

Lorem ipsum dolor sit amet, consectetur adipiscing elit,
sed do eiusmod tempor incididunt ut labore et dolore
magna aliqua. Ut enim ad minim veniam, quis nostrud
exercitation ullamco laboris nisi ut aliquip ex ea
commodo consequat. Duis aute irure dolor in
reprehenderit in voluptate velit esse cillum dolore eu
fugiat nulla pariatur. Excepteur sint occaecat cupidatat
non proident, sunt in culpa qui officia deserunt mollit
anim id est laborum. found [Lorem Ipsum Generator]

# Section 2

<ul>
  <li> Apple
  <li> Orange
  <li> Pineapple
</ul>

[Lorem Ipsum Generator]: https://loremipsum.io/generator/
```

[reference-style-links]: https://www.markdownguide.org/basic-syntax/#reference-style-links
