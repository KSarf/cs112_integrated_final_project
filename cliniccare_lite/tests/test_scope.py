"""Non-diagnostic scope tests for ClinicCare-Lite."""

from cliniccare_lite.app.analytics.operational_metrics import (
    get_operational_summary,
)


def test_non_diagnostic_warning_is_visible(
    client,
):
    """The application should clearly display its safety boundary."""

    response = client.get("/")

    assert response.status_code == 200

    assert b"Administrative use only" in response.data

    assert b"does not diagnose patients" in response.data

    assert b"must not be used for emergencies" in response.data


def test_no_diagnostic_routes_exist(
    app,
):
    """ClinicCare should not contain diagnostic routes."""

    routes = " ".join(rule.rule.lower() for rule in app.url_map.iter_rules())

    prohibited_terms = [
        "diagnose",
        "diagnosis",
        "treatment",
        "prescribe",
        "prescription",
        "symptom-checker",
        "risk-score",
    ]

    for term in prohibited_terms:
        assert term not in routes


def test_analytics_are_administrative_only(
    app,
):
    """Operational analytics should not contain medical scoring."""

    with app.app_context():

        summary = get_operational_summary(clinician_id=999999)

    metric_names = " ".join(summary.keys()).lower()

    prohibited_terms = [
        "diagnosis",
        "disease",
        "symptom",
        "treatment",
        "prescription",
        "health_score",
        "risk_score",
    ]

    for term in prohibited_terms:
        assert term not in metric_names
