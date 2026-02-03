"""Span mode demo: range selection for annotation."""

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

from demos.data import SPAN_TEXT


def setup(route_prefix="/span"):
    """Set up the span mode token selector demo."""
    config = TokenSelectorConfig(prefix="span", selection_mode="span")
    ids = TokenSelectorHtmlIds(prefix=config.prefix)
    tokens = tokenize(SPAN_TEXT)
    state = TokenSelectorState(anchor=0, focus=0, word_count=len(tokens))

    MODE_NAME = "token-select"
    CONFIRM_BTN = "span-confirm-btn"
    CANCEL_BTN = "span-cancel-btn"
    RESULT_ID = "span-result"

    router = APIRouter(prefix=route_prefix)

    @router
    def confirm(kw:dict):
        """Handle span selection confirm."""
        anchor = int(kw.get(ids.anchor_name, 0))
        focus = int(kw.get(ids.focus_name, 0))
        word_list = get_token_list(SPAN_TEXT)
        lo, hi = min(anchor, focus), max(anchor, focus)
        selected_words = word_list[lo:hi + 1] if lo < len(word_list) else []
        selected_text = " ".join(selected_words)

        return Div(
            P("Selected Span:",
              cls=combine_classes(font_weight.semibold, m.b(2))),
            P(Span(f'"{selected_text}"',
                   cls=combine_classes(font_size.lg, font_weight.bold)),
              cls=m.b(2)),
            P(f"Tokens {lo} to {hi} ({hi - lo + 1} words)",
              cls=combine_classes(font_size.sm, text_dui.base_content)),
            id=RESULT_ID,
            hx_swap_oob="true",
            cls=combine_classes(p(4), bg_dui.base_200, rounded.lg, m.b(4)),
        )

    @router
    def cancel(kw:dict):
        """Handle span selection cancel."""
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
        title="Span Mode",
        description=(
            "Select a range of words for annotation. "
            "Use Shift+Arrow to extend the selection from the anchor."
        ),
        keyboard_hints=[
            "Enter \u2014 Activate token select mode",
            "Left/Right \u2014 Move to a word (resets anchor)",
            "Shift+Left/Right \u2014 Extend selection from anchor",
            "Home/End \u2014 Jump to first/last word",
            "Enter/Space \u2014 Confirm selected span",
            "Escape \u2014 Cancel selection",
        ],
    )
