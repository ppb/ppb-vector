from ppb_vector import Vector2
import hypothesis.strategies as st

vectors = lambda: st.builds(
    Vector2,
    st.floats(allow_nan=False, allow_infinity=False),
    st.floats(allow_nan=False, allow_infinity=False)
)

@st.composite
def units(draw, elements=st.floats(min_value=0, max_value=360)):
    angle = draw(elements)
    return Vector2(1, 0).rotate(angle)
