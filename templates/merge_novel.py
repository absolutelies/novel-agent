#!/usr/bin/env python3
"""
Novel Chapter Merger Script (Chinese-Only)
==========================================
Merges Chinese chapter files into complete novel file.

Features:
- Merges Chinese chapters → novel_full_zh.md
- Proper title header formatting
- Correct chapter separators (---)
- Handles chapter first lines properly
- Maintains proper line breaks between chapters

NOTE: English merge logic removed - simplified workflow generates Chinese directly.
"""

import os
import re
import glob
from pathlib import Path
from typing import List, Tuple


class NovelMerger:
    """Merges Chinese chapter files into complete novel files."""

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        # base_path should point to the project root (contains output folder)
        self.output_final = self.base_path / "output" / "final"
        self.output_zh = self.output_final / "zh-CN"

    def get_chapter_files(self) -> List[Path]:
        """
        Get sorted list of Chinese chapter files.

        Returns:
            Sorted list of chapter file paths
        """
        pattern = str(self.output_zh / "chapter_*.md")
        files = glob.glob(pattern)

        # Sort by chapter number
        def extract_number(filepath: str) -> int:
            match = re.search(r"chapter_(\d+)", filepath)
            return int(match.group(1)) if match else 0

        return sorted([Path(f) for f in files], key=lambda x: extract_number(str(x)))

    def read_chapter(self, filepath: Path) -> str:
        """
        Read chapter content, stripping trailing whitespace.

        Args:
            filepath: Path to chapter file

        Returns:
            Chapter content string
        """
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Strip trailing whitespace but preserve internal formatting
        content = content.rstrip()

        return content

    def get_novel_title(self) -> str:
        """
        Get novel title header (placeholder - should be customized per project).

        Returns:
            Title header string
        """
        return "# 小说标题\n\n小说\n\n---\n\n"

    def merge_chapters(self) -> Tuple[str, int]:
        """
        Merge all chapters into a single novel string.

        Returns:
            Tuple of (merged content, actual chapter count)
        """
        files = self.get_chapter_files()
        print(f"Found {len(files)} chapter files")

        # Start with title header
        merged = self.get_novel_title()

        # Merge each chapter
        for i, filepath in enumerate(files, 1):
            print(f"  Processing chapter {i}: {filepath.name}")
            chapter_content = self.read_chapter(filepath)

            # Check for chapter heading
            if not re.search(r"第\d+章\s", chapter_content):
                print(
                    f"  WARNING: Chapter file {filepath.name} has no heading"
                )

            # Normalize: strip markdown heading prefix from chapter heading
            chapter_content = re.sub(
                r"^# (第\d+章)", r"\1", chapter_content, count=1, flags=re.MULTILINE
            )

            # Add chapter content
            merged += chapter_content

            # Add separator after each chapter (except the last)
            if i < len(files):
                merged += "\n\n---\n\n"
            else:
                # Last chapter ends with just newline
                merged += "\n"

        return merged, len(files)

    def _count_headings(self, content: str) -> int:
        """
        Count number of chapter headings (第N章) in content.

        Args:
            content: Text content to scan

        Returns:
            Number of chapter heading matches
        """
        return len(re.findall(r"^第\d+章\s", content, flags=re.MULTILINE))

    def validate_headings(
        self, content: str, expected_count: int
    ) -> Tuple[bool, str]:
        """
        Validate that heading count matches expected chapter count.

        Args:
            content: Merged novel content
            expected_count: Number of chapter files that were merged

        Returns:
            Tuple of (is_valid, message)
        """
        actual = self._count_headings(content)

        if actual == expected_count:
            return (True, f"PASS: All {expected_count} chapter headings found")

        # Find which chapter numbers are missing
        existing = set(re.findall(r"^第(\d+)章\s", content, flags=re.MULTILINE))
        expected = set(str(i) for i in range(1, expected_count + 1))
        missing = expected - existing

        if missing:
            sorted_missing = sorted(missing, key=int)
            missing_str = ", ".join(sorted_missing)
            return (
                False,
                f"FAIL: Found {actual} heading(s), expected {expected_count}. "
                f"Missing chapter(s): {missing_str}",
            )
        else:
            # Same count but different numbers (duplicates/overlaps)
            extra = existing - expected
            extra_str = ", ".join(sorted(extra, key=int)) if extra else "none"
            return (
                False,
                f"FAIL: Found {actual} heading(s), expected {expected_count}. "
                f"Extra chapter(s): {extra_str}",
            )

    def write_novel(self, content: str) -> Path:
        """
        Write merged novel to file.

        Args:
            content: Merged novel content

        Returns:
            Path to output file
        """
        output_path = self.output_zh / "novel_full_zh.md"

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        return output_path

    def get_stats(self, filepath: Path) -> dict:
        """
        Get statistics for a novel file.

        Args:
            filepath: Path to novel file

        Returns:
            Dictionary with word count, line count, etc.
        """
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        lines = content.split("\n")

        # Chinese: count characters (excluding spaces/newlines)
        char_count = len(re.sub(r"[\s\n]", "", content))

        # Count chapter headings
        heading_count = self._count_headings(content)

        return {
            "char_count": char_count,
            "line_count": len(lines),
            "total_chars": len(content),
            "file_size": filepath.stat().st_size if filepath.exists() else 0,
            "heading_count": heading_count,
        }

    def run(self) -> dict:
        """
        Run the full merge process.

        Returns:
            Dictionary with merge results and statistics
        """
        results = {}

        # Merge Chinese
        print("Merging Chinese chapters...")
        zh_content, zh_count = self.merge_chapters()

        # Validate headings before writing
        is_valid, validation_msg = self.validate_headings(zh_content, zh_count)
        print(f"  {validation_msg}")
        if not is_valid:
            print("ERROR: Heading count mismatch — aborting merge")
            exit(1)

        zh_path = self.write_novel(zh_content)
        zh_stats = self.get_stats(zh_path)

        results["chinese"] = {
            "path": str(zh_path),
            "chapter_count": zh_count,
            "char_count": zh_stats["char_count"],
            "line_count": zh_stats["line_count"],
            "file_size": zh_stats["file_size"],
            "heading_count": zh_stats["heading_count"],
        }

        print(
            f"Chinese novel: {zh_count} chapters, {zh_stats['char_count']} characters, "
            f"{zh_stats['heading_count']} headings"
        )
        print(f"Output: {zh_path}")

        return results


def main():
    """Main entry point."""
    # base_path should be the project root
    base_path = Path(__file__).parent.parent

    # Verify output directory exists
    if not (base_path / "output" / "final" / "zh-CN").exists():
        print(f"Error: Cannot find output/final/zh-CN directory")
        print(f"Checked: {base_path / 'output' / 'final' / 'zh-CN'}")
        return 1

    print(f"Project: {base_path.name}")
    print(f"Base path: {base_path}")

    # Create merger and run
    merger = NovelMerger(str(base_path))
    results = merger.run()

    # Print summary
    print("\n" + "=" * 50)
    print("MERGE COMPLETE")
    print("=" * 50)
    print(f"Chinese: {results['chinese']['chapter_count']} chapters")
    print(f"         {results['chinese']['char_count']} characters")
    print(f"         {results['chinese']['line_count']} lines")
    print(f"         {results['chinese']['heading_count']} headings")
    print(f"         {results['chinese']['file_size']} bytes")
    print("=" * 50)

    return 0


if __name__ == "__main__":
    exit(main())
