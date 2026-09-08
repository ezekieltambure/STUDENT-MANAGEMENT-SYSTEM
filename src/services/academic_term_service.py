from typing import List, Optional

from src.models.academic_term import AcademicTerm
from src.repositories.academic_term_repository import (
    AcademicTermRepository,
)


class AcademicTermService:
    """Provides business logic for academic terms."""

    def __init__(
        self,
        repository: Optional[AcademicTermRepository] = None,
    ) -> None:
        self.repository = repository or AcademicTermRepository()

    def create_term(
        self,
        term_name: str,
        academic_year: int,
        start_date,
        end_date,
        is_current: bool = False,
    ) -> AcademicTerm:
        """Create a new academic term."""

        if self.repository.exists_by_name_and_year(
            term_name,
            academic_year,
        ):
            raise ValueError(
                "An academic term with this name and year "
                "already exists."
            )

        term = AcademicTerm(
            term_name=term_name,
            academic_year=academic_year,
            start_date=start_date,
            end_date=end_date,
            is_current=is_current,
        )

        if is_current:
            created_term = self.repository.create(
                term
            )
            self.repository.set_current(created_term.id)
            return self.repository.find_by_id(created_term.id)

        return self.repository.create(term)

    def get_term(
        self,
        term_id: int,
    ) -> Optional[AcademicTerm]:
        """Return an academic term by ID."""

        return self.repository.find_by_id(term_id)

    def get_all_terms(self) -> List[AcademicTerm]:
        """Return all academic terms."""

        return self.repository.list_all()

    def search_terms(
        self,
        query: str,
    ) -> List[AcademicTerm]:
        """Search academic terms."""

        return self.repository.search(query)

    def update_term(
        self,
        term: AcademicTerm,
    ) -> AcademicTerm:
        """Update an academic term."""

        if term.id is None:
            raise ValueError(
                "Academic term ID is required for update."
            )

        existing = self.repository.find_by_id(term.id)

        if existing is None:
            raise ValueError(
                "Academic term not found."
            )

        if self.repository.exists_by_name_and_year(
            term.term_name,
            term.academic_year,
            exclude_id=term.id,
        ):
            raise ValueError(
                "An academic term with this name and year "
                "already exists."
            )

        self.repository.update(term)

        if term.is_current:
            self.repository.set_current(term.id)

        return self.repository.find_by_id(term.id)

    def delete_term(
        self,
        term_id: int,
    ) -> bool:
        """Delete an academic term."""

        existing = self.repository.find_by_id(term_id)

        if existing is None:
            raise ValueError(
                "Academic term not found."
            )

        return self.repository.delete(term_id)

    def set_current_term(
        self,
        term_id: int,
    ) -> AcademicTerm:
        """Set an academic term as the current term."""

        existing = self.repository.find_by_id(term_id)

        if existing is None:
            raise ValueError(
                "Academic term not found."
            )

        self.repository.set_current(term_id)

        return self.repository.find_by_id(term_id)

    def get_current_term(
        self,
    ) -> Optional[AcademicTerm]:
        """Return the current academic term."""

        return self.repository.get_current()
