"""Word mode demo: single word selection for tagging."""

from fasthtml.common import APIRouter, Div, P, Span

from cjm_fasthtml_daisyui.utilities.semantic_colors import bg_dui, text_dui
from cjm_fasthtml_tailwind.utilities.spacing import p, m
from cjm_fasthtml_tailwind.utilities.typography import font_size, font_weight
from cjm_fasthtml_tailwind.utilities.borders import rounded
from cjm_fasthtml_tailwind.core.base import combine_classes

from cjm_fasthtml_token_selector.core.config import TokenSelectorConfig
from cjm_fasthtml_token_selector.core.html_ids import TokenSelectorHtmlIds
from cjm_fasthtml_token_selector.core.models import TokenSelectorState
from cjm_fasthtml_token_selector.helpers.tokenizer import tokenize, get_token_list

from demos.data import WORD_TEXT


def setup(route_prefix="/word"):
    """Set up the word mode token selector demo."""
    config = TokenSelectorConfig(prefix="word", selection_mode="word")
    ids = TokenSelectorHtmlIds(prefix=config.prefix)
    tokens = tokenize(WORD_TEXT)
    state = TokenSelectorState(anchor=0, focus=0, word_count=len(tokens))

    MODE_NAME = "token-select"
    CONFIRM_BTN = "word-confirm-btn"
    CANCEL_BTN = "word-cancel-btn"
    RESULT_ID = "word-result"

    router = APIRouter(prefix=route_prefix)

    @router
    def confirm(kw:dict):
        """Handle word selection confirm."""
        anchor = int(kw.get(ids.anchor_name, 0))
        word_list = get_token_list(WORD_TEXT)
        selected = word_list[anchor] if 0 <= anchor < len(word_list) else "(none)"

        return Div(
            P("Selected Word:",
              cls=combine_classes(font_weight.semibold, m.b(2))),
            P(Span(selected,
                   cls=combine_classes(font_size.xl, font_weight.bold)),
              cls=m.b(2)),
            P(f"Token index: {anchor}",
              cls=combine_classes(font_size.sm, text_dui.base_content)),
            id=RESULT_ID,
            hx_swap_oob="true",
            cls=combine_classes(p(4), bg_dui.base_200, rounded.lg, m.b(4)),
        )

    @router
    def cancel(kw:dict):
        """Handle word selection cancel."""
        return Div(
            P("Selection cancelled. Press Enter to try again.",
              cls=combine_classes(text_dui.base_content, font_size.sm)),
            id=RESULT_ID,
            hx_swap_oob="true",
            cls=combine_classes(p(4), bg_dui.base_200, rounded.lg, m.b(4)),
        )

    return dict(
        config=config,
        ids=ids,
        tokens=tokens,
        state=state,
        router=router,
        mode_name=MODE_NAME,
        confirm_btn_id=CONFIRM_BTN,
        cancel_btn_id=CANCEL_BTN,
        confirm_url=confirm.to(),
        cancel_url=cancel.to(),
        result_id=RESULT_ID,
        title="Word Mode",
        description=(
            "Select individual words by highlighting them. "
            "Good for tagging or marking specific tokens."
        ),
        keyboard_hints=[
            "Enter \u2014 Activate token select mode",
            "Left/Right \u2014 Move highlight between words",
            "Home/End \u2014 Jump to first/last word",
            "Enter/Space \u2014 Confirm selected word",
            "Escape \u2014 Cancel selection",
        ],
    )
