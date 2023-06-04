import glob
import json
import click
import os
from slack_dump_splitter.utils import (
    group_files_by_month,
    group_files_by_n_days,
    open_json_files_list,
    concatenate_json,
)


def main(input_dir, output_dir, mode="monthly", n_days=None):
    # List JSON files in directory
    files = glob.glob(os.path.join(input_dir, "*.json"))
    click.echo(f"Found {len(files)} files.")

    # Split filenames into different groups based on mode
    if mode == "monthly":
        grouped_files = group_files_by_month(files)
        output_basename = "slack-dump-month-"
    elif mode == "n_days":
        grouped_files = group_files_by_n_days(files, n_days)
        output_basename = "slack-dump-group-"

    # Confirm with user
    click.echo(
        f"Concatenated into {len(grouped_files)} new JSON files using {mode} mode."
    )
    if not click.confirm("Do you want to save these to disk?"):
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load each group, concatenate to signle JSON body, write to output dir
    for idx, file_group in enumerate(grouped_files):
        json_vals = open_json_files_list(file_group)
        json_concatenated = concatenate_json(json_vals)
        path = os.path.join(output_dir, output_basename + f"{idx}")
        with open(path, "+w") as file:
            json.dump(json_concatenated, file)
            click.echo(f"Concatenated JSON written to {path}")


@click.command()
@click.option(
    "-m",
    "--group-mode",
    default="monthly",
    type=click.Choice(["monthly", "n_days"]),
    prompt="What type of grouping mode do you wish to use?",
    help="Method to use when grouping JSON files together. 'monthly' will concatenate all files generated in the same calendar month together, while 'n_days' will group a pre-determined number (-n/--n-days) of json files together, regadless of the date.",
)
@click.option(
    "-n",
    "--n-days",
    type=click.INT,
    default=10,
    prompt="How many days' worth of slack messages should be grouped per JSON file? (Ignored if using 'monthly' group mode)",
    help="If -m/--group-mode is set to 'n_days', this parameter controls how many days' worth of JSON files are concatenated together.",
)
@click.argument("input_dir", type=click.Path(exists=True))
@click.argument("output_dir", type=click.Path())
def cli(input_dir, output_dir, group_mode, n_days):
    """Scans a INPUT_DIR for daily JSON-formatted slack message archives, as dumped by
    the slackdump tool, and concatenates into a smaller number of files saved to
    OUTPUT_DIR."""
    main(
        input_dir=input_dir,
        output_dir=output_dir,
        mode=group_mode,
        n_days=n_days,
    )


if __name__ == "__main__":
    print("Hello world: __main__")
