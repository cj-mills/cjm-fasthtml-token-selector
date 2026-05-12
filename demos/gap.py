"""Gap mode demo: caret between words for text splitting."""
from fasthtml.common import APIRouter, Div, P, Span

from cjm_fasthtml_daisyui.utilities.semantic_colors import bg_dui, text_dui
from cjm_fasthtml_tailwind.utilities.spacing import p, m
from cjm_fasthtml_tailwind.utilities.typography import font_size, font_weight
from cjm_fasthtml_tailwind.utilities.borders import rounded
from cjm_fasthtml_tailwind.core.base import combine_classes

from cjm_fasthtml_token_selector.core.config import TokenSelectorConfig
from cjm_fasthtml_token_selector.core.html_ids import TokenSelectorHtmlIds
from cjm_fasthtml_token_selector.core.models import TokenSelectorState
from cjm_fasthtml_token_selector.helpers.tokenizer import (
    tokenize, get_token_list, token_index_to_char_position,
)

from demos.data import GAP_TEXT


def setup(route_prefix="/gap"):
    """Set up the gap mode token selector demo."""
    config = TokenSelectorConfig(prefix="gap", selection_mode="gap")
    ids = TokenSelectorHtmlIds(prefix=config.prefix)
    tokens = tokenize(GAP_TEXT)
    state = TokenSelectorState(anchor=0, focus=0, word_count=len(tokens))

    MODE_NAME = "token-select"
    CONFIRM_BTN = "gap-confirm-btn"
    CANCEL_BTN = "gap-cancel-btn"
    RESULT_ID = "gap-result"

    router = APIRouter(prefix=route_prefix)

    @router
    def confirm(kw:dict):
        """Handle gap selection confirm."""
        anchor = int(kw.get(ids.anchor_name, 0))
        char_pos = token_index_to_char_position(GAP_TEXT, anchor)
        before = GAP_TEXT[:char_pos].rstrip()
        after = GAP_TEXT[char_pos:].lstrip()

        return Div(
            P("Split Result:",
              cls=combine_classes(font_weight.semibold, m.b(2))),
            P(Span("Before: ", cls=font_weight.semibold),
              Span(f'"{before}"' if before else "(empty)",
                   cls=text_dui.base_content)),
            P(Span("After: ", cls=font_weight.semibold),
              Span(f'"{after}"' if after else "(empty)",
                   cls=text_dui.base_content)),
            P(f"Split at gap position {anchor} (character {char_pos})",
              cls=combine_classes(font_size.sm, text_dui.base_content, m.t(2))),
            id=RESULT_ID,
            hx_swap_oob="true",
            cls=combine_classes(p(4), bg_dui.base_200, rounded.lg, m.b(4)),
        )

    @router
    def cancel(kw:dict):
        """Handle gap selection cancel."""
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
        title="Gap Mode",
        description=(
            "Place a caret between words to define a split point. "
            "The pulsing indicator shows the current gap position."
        ),
        # No extra KeyActions beyond what create_token_nav_actions emits \u2014 all
        # gap-mode shortcuts (Enter activate, Left/Right caret, Home/End,
        # Enter/Space confirm, Escape cancel) surface in the keyboard-hints
        # modal via the library's registered + documentation-only KeyActions.
        extra_actions=(),
    )
