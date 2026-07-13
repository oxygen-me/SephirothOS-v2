"""Home tab page identities."""

from enum import StrEnum


class HomePageId(StrEnum):
    DASHBOARD = "dashboard"


HOME_PAGE_LABELS: dict[HomePageId, str] = {
    HomePageId.DASHBOARD: "Dashboard",
}

HOME_PAGE_ORDER: tuple[HomePageId, ...] = (HomePageId.DASHBOARD,)

DEFAULT_HOME_PAGE = HomePageId.DASHBOARD
