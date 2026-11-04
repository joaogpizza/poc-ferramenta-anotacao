from backend.home_view_model import HomeViewModel


def test_click_count_starts_at_zero():
    view_model = HomeViewModel()
    assert view_model.clickCount == 0


def test_register_click_increments_count():
    view_model = HomeViewModel()
    view_model.registerClick()
    view_model.registerClick()
    assert view_model.clickCount == 2


def test_register_click_emits_signal():
    view_model = HomeViewModel()
    emissions = []
    view_model.clickCountChanged.connect(lambda: emissions.append(True))

    view_model.registerClick()

    assert len(emissions) == 1
