"""Scale-aware SephirothOS design metrics."""

from dataclasses import dataclass

from sephirothos.services.display_scale import DisplayScaleService


@dataclass(frozen=True, slots=True)
class UiMetrics:
    """Resolved Qt measurements for the active interface scale."""

    # Base-5 spacing
    space_5: int
    space_10: int
    space_15: int
    space_20: int
    space_25: int
    space_30: int
    space_40: int
    space_50: int
    space_60: int

    # Typography
    font_caption: int
    font_small: int
    font_body: int
    font_subtitle: int
    font_emphasis: int
    font_hero_subtitle: int
    font_page_title: int
    font_hero_title: int

    # Borders and radii
    border_thin: int
    border_strong: int
    radius_small: int
    radius_medium: int
    radius_large: int

    # Shell geometry
    top_bar_height: int
    sidebar_width: int

    # Component geometry
    scrollbar_extent: int
    checkbox_extent: int
    progress_height: int
    appearance_feature_card_height: int

    @classmethod
    def from_scale(
        cls,
        scale: DisplayScaleService,
    ) -> "UiMetrics":
        px = scale.scale_pixels

        return cls(
            space_5=px(5),
            space_10=px(10),
            space_15=px(15),
            space_20=px(20),
            space_25=px(25),
            space_30=px(30),
            space_40=px(40),
            space_50=px(50),
            space_60=px(60),
            font_caption=px(12),
            font_small=px(14),
            font_body=px(16),
            font_subtitle=px(18),
            font_emphasis=px(24),
            font_hero_subtitle=px(32),
            font_page_title=px(36),
            font_hero_title=px(60),
            border_thin=max(1, px(1)),
            border_strong=max(2, px(2)),
            radius_small=px(4),
            radius_medium=px(8),
            radius_large=px(12),
            top_bar_height=px(64),
            sidebar_width=px(264),
            scrollbar_extent=px(8),
            checkbox_extent=px(20),
            progress_height=max(2, px(4)),
            appearance_feature_card_height=px(400),
        )
