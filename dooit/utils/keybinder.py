from collections import defaultdict
from typing import DefaultDict, Dict, List, Optional, Union
from dooit.utils.conf_reader import config_man
from copy import deepcopy

from dooit.utils.enums import Keybinds

customed_keys = config_man.get("keybindings")


class Bind:
    exclude_cursor_check = [
        "add_sibling",
        "change_status",
        "move_down",
        "move_up",
        "switch_pane",
        "spawn_help",
        "switch_pane_workspace",
        "start_search",
        "stop_search",
    ]

    def __init__(self, func_name: str, params: List[str]) -> None:
        self.func_name = func_name
        self.params = params
        self.check_for_cursor = func_name not in self.exclude_cursor_check


KeyList = Dict[str, Union[str, List]]
PRINTABLE = (
    "0123456789"
    + "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    + "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ "
)
DEFAULTS = {
    Keybinds.SWITCH_PANE: "<tab>",
    Keybinds.MOVE_UP: ["k", "<up>"],
    Keybinds.SHIFT_UP: ["K", "<shift+up>"],
    Keybinds.MOVE_DOWN: ["j", "<down>"],
    Keybinds.SHIFT_DOWN: ["J", "<shift+down>"],
    Keybinds.EDIT_DESCRIPTION: "i",
    Keybinds.TOGGLE_EXPAND: "z",
    Keybinds.TOGGLE_EXPAND_RECURSIVE: "<ctrl+z>",
    Keybinds.TOGGLE_EXPAND_PARENT: "Z",
    Keybinds.ADD_CHILD: "A",
    Keybinds.ADD_SIBLING: "a",
    Keybinds.REMOVE_ITEM: "x",
    Keybinds.MOVE_TO_TOP: ["g", "<home>"],
    Keybinds.MOVE_TO_BOTTOM: ["G", "<end>"],
    Keybinds.SORT_MENU_TOGGLE: "s",
    Keybinds.START_SEARCH: "/",
    Keybinds.SPAWN_HELP: "?",
    Keybinds.COPY_TEXT: "Y",
    Keybinds.YANK: "y",
    Keybinds.PASTE: "p",
    Keybinds.TOGGLE_COMPLETE: "c",
    Keybinds.EDIT_DUE: "d",
    Keybinds.SWITCH_DATE_STYLE: "D",
    Keybinds.EDIT_RECURRENCE: "r",
    Keybinds.INCREASE_URGENCY: ["+", "="],
    Keybinds.DECREASE_URGENCY: ["-", "_"],
    Keybinds.SWITCH_PANE_WORKSPACE: ["h"],
    Keybinds.SWITCH_PANE_TODO: ["l"],
}

configured_keys = deepcopy(DEFAULTS)
configured_keys.update(customed_keys)


class KeyBinder:
    # KEYBIND MANAGER FOR NORMAL MODE

    def __init__(self) -> None:
        self.pressed = ""
        self.methods: Dict[str, Bind] = {}
        self.raw: DefaultDict[str, List[str]] = defaultdict(list)
        self.add_keys(configured_keys)

    def convert_to_bind(self, cmd: str) -> Bind:
        func_split = cmd.split()
        if func_split[0] == "edit":
            return Bind("start_edit", [func_split[1]])
        else:
            return Bind("_".join(func_split), [])

    def add_keys(self, keys: KeyList) -> None:
        for cmd, key in keys.items():
            if isinstance(key, str):
                key = [key]

            for k in key:
                if k not in self.raw[cmd]:
                    self.raw[cmd].append(k)

                self.methods[k] = self.convert_to_bind(cmd)

    def attach_key(self, key: str) -> None:
        if key == "escape" and self.pressed:
            return self.clear()

        if len(key) > 1:
            key = f"<{key}>"

        self.pressed += key

    def clear(self) -> None:
        self.pressed = ""

    def find_keys(self) -> List[str]:
        possible_bindings = filter(
            lambda keybind: keybind.startswith(self.pressed),
            self.methods.keys(),
        )
        return list(possible_bindings)

    def get_method(self) -> Optional[Bind]:
        possible_keys = self.find_keys()
        if self.pressed and possible_keys:
            if len(possible_keys) == 1 and possible_keys[0] == self.pressed:
                method = self.methods.get(possible_keys[0])
                self.clear()
                return method
            else:
                return Bind("change_status", ["K PENDING"])
        else:
            self.clear()
            return Bind("change_status", ["NORMAL"])
