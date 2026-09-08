from typing import List, Optional

from src.models.academic_term import AcademicTerm


class AcademicTermView:
    """Presentation helpers for academic terms."""

    @staticmethod
    def format_term(term: AcademicTerm) -> str:
        """Return a readable representation of one term."""

        current = " [CURRENT]" if term.is_current else ""

        return (
            f"{term.term_name} {term.academic_year}"
            f" | {term.start_date.isoformat()}"
            f" to {term.end_date.isoformat()}"
            f"{current}"
        )

    @staticmethod
    def format_term_list(
        terms: List[AcademicTerm],
    ) -> str:
        """Return a formatted list of academic terms."""

        if not terms:
            return "No academic terms found."

        lines = [
            AcademicTermView.format_term(term)
            for term in terms
        ]

        return "\n".join(lines)

    @staticmethod
    def format_current_term(
        term: Optional[AcademicTerm],
    ) -> str:
        """Return a formatted current-term message."""

        if term is None:
            return "No current academic term is set."

        return (
            f"Current Academic Term: "
            f"{term.term_name} {term.academic_year}"
        )
