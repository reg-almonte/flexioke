import pytest
from pathlib import Path

def test_v041_domain_tiered_test_directory_structure():
    """Verify that tests/ is partitioned into api, services, frontend, and integration directories."""
    tests_dir = Path("tests")
    assert (tests_dir / "api").is_dir(), "tests/api must exist"
    assert (tests_dir / "services").is_dir(), "tests/services must exist"
    assert (tests_dir / "frontend").is_dir(), "tests/frontend must exist"
    assert (tests_dir / "integration").is_dir(), "tests/integration must exist"
    
    # Verify zero test files in tests root
    root_test_files = list(tests_dir.glob("test_*.py"))
    assert len(root_test_files) == 0, f"No test_*.py files should remain in tests/ root: {root_test_files}"
    
    # Verify pytest.ini exists and defines testpaths = tests
    pytest_ini = Path("pytest.ini")
    assert pytest_ini.exists(), "pytest.ini must exist"
    content = pytest_ini.read_text(encoding="utf-8")
    assert "testpaths = tests" in content
    assert "pythonpath = ." in content

def test_v041_assessment_report_integrity():
    """Verify tests/ASSESSMENT_REPORT.md is present and thoroughly answers all 7 dimensions."""
    report_file = Path("tests/ASSESSMENT_REPORT.md")
    assert report_file.exists(), "tests/ASSESSMENT_REPORT.md must exist"
    
    report_text = report_file.read_text(encoding="utf-8")
    assert "Executive Summary & Quality Scorecard" in report_text
    assert "2.1 Architecture Fit" in report_text or "2.1 Architecture & Design Fit" in report_text
    assert "2.2 Maintainability" in report_text or "2.2 Maintainability & Code Structure" in report_text
    assert "2.3 Reliability" in report_text or "2.3 Reliability, Concurrency & Error Resilience" in report_text
    assert "2.4 Efficiency" in report_text or "2.4 Efficiency & System Performance" in report_text
    assert "2.5 Testability" in report_text or "2.5 Testability & Suite Architecture" in report_text
    assert "2.6 Consistency" in report_text or "2.6 Consistency & API/Data Standards" in report_text
    assert "2.7 Readability" in report_text or "2.7 Readability, Documentation & Type Safety" in report_text
    assert "Prioritized Recommendations & Refactoring Roadmap" in report_text
    assert "Quality Score" in report_text or "Quality Index" in report_text

def test_v041_refactoring_roadmap_integrity():
    """Verify docs/design/REFACTORING_ROADMAP.md defines actionable technical debt backlog and migration protocol."""
    roadmap_file = Path("docs/design/REFACTORING_ROADMAP.md")
    assert roadmap_file.exists(), "docs/design/REFACTORING_ROADMAP.md must exist"
    
    roadmap_text = roadmap_file.read_text(encoding="utf-8")
    assert "REF-01" in roadmap_text
    assert "REF-02" in roadmap_text
    assert "REF-03" in roadmap_text
    assert "REF-04" in roadmap_text
    assert "REF-05" in roadmap_text
    assert "REF-06" in roadmap_text
    assert "Implementation & Verification Protocol" in roadmap_text
