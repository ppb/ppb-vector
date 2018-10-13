from ppb_vector import Vector2
import hypothesis.strategies as st

vectors = lambda: st.builds(
    Vector2,
    st.floats(min_value=-1e300, max_value=1e300),
    st.floats(min_value=-1e300, max_value=1e300)
)

@st.composite
def units(draw, elements=st.floats(min_value=0, max_value=360)):
    angle = draw(elements)
    return Vector2(1, 0).rotate(angle)


def angle_isclose(x, y, epsilon = 6.5e-5):
    d = (x - y) % 360
    return (d < epsilon) or (d > 360 - epsilon)
