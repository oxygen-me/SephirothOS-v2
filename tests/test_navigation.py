from sephirothos.ui.tabs.navigation import (
    DEFAULT_TAB,
    TAB_LABELS,
    TAB_ORDER,
    TabId,
)


def test_all_tabs_have_labels() -> None:
    assert set(TAB_LABELS) == set(TabId)


def test_tab_order_contains_each_tab_once() -> None:
    assert len(TAB_ORDER) == len(TabId)
    assert len(set(TAB_ORDER)) == len(TabId)
    assert set(TAB_ORDER) == set(TabId)


def test_primary_tab_order_matches_product_layout() -> None:
    assert TAB_ORDER == (
        TabId.HOME,
        TabId.APPS,
        TabId.SETTINGS,
        TabId.CLI,
    )


def test_home_is_the_default_tab() -> None:
    assert DEFAULT_TAB is TabId.HOME


def test_visible_tab_labels_are_stable() -> None:
    assert TAB_LABELS == {
        TabId.HOME: "Home",
        TabId.APPS: "Apps",
        TabId.SETTINGS: "Settings",
        TabId.CLI: "CLI",
    }
