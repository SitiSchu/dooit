from typing import Dict, List
from rich.align import Align
from rich.console import Group, RenderableType
from rich.style import Style, StyleType
from rich.table import Table
from rich.text import Text

from dooit.utils.enums import Keybinds
from dooit.utils.keybinder import KeyBinder


# UTILS
# ---------------------------------------------------
NL = Text("\n")
kb = KeyBinder()


def colored(text: str, color: StyleType) -> str:
    return f"[{color}]{text}[/]"


def convert_to_row(bindings: Dict):
    arr = []
    methods = kb.raw

    for i, j in bindings.items():
        if i in methods:
            key = methods[i]
            if isinstance(key, list):
                key = "/".join(key)

            arr.append(
                [
                    Text.from_markup(
                        colored(
                            " or ",
                            "i cyan",
                        ).join(methods[i]),
                        style="b green",
                    ),
                    Text(i, style="magenta"),
                    Text.from_markup(j, style="b blue"),
                ]
            )
        else:
            arr.append(
                [
                    Text(i, style="b green"),
                    Text("N/A", style="d white", justify="center"),
                    Text.from_markup(j, style="b blue"),
                ]
            )

    return arr


def generate_kb_table(
    kb: Dict[str, str], topic: str, notes: List[str] = []
) -> RenderableType:
    """
    Generate Table for modes
    """

    arr = convert_to_row(kb)

    table = Table.grid(expand=True, padding=(0, 3))
    table.add_column("mode", width=20)
    table.add_column("keybind", width=15)
    table.add_column("cmd", width=20)
    table.add_column("colon", width=2)
    table.add_column("help", width=50)

    table.add_row(Text.from_markup(f" [r green] {topic} [/r green]"), "", "", "")

    for i in arr:
        table.add_row("", i[0], i[1], Text("->", style="d white"), i[2])

    if notes:
        notes = [f"{colored('!', 'd yellow')} {i}" for i in notes]
        notes = [colored(" Note:", "d white")] + notes

    return Align.center(
        Group(table, *[Text.from_markup(i) for i in notes], NL, separator, NL)
    )


separator = Text.from_markup(f"{colored('─' * 60, 'b d black')}", justify="center")

# ---------------- X -------------------------


# KEYBINDINGS
# --------------------------------------------
NORMAL_KB = {
    Keybinds.MOVE_DOWN: "Move down in list",
    Keybinds.SHIFT_DOWN: "Shift todo down in list",
    Keybinds.MOVE_UP: "Move up in list",
    Keybinds.SHIFT_UP: "Shift todo up in list",
    Keybinds.TOGGLE_COMPLETE: "Toggle todo status as complete/incomplete**",
    Keybinds.COPY_TEXT: "Copy (todo/workspace)'s text",
    Keybinds.YANK: "Copy a whole todo/workspace",
    Keybinds.PASTE: "Paste the yanked todo/workspace",
    Keybinds.MOVE_TO_TOP: "Move to top of list",
    Keybinds.MOVE_TO_BOTTOM: "Move to bottom of list",
    Keybinds.TOGGLE_EXPAND: "Toggle-expand highlighted item",
    Keybinds.TOGGLE_EXPAND_RECURSIVE: "Toggle-expand highlighted item and all it's children",
    Keybinds.TOGGLE_EXPAND_PARENT: "Toggle-expand parent item",
    Keybinds.REMOVE_ITEM: "Remove highlighted node",
    Keybinds.ADD_SIBLING: "Add sibling todo/workspace",
    Keybinds.ADD_CHILD: "Add child todo/workspace",
    Keybinds.SORT_MENU_TOGGLE: "Launch sort menu",
    Keybinds.START_SEARCH: "Start Search Mode",
    Keybinds.SWITCH_PANE: "Toggle focused pane",
    Keybinds.SWITCH_PANE_WORKSPACE: "Change focus to workspace",
    Keybinds.SWITCH_PANE_TODO: "Change focus to todo",
    Keybinds.EDIT_DUE: "Edit date**",
    Keybinds.EDIT_DESCRIPTION: "Edit description**",
    Keybinds.EDIT_EFFORT: "Edit effort for todo**",
    Keybinds.EDIT_RECURRENCE: "Edit recurrence for todo**",
    Keybinds.SWITCH_DATE_STYLE: "Increase urgency**",
    Keybinds.INCREASE_URGENCY: "Decrease urgency**",
    Keybinds.DECREASE_URGENCY: "switch due from date or time remaining ",
}

NORMAL_NB = [
    f"{colored('*  - In Menu Only', 'grey50')}",
    f"{colored('** - In Todo List Only', 'grey50')}",
]

INSERT_KB = {
    "escape": "Go back to NORMAL mode",
    "enter": "Continue adding more todos",
    "any": "Push key in the selected item",
}

DATE_KB = {
    "escape": "Go back to normal mode",
    "any": "Enter the key in the focused area",
}

DATE_NB = [
    colored("Only digits and hyphen allowed format:", "grey50")
    + (colored("dd-mm-yyyy", "yellow"))
]

SEARCH_KB = {
    "escape": "Navigate in the searched items"
    + "\n"
    + "Goes back to normal mode [i u]if navigating[/i u]",
    "start search": "Go back to search input [i u]if navigating[/i u]",
    "any": "Press key to search input",
}

SORT_KB = {
    "move down": "Move to next sort option",
    "move up": "Move to previous sort option",
    "sort menu toggle": "Cancel sort operation",
    "enter": "Select the sorting method",
}
# ---------------- X -------------------------


# TEXT CONSTS
# --------------------------------------------
HEADER = f"""
{colored("Welcome to the help menu!", 'yellow')}
{separator.markup}
"""

BODY = f"""{colored('Dooit is built to be used from the keyboard!', 'green')}

Documentation below will walk you through the controls:
{separator.markup}
"""

THANKS = f"{colored('Thanks for using dooit :heart:', 'yellow')}"
SPONSOR_URL = "https://github.com/sponsors/kraanzu"
SPONSOR1 = f"{colored('You can also sponsor this project on github!', 'yellow')}"
SPONSOR2 = Text(
    "Github Sponsor",
    style=Style.from_meta({"@click": f"app.open_url('{SPONSOR_URL}')"}),
    justify="center",
)
AUTHOR = f"{colored('--kraanzu', 'orchid')}{NL.plain * 2}{separator.markup}{NL}"

OUTRO = (
    f"Press {colored('escape', 'green')} or {colored('?', 'green')} to exit help menu"
)

# ---------------- X -------------------------


class HelpMenu:
    """
    A Help Menu Widget
    """

    header = Text.from_markup(HEADER, justify="center")
    body = Text.from_markup(BODY, justify="center")
    thanks = Text.from_markup(THANKS, justify="center")
    author = Text.from_markup(AUTHOR, justify="center")
    outro = Text.from_markup(OUTRO, justify="center")
    sponsor = Text.from_markup(SPONSOR1, justify="center")

    def items(self) -> List[RenderableType]:
        arr = []
        arr.append(self.header)
        arr.append(self.body)
        arr.append(generate_kb_table(NORMAL_KB, "NORMAL", NORMAL_NB))
        arr.append(generate_kb_table(INSERT_KB, "INSERT"))
        arr.append(generate_kb_table(DATE_KB, "DATE", DATE_NB))
        arr.append(generate_kb_table(SEARCH_KB, "SEARCH"))
        arr.append(generate_kb_table(SORT_KB, "SORT"))
        arr.append(self.thanks)
        arr.append(self.sponsor)
        arr.append(SPONSOR2)
        arr.append(self.author)
        arr.append(self.outro)

        return arr
