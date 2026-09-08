from typing import List, Optional

from src.models.academic_term import AcademicTerm
from src.services.academic_term_service import AcademicTermService


class AcademicTermController:
    """Controller for academic term operations."""

    def __init__(
        self,
        service: Optional[AcademicTermService] = None,
    ) -> None:
        self.service = service or AcademicTermService()

    def create_term(
        self,
        term_name: str,
        academic_year: int,
        start_date,
        end_date,
        is_current: bool = False,
    ) -> AcademicTerm:
        """Create a new academic term."""

        return self.service.create_term(
            term_name=term_name,
            academic_year=academic_year,
            start_date=start_date,
            end_date=end_date,
            is_current=is_current,
        )

    def get_term(
        self,
        term_id: int,
    ) -> Optional[AcademicTerm]:
        """Get an academic term by ID."""

        return self.service.get_term(term_id)

    def get_all_terms(self) -> List[AcademicTerm]:
        """Get all academic terms."""

        return self.service.get_all_terms()

    def search_terms(
        self,
        query: str,
    ) -> List[AcademicTerm]:
        """Search academic terms."""

        return self.service.search_terms(query)

    def update_term(
        self,
        term: AcademicTerm,
    ) -> AcademicTerm:
        """Update an academic term."""

        return self.service.update_term(term)

    def delete_term(
        self,
        term_id: int,
    ) -> bool:
        """Delete an academic term."""

        return self.service.delete_term(term_id)

    def set_current_term(
        self,
        term_id: int,
    ) -> AcademicTerm:
        """Set an academic term as the current term."""

        return self.service.set_current_term(term_id)

    def get_current_term(self) -> Optional[AcademicTerm]:
        """Get the current academic term."""

        return self.service.get_current_term()
