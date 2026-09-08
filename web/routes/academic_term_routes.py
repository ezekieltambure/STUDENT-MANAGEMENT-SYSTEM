from datetime import date

from flask import Blueprint, redirect, render_template, request, session, url_for

from src.controllers.academic_term_controller import AcademicTermController
from src.models.academic_term import AcademicTerm


academic_term_bp = Blueprint(
    "academic_terms",
    __name__,
    url_prefix="/academic-terms",
)

academic_term_controller = AcademicTermController()


def _require_login():
    """Require an authenticated user."""

    if "user_id" not in session:
        return redirect(url_for("home"))

    return None


@academic_term_bp.route("/")
def list_terms():
    """Display all academic terms."""

    redirect_response = _require_login()

    if redirect_response:
        return redirect_response

    query = request.args.get("q", "").strip()

    if query:
        terms = academic_term_controller.search_terms(query)
    else:
        terms = academic_term_controller.get_all_terms()

    current_term = academic_term_controller.get_current_term()

    return render_template(
        "academic_terms/list.html",
        terms=terms,
        current_term=current_term,
        query=query,
    )


@academic_term_bp.route("/new", methods=["GET", "POST"])
def create_term():
    """Create a new academic term."""

    redirect_response = _require_login()

    if redirect_response:
        return redirect_response

    if request.method == "POST":
        term_name = request.form.get(
            "term_name",
            "",
        ).strip()

        academic_year_raw = request.form.get(
            "academic_year",
            "",
        ).strip()

        start_date_raw = request.form.get(
            "start_date",
            "",
        ).strip()

        end_date_raw = request.form.get(
            "end_date",
            "",
        ).strip()

        is_current = (
            request.form.get("is_current") == "on"
        )

        try:
            academic_year = int(academic_year_raw)

            start_date = date.fromisoformat(
                start_date_raw
            )

            end_date = date.fromisoformat(
                end_date_raw
            )

            term = academic_term_controller.create_term(
                term_name=term_name,
                academic_year=academic_year,
                start_date=start_date,
                end_date=end_date,
                is_current=is_current,
            )

            if term is None or term.id is None:
                return "Academic term could not be created.", 500

            return redirect(
                url_for(
                    "academic_terms.view_term",
                    term_id=term.id,
                )
            )

        except (ValueError, TypeError) as exc:
            return render_template(
                "academic_terms/form.html",
                term=None,
                error=str(exc),
            )

    return render_template(
        "academic_terms/form.html",
        term=None,
        error=None,
    )


@academic_term_bp.route("/<int:term_id>")
def view_term(term_id):
    """Display one academic term."""

    redirect_response = _require_login()

    if redirect_response:
        return redirect_response

    term = academic_term_controller.get_term(term_id)

    if term is None:
        return "Academic term not found", 404

    return render_template(
        "academic_terms/detail.html",
        term=term,
    )


@academic_term_bp.route("/<int:term_id>/edit", methods=["GET", "POST"])
def edit_term(term_id):
    """Edit an academic term."""

    redirect_response = _require_login()

    if redirect_response:
        return redirect_response

    term = academic_term_controller.get_term(term_id)

    if term is None:
        return "Academic term not found", 404

    if request.method == "POST":
        term_name = request.form.get(
            "term_name",
            "",
        ).strip()

        academic_year_raw = request.form.get(
            "academic_year",
            "",
        ).strip()

        start_date_raw = request.form.get(
            "start_date",
            "",
        ).strip()

        end_date_raw = request.form.get(
            "end_date",
            "",
        ).strip()

        is_current = (
            request.form.get("is_current") == "on"
        )

        try:
            academic_year = int(academic_year_raw)

            start_date = date.fromisoformat(
                start_date_raw
            )

            end_date = date.fromisoformat(
                end_date_raw
            )

            updated_term = AcademicTerm(
                id=term.id,
                term_name=term_name,
                academic_year=academic_year,
                start_date=start_date,
                end_date=end_date,
                is_current=is_current,
            )

            academic_term_controller.update_term(
                updated_term
            )

            return redirect(
                url_for(
                    "academic_terms.view_term",
                    term_id=term.id,
                )
            )

        except (ValueError, TypeError) as exc:
            return render_template(
                "academic_terms/form.html",
                term=term,
                error=str(exc),
            )

    return render_template(
        "academic_terms/form.html",
        term=term,
        error=None,
    )


@academic_term_bp.route(
    "/<int:term_id>/set-current",
    methods=["POST"],
)
def set_current_term(term_id):
    """Set an academic term as the current term."""

    redirect_response = _require_login()

    if redirect_response:
        return redirect_response

    try:
        academic_term_controller.set_current_term(
            term_id
        )
    except ValueError as exc:
        return str(exc), 400

    return redirect(
        url_for(
            "academic_terms.view_term",
            term_id=term_id,
        )
    )


@academic_term_bp.route(
    "/<int:term_id>/delete",
    methods=["POST"],
)
def delete_term(term_id):
    """Delete an academic term."""

    redirect_response = _require_login()

    if redirect_response:
        return redirect_response

    try:
        academic_term_controller.delete_term(term_id)
    except ValueError as exc:
        return str(exc), 400

    return redirect(
        url_for(
            "academic_terms.list_terms"
        )
    )
