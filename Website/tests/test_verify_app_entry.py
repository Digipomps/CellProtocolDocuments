from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "verify_app_entry.py"
SPEC = importlib.util.spec_from_file_location("verify_app_entry", MODULE_PATH)
assert SPEC and SPEC.loader
verify_app_entry = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verify_app_entry)


def hero(state: str, first: str, first_href: str, second: str, second_href: str, *, target: str = "") -> str:
    target_attr = f' target="{target}"' if target else ""
    return f"""
      <section class="hero" data-app-entry-state="{state}">
        <div class="hero-actions">
          <a class="button button-primary" href="{first_href}"{target_attr}>{first}</a>
          <a class="button button-secondary" href="{second_href}">{second}</a>
        </div>
      </section>
    """


class AppEntryGuardTests(unittest.TestCase):
    def test_current_blocked_index_passes(self) -> None:
        index = MODULE_PATH.parents[1] / "index.html"
        self.assertEqual([], verify_app_entry.validate_markup(index.read_text(encoding="utf-8")))

    def test_valid_public_demo_passes_with_explicit_origin(self) -> None:
        markup = hero(
            "public-demo",
            "Åpne HAVEN-demoen",
            "https://app.digipomps.org/install",
            "Forstå HAVEN",
            "#velg-inngang",
        )
        self.assertEqual([], verify_app_entry.validate_markup(markup, "https://app.digipomps.org"))

    def test_active_cta_without_allowlist_fails(self) -> None:
        markup = hero(
            "public-app",
            "Installer HAVEN",
            "https://app.digipomps.org/install",
            "Forstå HAVEN",
            "#velg-inngang",
        )
        errors = verify_app_entry.validate_markup(markup)
        self.assertTrue(any("--allow-origin" in error for error in errors))

    def test_staging_url_fails(self) -> None:
        markup = hero(
            "public-demo",
            "Åpne HAVEN-demoen",
            "https://staging.haven.digipomps.org/install",
            "Forstå HAVEN",
            "#velg-inngang",
        )
        errors = verify_app_entry.validate_markup(markup, "https://staging.haven.digipomps.org")
        self.assertTrue(any("staging" in error.lower() for error in errors))

    def test_wrong_maturity_copy_fails(self) -> None:
        markup = hero(
            "public-demo",
            "Installer HAVEN",
            "https://app.digipomps.org/install",
            "Forstå HAVEN",
            "#velg-inngang",
        )
        errors = verify_app_entry.validate_markup(markup, "https://app.digipomps.org")
        self.assertTrue(any("cta-teksten" in error.lower() for error in errors))

    def test_preview_url_fails(self) -> None:
        markup = hero(
            "public-demo",
            "Åpne HAVEN-demoen",
            "https://preview.haven.digipomps.org/install",
            "Forstå HAVEN",
            "#velg-inngang",
        )
        errors = verify_app_entry.validate_markup(markup, "https://preview.haven.digipomps.org")
        self.assertTrue(any("review" in error.lower() for error in errors))

    def test_new_tab_fails(self) -> None:
        markup = hero(
            "public-demo",
            "Åpne HAVEN-demoen",
            "https://app.digipomps.org/install",
            "Forstå HAVEN",
            "#velg-inngang",
            target="_blank",
        )
        errors = verify_app_entry.validate_markup(markup, "https://app.digipomps.org")
        self.assertTrue(any("samme fane" in error.lower() for error in errors))

    def test_third_hero_action_fails(self) -> None:
        markup = hero(
            "public-demo",
            "Åpne HAVEN-demoen",
            "https://app.digipomps.org/install",
            "Forstå HAVEN",
            "#velg-inngang",
        ).replace("</div>", '<a class="button" href="/bevis/">Tredje valg</a></div>', 1)
        errors = verify_app_entry.validate_markup(markup, "https://app.digipomps.org")
        self.assertTrue(any("nøyaktig to" in error.lower() for error in errors))


if __name__ == "__main__":
    unittest.main()
