"""The plugin manifest and its skill share one identity, and the skill's links resolve."""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / ".claude-plugin/plugin.json"
SKILL_ROOT = REPO_ROOT / "skills/show-me"
SKILL_PATH = SKILL_ROOT / "SKILL.md"
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
RELATIVE_LINK = re.compile(r"\]\((?!https?://|#)([^)]+)\)")


def parse_frontmatter(skill_text):
    """Frontmatter fields by key; a double-quoted value is decoded as a JSON string."""
    fields = {}
    for line in FRONTMATTER.match(skill_text).group(1).splitlines():
        key, value = line.split(": ", 1)
        fields[key] = json.loads(value) if value.startswith('"') else value

    return fields


def test_manifest_lists_exactly_the_plugin_fields():
    manifest = json.loads(MANIFEST_PATH.read_text())

    assert list(manifest) == ["name", "version", "description", "author"], (
        f"plugin.json fields {list(manifest)}"
    )


def test_the_plugin_is_named_show_me():
    manifest = json.loads(MANIFEST_PATH.read_text())

    assert manifest["name"] == "show-me", f"plugin name {manifest['name']!r}"


def test_skill_frontmatter_mirrors_the_plugin_manifest():
    manifest = json.loads(MANIFEST_PATH.read_text())

    frontmatter = parse_frontmatter(SKILL_PATH.read_text())

    identity = {key: frontmatter.get(key) for key in ("name", "description")}
    expected = {"name": "show-me", "description": manifest["description"]}
    assert identity == expected, f"frontmatter {identity}, expected {expected}"


def test_the_plugin_ships_exactly_one_nested_skill():
    skills = sorted(path.relative_to(REPO_ROOT) for path in REPO_ROOT.glob("skills/*/SKILL.md"))

    assert skills == [Path("skills/show-me/SKILL.md")], f"skills found: {skills}"
    assert not (REPO_ROOT / "SKILL.md").exists(), "a root SKILL.md would ship a second skill"


def test_skill_links_resolve_inside_the_skill_directory():
    targets = RELATIVE_LINK.findall(SKILL_PATH.read_text())

    assert sorted(set(targets)) == ["references/diagram-types.md"], f"links found: {targets}"
    for target in targets:
        resolved = (SKILL_ROOT / target).resolve()
        assert resolved.is_relative_to(SKILL_ROOT.resolve()), f"{target} leaves the skill"
        assert resolved.is_file(), f"{target} does not exist"
