from os import linesep
from typing import Dict, Iterator, Sequence, Set, Tuple

from pynvim import Nvim

from .consts import fm_hl_prefix
from .nvim import call
from .types import HLgroup

LEGAL_CTERM: Set[str] = {
    "bold",
    "underline",
    "undercurl",
    "strikethrough",
    "reverse",
    "italic",
    "standout",
}

LEGAL_CTERM_COLOURS = range(8)


def gen_hl(name_prefix: str, mapping: Dict[str, str]) -> Dict[str, HLgroup]:
    def cont() -> Iterator[Tuple[str, HLgroup]]:
        for key, val in mapping.items():
            name = f"{fm_hl_prefix}_{name_prefix}_{key}"
            yield key, HLgroup(name=name, guifg=val)

    return {k: v for k, v in cont()}


async def add_hl_groups(nvim: Nvim, groups: Sequence[HLgroup]) -> None:
    def parse() -> Iterator[str]:
        for group in groups:
            name = group.name
            _cterm = ",".join(group.cterm) or "NONE"
            cterm = f"cterm={_cterm}"
            ctermfg = f"ctermfg={group.ctermfg}" if group.ctermfg else ""
            ctermbg = f"ctermbg={group.ctermbg}" if group.ctermbg else ""
            guifg = f"guifg={group.guifg}" if group.guifg else ""
            guibg = f"guibg={group.guibg}" if group.guibg else ""

            yield f"highlight {name} {cterm} {ctermfg} {ctermbg} {guifg} {guibg}"

    def cont() -> None:
        commands = linesep.join(parse())
        nvim.api.exec(commands, False)

    await call(nvim, cont)