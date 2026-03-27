"""Demo application for cjm-fasthtml-token-selector library.

Showcases the token selector component in all three selection modes:
  - Gap: caret between words for text splitting
  - Word: single word highlight for tagging
  - Span: range selection for annotation

Run with: python demo_app.py
"""


def main():
    """Initialize token selector demos and start the server."""
    from fasthtml.common import fast_app, Div, H1, H2, P, Span, A, APIRouter

    from cjm_fasthtml_daisyui.core.resources import get_daisyui_headers
    from cjm_fasthtml_daisyui.core.testing import create_theme_persistence_script
    from cjm_fasthtml_daisyui.components.data_display.card import card, card_body
    from cjm_fasthtml_daisyui.components.data_display.badge import badge, badge_colors
    from cjm_fasthtml_daisyui.utilities.semantic_colors import bg_dui, text_dui

    from cjm_fasthtml_tailwind.utilities.spacing import p, m
    from cjm_fasthtml_tailwind.utilities.sizing import container, max_w
    from cjm_fasthtml_tailwind.utilities.typography import font_size, font_weight, text_align
    from cjm_fasthtml_tailwind.utilities.flexbox_and_grid import grid_display, grid_cols, gap
    from cjm_fasthtml_tailwind.core.base import combine_classes

    from cjm_fasthtml_app_core.components.navbar import create_navbar
    from cjm_fasthtml_app_core.core.routing import register_routes
    from cjm_fasthtml_app_core.core.htmx import handle_htmx_request
    from cjm_fasthtml_app_core.core.layout import wrap_with_layout

    from cjm_fasthtml_token_selector.core.config import _reset_prefix_counter

    from demos.shared import render_demo_page
    import demos.gap as gap_demo
    import demos.word as word_demo
    import demos.span as span_demo

    print("\n" + "=" * 70)
    print("Initializing cjm-fasthtml-token-selector Demo")
    print("=" * 70)

    _reset_prefix_counter()

    APP_ID = "toksel"

    app, rt = fast_app(
        pico=False,
        hdrs=[*get_daisyui_headers(), create_theme_persistence_script()],
        title="Token Selector Demo",
        htmlkw={'data-theme': 'light'},
        session_cookie=f'session_{APP_ID}_',
        secret_key=f'{APP_ID}-demo-secret',
    )

    router = APIRouter(prefix="")

    # -------------------------------------------------------------------------
    # Set up demos
    # -------------------------------------------------------------------------
    gap_cfg = gap_demo.setup()
    word_cfg = word_demo.setup()
    span_cfg = span_demo.setup()

    print(f"  Gap demo: {len(gap_cfg['tokens'])} tokens")
    print(f"  Word demo: {len(word_cfg['tokens'])} tokens")
    print(f"  Span demo: {len(span_cfg['tokens'])} tokens")

    # Build page content factories using shared renderer
    shared_keys = (
        'title', 'description', 'config', 'ids', 'tokens', 'state',
        'mode_name', 'confirm_btn_id', 'cancel_btn_id',
        'confirm_url', 'cancel_url', 'result_id', 'keyboard_hints',
    )
    gap_page = render_demo_page(**{k: gap_cfg[k] for k in shared_keys})
    word_page = render_demo_page(**{k: word_cfg[k] for k in shared_keys})
    span_page = render_demo_page(**{k: span_cfg[k] for k in shared_keys})

    # -------------------------------------------------------------------------
    # Page routes
    # -------------------------------------------------------------------------
    @router
    def index(request):
        """Homepage with demo overview."""

        def home_content():
            return Div(
                H1("Token Selector Demo",
                   cls=combine_classes(font_size._4xl, font_weight.bold, m.b(4))),

                P("An interactive token grid component for FastHTML with three "
                  "selection modes, keyboard navigation integration, and "
                  "HTMX-driven state management.",
                  cls=combine_classes(font_size.lg, text_dui.base_content,
                                     m.b(8))),

                # Demo cards
                Div(
                    _demo_card(
                        "Gap Mode",
                        "Place a caret between words to define split points. "
                        "Useful for text segmentation tasks.",
                        badges=[("Gap", badge_colors.primary),
                                ("Split", badge_colors.secondary)],
                        href=demo_gap.to(),
                        btn_cls="btn btn-primary",
                    ),
                    _demo_card(
                        "Word Mode",
                        "Select individual words by highlighting. "
                        "Useful for tagging and marking tokens.",
                        badges=[("Word", badge_colors.primary),
                                ("Tag", badge_colors.secondary)],
                        href=demo_word.to(),
                        btn_cls="btn btn-secondary",
                    ),
                    _demo_card(
                        "Span Mode",
                        "Select a range of words for annotation. "
                        "Useful for named entity recognition.",
                        badges=[("Span", badge_colors.primary),
                                ("Annotate", badge_colors.secondary)],
                        href=demo_span.to(),
                        btn_cls="btn btn-accent",
                    ),
                    cls=combine_classes(
                        grid_display, grid_cols(1), grid_cols(3).md,
                        gap(6), m.b(8),
                    ),
                ),

                # Keyboard shortcuts overview
                Div(
                    H2("Common Keyboard Shortcuts",
                       cls=combine_classes(font_size._2xl, font_weight.bold,
                                          m.b(4))),
                    Div(
                        P("Enter \u2014 Activate token select mode",
                          cls=m.b(1)),
                        P("Left/Right \u2014 Navigate between tokens",
                          cls=m.b(1)),
                        P("Shift+Left/Right \u2014 Extend selection (Span mode)",
                          cls=m.b(1)),
                        P("Home/End \u2014 Jump to first/last position",
                          cls=m.b(1)),
                        P("Enter/Space \u2014 Confirm selection",
                          cls=m.b(1)),
                        P("Escape \u2014 Cancel selection",
                          cls=m.b(1)),
                        cls=combine_classes(text_align.left, max_w.md,
                                           m.x.auto, font_size.sm),
                    ),
                    cls=m.b(8),
                ),

                cls=combine_classes(container, max_w._5xl, m.x.auto, p(8),
                                    text_align.center),
            )

        return handle_htmx_request(
            request, home_content,
            wrap_fn=lambda content: wrap_with_layout(content, navbar=navbar),
        )

    def _demo_card(title, description, badges, href, btn_cls):
        """Render a demo card for the homepage."""
        return Div(
            Div(
                H2(title, cls=combine_classes(font_size.xl,
                                             font_weight.semibold, m.b(2))),
                P(description,
                  cls=combine_classes(text_dui.base_content, m.b(4))),
                Div(
                    *[Span(label, cls=combine_classes(badge, color, m.r(2)))
                      for label, color in badges],
                    cls=m.b(4),
                ),
                A("Open Demo", href=href, cls=btn_cls),
                cls=card_body,
            ),
            cls=combine_classes(card, bg_dui.base_200),
        )

    @router
    def demo_gap(request):
        """Gap mode demo page."""
        return handle_htmx_request(
            request, gap_page,
            wrap_fn=lambda content: wrap_with_layout(content, navbar=navbar),
        )

    @router
    def demo_word(request):
        """Word mode demo page."""
        return handle_htmx_request(
            request, word_page,
            wrap_fn=lambda content: wrap_with_layout(content, navbar=navbar),
        )

    @router
    def demo_span(request):
        """Span mode demo page."""
        return handle_htmx_request(
            request, span_page,
            wrap_fn=lambda content: wrap_with_layout(content, navbar=navbar),
        )

    # -------------------------------------------------------------------------
    # Navbar & route registration
    # -------------------------------------------------------------------------
    navbar = create_navbar(
        title="Token Selector Demo",
        nav_items=[
            ("Home", index),
            ("Gap", demo_gap),
            ("Word", demo_word),
            ("Span", demo_span),
        ],
        home_route=index,
        theme_selector=True,
    )

    register_routes(
        app, router,
        gap_cfg['router'], word_cfg['router'], span_cfg['router'],
    )

    # Debug output
    print("\n" + "=" * 70)
    print("Registered Routes:")
    print("=" * 70)
    for route in app.routes:
        if hasattr(route, 'path'):
            print(f"  {route.path}")
    print("=" * 70)
    print("Demo App Ready!")
    print("=" * 70 + "\n")

    return app


if __name__ == "__main__":
    import uvicorn
    import webbrowser
    import threading

    app = main()

    port = 5034
    host = "0.0.0.0"
    display_host = 'localhost' if host in ['0.0.0.0', '127.0.0.1'] else host

    print(f"Server: http://{display_host}:{port}")
    print(f"\n  http://{display_host}:{port}/              -- Homepage")
    print(f"  http://{display_host}:{port}/demo_gap      -- Gap mode")
    print(f"  http://{display_host}:{port}/demo_word     -- Word mode")
    print(f"  http://{display_host}:{port}/demo_span     -- Span mode")
    print()

    timer = threading.Timer(1.5, lambda: webbrowser.open(f"http://localhost:{port}"))
    timer.daemon = True
    timer.start()

    uvicorn.run(app, host=host, port=port)
