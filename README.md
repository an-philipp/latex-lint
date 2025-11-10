# latex-lint
Lint your latex files and check them for predefined rules.
Right now these rudimentary rules are implemented:

1. `\cite{}` without a preceding protected white space
2. `\ref{}` without preceding protected whitespace
3. Using labels for chapters that differ from the following form: `chapter::<lowercase chaptername>::<lowercase section>`

If one of these conditions fails, the script returns a non-zero exit code.
