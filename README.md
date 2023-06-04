# Slack Dump Splitter

Concatenates the conversation dump output of the [slackdump](https://github.com/rusq/slackdump) tool into a smaller number of JSON files for easier importing into Discord via [Slackord](https://github.com/thomasloupe/Slackord).


## Installing
```
pip install .
```

This will register a console script as `slack-dump-splitter`

## Running
See below for help output:
```
Usage: slack-dump-splitter [OPTIONS] INPUT_DIR OUTPUT_DIR

  Scans a INPUT_DIR for daily JSON-formatted slack message archives, as dumped
  by the slackdump tool, and concatenates into a smaller number of files saved
  to OUTPUT_DIR.

Options:
  -m, --group-mode [monthly|n_days]
                                  Method to use when grouping JSON files
                                  together. 'monthly' will concatenate all
                                  files generated in the same calendar month
                                  together, while 'n_days' will group a pre-
                                  determined number (-n/--n-days) of json
                                  files together, regadless of the date.
  -n, --n-days INTEGER            If -m/--group-mode is set to 'n_days', this
                                  parameter controls how many days' worth of
                                  JSON files are concatenated together.
  --help                          Show this message and exit.
```