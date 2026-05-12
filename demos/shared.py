"""Shared utilities for token selector demos."""

from typing import Tuple

from fasthtml.common import Div, H1, P

from cjm_fasthtml_daisyui.utilities.semantic_colors import bg_dui, text_dui
from cjm_fasthtml_tailwind.utilities.spacing import p, m
from cjm_fasthtml_tailwind.utilities.sizing import container, max_w
from cjm_fasthtml_tailwind.utilities.typography import font_size, font_weight
from cjm_fasthtml_tailwind.utilities.flexbox_and_grid import flex_display, items, justify
from cjm_fasthtml_tailwind.utilities.borders import rounded
from cjm_fasthtml_tailwind.core.base import combine_classes

from cjm_fasthtml_keyboard_navigation.core.focus_zone import FocusZone
from cjm_fasthtml_keyboard_navigation.core.navigation import ScrollOnly
from cjm_fasthtml_keyboard_navigation.core.actions import KeyAction
from cjm_fasthtml_keyboard_navigation.core.manager import ZoneManager
from cjm_fasthtml_keyboard_navigation.components.system import render_keyboard_system
from cjm_fasthtml_keyboard_navigation.components.hints_modal import render_keyboard_hints_modal

from cjm_fasthtml_token_selector.components.tokens import render_token_grid
from cjm_fasthtml_token_selector.components.inputs import render_hidden_inputs
from cjm_fasthtml_token_selector.js.core import generate_token_selector_js
from cjm_fasthtml_token_selector.keyboard.actions import (
    create_token_selector_mode,
    create_token_nav_actions,
    build_token_selector_url_map,
)


def build_keyboard_system(config, ids, mode_name, confirm_btn_id, cancel_btn_id,
                          confirm_url, cancel_url,
                          extra_actions: Tuple[KeyAction, ...] = ()):
    """Build keyboard navigation system for a token selector demo.

    Returns `(manager, system)` so the caller can also pass `manager` to
    `render_keyboard_hints_modal` for the shortcut modal.

    `extra_actions` lets a demo add KeyActions beyond the library defaults —
    used by the span demo to register documentation-only `KeyAction.documentation_only`
    entries for Shift+Left/Shift+Right (handled client-side by the token-selector's
    own shift-extend behavior, surfaced in the hints modal for discoverability).
    """
    zone = FocusZone(
        id=ids.container,
        item_selector=None,
        navigation=ScrollOnly(),
        zone_focus_classes=(),
        item_focus_classes=(),
    )
    zone_id = zone.id

    ts_mode = create_token_selector_mode(config, mode_name=mode_name)

    enter_mode_action = KeyAction(
        key="Enter",
        mode_enter=mode_name,
        not_modes=(mode_name,),
        zone_ids=(zone_id,),
        description="Enter token select mode",
        hint_group="Navigation",
    )

    token_actions = create_token_nav_actions(
        config,
        zone_id=zone_id,
        mode_name=mode_name,
        confirm_button_id=confirm_btn_id,
        cancel_button_id=cancel_btn_id,
    )

    all_actions = (enter_mode_action,) + token_actions + extra_actions

    manager = ZoneManager(
        zones=(zone,),
        actions=all_actions,
        modes=(ts_mode,),
    )

    url_map = build_token_selector_url_map(
        confirm_btn_id, cancel_btn_id, confirm_url, cancel_url,
    )
    include_selector = f"#{ids.anchor_input}, #{ids.focus_input}"
    swap_map = {btn_id: "none" for btn_id in url_map}
    include_map = {btn_id: include_selector for btn_id in url_map}

    system = render_keyboard_system(
        manager,
        url_map=url_map,
        target_map={},
        swap_map=swap_map,
        include_map=include_map,
        show_hints=False,
    )

    return manager, system


def render_demo_page(title, description, config, ids, tokens, state,
                     mode_name, confirm_btn_id, cancel_btn_id,
                     confirm_url, cancel_url, result_id,
                     extra_actions: Tuple[KeyAction, ...] = ()):
    """Render a standard token selector demo page with keyboard-hints modal.

    The hand-crafted "Keyboard Shortcuts" prose section was replaced by the
    `cjm-fasthtml-keyboard-navigation` 0.0.22 keyboard-hints modal — all
    KeyActions registered with the keyboard system (including the new
    documentation-only ArrowLeft/ArrowRight entries from `create_token_nav_actions`)
    surface automatically.
    """

    def page_content():
        manager, kb_system = build_keyboard_system(
            config, ids, mode_name,
            confirm_btn_id, cancel_btn_id,
            confirm_url, cancel_url,
            extra_actions=extra_actions,
        )

        hints_modal, hints_trigger, hints_script = render_keyboard_hints_modal(manager)

        ts_js = generate_token_selector_js(config, ids, state)

        return Div(
            # Header — title + description on left, hints-modal trigger on right
            Div(
                Div(
                    H1(title, cls=combine_classes(font_size._2xl, font_weight.bold)),
                    P(description,
                      cls=combine_classes(text_dui.base_content, font_size.sm)),
                ),
                hints_trigger,
                cls=combine_classes(flex_display, items.start, justify.between, m.b(4)),
            ),

            # Token grid section
            Div(
                render_token_grid(tokens, config, ids, state),
                id=ids.container,
                cls=combine_classes(p(4), bg_dui.base_100, rounded.lg, m.b(4)),
            ),

            # Hidden inputs for HTMX
            *render_hidden_inputs(ids, state),

            # Result panel
            Div(
                P("Press Enter to activate token selection, then navigate and confirm. Press ? for keyboard shortcuts.",
                  cls=combine_classes(text_dui.base_content, font_size.sm)),
                id=result_id,
                cls=combine_classes(p(4), bg_dui.base_200, rounded.lg, m.b(4)),
            ),

            # Keyboard system
            kb_system.script,
            kb_system.hidden_inputs,
            kb_system.action_buttons,

            # Hints modal + global ? key listener
            hints_modal,
            hints_script,

            # Token selector JS
            ts_js,

            cls=combine_classes(container, max_w._4xl, m.x.auto, p(4)),
        )

    return page_content
