from typing import List

from core.model.domain.script import Script


def make_merged_script(scripts: Script) -> str:
    records = scripts.scripts
    return "".join(f"{record.speaker}: {record.text}\n" for record in records)
