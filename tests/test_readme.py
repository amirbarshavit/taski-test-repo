"""
Tests for the README update feature (RND-1).

These tests verify that the README.md has been properly updated from its
boilerplate/placeholder state to meaningful, project-specific content.

Run with:
    pip install pytest
    pytest tests/test_readme.py -v
"""

import re
from pathlib import Path

README_PATH = Path(__file__).parent.parent / "README.md"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def readme_text() -> str:
    """Return the full README content as a string."""
    return README_PATH.read_text(encoding="utf-8")


def readme_lines() -> list[str]:
    """Return the README as a list of stripped lines."""
    return [line.strip() for line in readme_text().splitlines()]


def readme_headings() -> list[str]:
    """Return all Markdown headings (lines starting with #) in the README."""
    return [line for line in readme_lines() if line.startswith("#")]


# ---------------------------------------------------------------------------
# Existence
# ---------------------------------------------------------------------------


class TestReadmeExists:
    def test_readme_file_exists(self):
        """The README.md file must be present in the project root."""
        assert README_PATH.exists(), "README.md not found at project root"

    def test_readme_is_not_empty(self):
        """README.md must contain at least some content."""
        assert len(readme_text().strip()) > 0, "README.md is empty"


# ---------------------------------------------------------------------------
# Title
# ---------------------------------------------------------------------------


class TestReadmeTitle:
    def test_has_h1_title(self):
        """README must start with an H1 heading."""
        lines = readme_lines()
        assert lines[0].startswith("# "), "First line must be an H1 heading"

    def test_title_is_not_placeholder(self):
        """Title must not be the generic placeholder 'test'."""
        lines = readme_lines()
        title = lines[0].lstrip("# ").strip()
        assert title.lower() != "test", (
            f"README title is still the placeholder value '{title}'. "
            "Update it to the real project name."
        )

    def test_title_is_not_empty(self):
        """Title must not be blank after the # marker."""
        lines = readme_lines()
        title = lines[0].lstrip("# ").strip()
        assert title != "", "README H1 title is blank"


# ---------------------------------------------------------------------------
# Description
# ---------------------------------------------------------------------------


class TestReadmeDescription:
    def test_has_description(self):
        """README must include a project description paragraph."""
        text = readme_text()
        assert len(text.strip()) > 50, "README seems too short to have a real description"

    def test_description_is_not_placeholder(self):
        """Description must not be the default boilerplate sentence."""
        placeholder = "A short description of what this project does and the problem it solves."
        assert placeholder not in readme_text(), (
            "README description is still the placeholder text. "
            "Replace it with an actual project description."
        )

    def test_description_mentions_project_purpose(self):
        """README description should be at least a sentence long (> 20 chars) after the title."""
        lines = readme_lines()
        # Find the first non-empty, non-heading line
        description_lines = [
            l for l in lines[1:] if l and not l.startswith("#")
        ]
        assert description_lines, "No description text found after the title"
        assert len(description_lines[0]) > 20, (
            "Description seems too short to convey project purpose"
        )


# ---------------------------------------------------------------------------
# Required Sections
# ---------------------------------------------------------------------------


REQUIRED_SECTIONS = ["Installation", "Usage"]


class TestRequiredSections:
    def test_has_installation_section(self):
        """README must have an Installation section."""
        headings_text = " ".join(readme_headings())
        assert "Installation" in headings_text, (
            "README is missing an 'Installation' section"
        )

    def test_has_usage_section(self):
        """README must have a Usage section."""
        headings_text = " ".join(readme_headings())
        assert "Usage" in headings_text, (
            "README is missing a 'Usage' section"
        )

    def test_has_at_least_three_sections(self):
        """A well-structured README should have at least 3 sections (H1 + 2 others)."""
        headings = readme_headings()
        assert len(headings) >= 3, (
            f"README only has {len(headings)} heading(s). "
            "A complete README typically has Installation, Usage, and more."
        )


# ---------------------------------------------------------------------------
# No Placeholder URLs / Content
# ---------------------------------------------------------------------------


class TestNoPlaceholderContent:
    def test_no_placeholder_github_url(self):
        """README must not contain the generic placeholder GitHub URL."""
        assert "your-username" not in readme_text(), (
            "README still contains placeholder GitHub URL 'your-username'. "
            "Replace it with the real repository URL."
        )

    def test_no_placeholder_repo_name_in_clone_url(self):
        """Clone URL must not still point to a repo literally named 'test'."""
        # Match 'git clone https://github.com/<anything>/test.git'
        pattern = r"git clone https://github\.com/[^/]+/test\.git"
        assert not re.search(pattern, readme_text()), (
            "README clone URL still uses the placeholder repository name 'test'. "
            "Update it to the real repository name."
        )

    def test_no_update_this_command_comment(self):
        """README must not contain the boilerplate 'update this command' comment."""
        assert "update this command to match your stack" not in readme_text().lower(), (
            "README still contains the boilerplate comment about updating the stack command."
        )


# ---------------------------------------------------------------------------
# Code Blocks / Commands
# ---------------------------------------------------------------------------


class TestCodeBlocks:
    def test_has_at_least_one_code_block(self):
        """README should contain at least one fenced code block."""
        assert "```" in readme_text(), (
            "README contains no fenced code blocks. "
            "Add code examples for installation and usage."
        )

    def test_code_blocks_are_closed(self):
        """Every opened code block must be closed."""
        fence_count = readme_text().count("```")
        assert fence_count % 2 == 0, (
            f"README has an odd number of ``` markers ({fence_count}), "
            "meaning at least one code block is not properly closed."
        )

    def test_installation_section_has_command(self):
        """The Installation section should include at least one shell command."""
        text = readme_text()
        # Find content between Installation and the next heading
        match = re.search(
            r"## Installation\s+(.*?)(?=\n##|\Z)", text, re.DOTALL
        )
        assert match, "Could not locate Installation section content"
        section_content = match.group(1)
        assert "```" in section_content, (
            "Installation section has no code block with commands"
        )

    def test_usage_section_has_command(self):
        """The Usage section should include at least one runnable command."""
        text = readme_text()
        match = re.search(
            r"## Usage\s+(.*?)(?=\n##|\Z)", text, re.DOTALL
        )
        assert match, "Could not locate Usage section content"
        section_content = match.group(1)
        assert "```" in section_content, (
            "Usage section has no code block with commands"
        )


# ---------------------------------------------------------------------------
# Overall Quality
# ---------------------------------------------------------------------------


class TestReadmeQuality:
    def test_minimum_length(self):
        """README should be substantive — at least 200 characters."""
        assert len(readme_text()) >= 200, (
            f"README is only {len(readme_text())} characters. "
            "A useful README should be more detailed."
        )

    def test_no_lorem_ipsum(self):
        """README must not contain 'lorem ipsum' placeholder text."""
        assert "lorem ipsum" not in readme_text().lower(), (
            "README contains 'lorem ipsum' placeholder text."
        )

    def test_no_todo_placeholders(self):
        """README must not contain unfilled TODO markers."""
        assert "TODO" not in readme_text(), (
            "README still contains TODO placeholders. Fill them in."
        )

    def test_no_fixme_placeholders(self):
        """README must not contain FIXME markers."""
        assert "FIXME" not in readme_text(), (
            "README still contains FIXME placeholders."
        )


# ---------------------------------------------------------------------------
# Messi Section (RND-1)
# ---------------------------------------------------------------------------


def readme_messi_section() -> str:
    """Return the content of the Messi section, or an empty string if absent."""
    text = readme_text()
    match = re.search(
        r"##\s+.*[Mm]essi.*\n(.*?)(?=\n##|\Z)", text, re.DOTALL
    )
    return match.group(1).strip() if match else ""


class TestMessiSection:
    def test_readme_mentions_messi(self):
        """README must mention Messi somewhere in its content."""
        assert "Messi" in readme_text() or "messi" in readme_text().lower(), (
            "README does not mention Messi at all. "
            "Add a section or passage about Messi (RND-1)."
        )

    def test_has_messi_heading(self):
        """README must contain a heading dedicated to Messi."""
        headings = readme_headings()
        messi_headings = [h for h in headings if "messi" in h.lower()]
        assert messi_headings, (
            "README has no heading that references Messi. "
            "Add a '## Messi' (or similar) section."
        )

    def test_messi_section_is_not_empty(self):
        """The Messi section must have body content, not just a heading."""
        content = readme_messi_section()
        assert content, (
            "The Messi section exists but has no body text. "
            "Write something substantive about Messi."
        )

    def test_messi_section_minimum_length(self):
        """The Messi section should be at least 50 characters of real content."""
        content = readme_messi_section()
        assert len(content) >= 50, (
            f"The Messi section is only {len(content)} character(s) long. "
            "Write at least a short paragraph about Messi."
        )

    def test_messi_section_not_placeholder(self):
        """The Messi section must not contain generic placeholder text."""
        content = readme_messi_section().lower()
        placeholders = ["lorem ipsum", "todo", "fixme", "write something here", "tbd"]
        for placeholder in placeholders:
            assert placeholder not in content, (
                f"The Messi section still contains placeholder text: '{placeholder}'. "
                "Replace it with real content."
            )

    def test_messi_section_mentions_messi_by_name(self):
        """The Messi section body should refer to Messi by name (not just the heading)."""
        content = readme_messi_section()
        assert "messi" in content.lower() or "lionel" in content.lower(), (
            "The Messi section body does not mention 'Messi' or 'Lionel' by name. "
            "The content should reference him explicitly."
        )

    def test_messi_section_contains_real_fact(self):
        """The Messi section should reference at least one real, specific fact about Messi.

        Accepted keywords: goals, Argentina, Ballon d'Or / ballon, World Cup / worldcup,
        Barcelona, Inter Miami / miami, champion, record, trophy, award.
        """
        content = readme_messi_section().lower()
        fact_keywords = [
            "goal", "argentina", "ballon", "world cup", "worldcup",
            "barcelona", "miami", "champion", "record", "trophy", "award",
        ]
        matched = [kw for kw in fact_keywords if kw in content]
        assert matched, (
            "The Messi section doesn't appear to contain any recognisable facts about Messi. "
            "Mention at least one of: goals, Argentina, Ballon d'Or, World Cup, "
            "Barcelona, Inter Miami, championships, records, trophies, or awards."
        )
