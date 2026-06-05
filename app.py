import streamlit as st
import math

# --- 1. PAGE SETUP & MOBLE STYLING ---
st.set_page_config(
    page_title="Scientific Matrix Calculator",
    page_icon="🧮",
    layout="centered"
)

st.markdown("""
<style>
/* Make calculation action buttons large and clear on mobile screens */
div.stButton > button:first-child {
    width: 100%;
    height: 50px;
    font-size: 18px;
    font-weight: bold;
    background-color: #3b82f6;
    color: white;
    border-radius: 8px;
}
input {
    font-size: 20px !important;
}
.calc-display {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 10px;
    border-left: 5px solid #10b981;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

st.title("🧮 Scientific Function Calculator")
st.write("Perform advanced mathematical sequences and baseline matrix conversions.")

# --- 2. OPERATION CATEGORY SELECTION ---
operation_type = st.selectbox(
    "Choose Calculator Mode:",
    ["Basic Arithmetic", "Trigonometry", "Logarithms & Exponents", "Powers & Roots"]
)

st.markdown("---")

# --- 3. DYNAMIC INTERFACE CONFIGURATION ---
result = None
error_message = None

if operation_type == "Basic Arithmetic":
    col1, col2 = st.columns(2)
    with col1:
        num1 = st.number_input("Enter First Value (x):", value=0.0, format="%f")
    with col2:
        num2 = st.number_input("Enter Second Value (y):", value=0.0, format="%f")
        
    op = st.radio("Select Operation:", ["Addition (+)", "Subtraction (-)", "Multiplication (×)", "Division (÷)"], horizontal=True)
    
    if st.button("Calculate Arithmetic"):
        if op == "Addition (+)":
            result = num1 + num2
        elif op == "Subtraction (-)":
            result = num1 - num2
        elif op == "Multiplication (×)":
            result = num1 * num2
        elif op == "Division (÷)":
            if num2 != 0:
                result = num1 / num2
            else:
                error_message = "Math Error: Cannot divide by absolute zero."

elif operation_type == "Trigonometry":
    num = st.number_input("Enter Angle Value (x):", value=0.0, format="%f")
    unit = st.radio("Angle Mode:", ["Degrees", "Radians"], horizontal=True)
    op = st.radio("Select Function:", ["Sine (sin)", "Cosine (cos)", "Tangent (tan)"], horizontal=True)
    
    if st.button("Calculate Trig Function"):
        # Convert to radians if user selects degrees
        calc_num = math.radians(num) if unit == "Degrees" else num
        
        if op == "Sine (sin)":
            result = math.sin(calc_num)
        elif op == "Cosine (cos)":
            result = math.cos(calc_num)
        elif op == "Tangent (tan)":
            # Check for tan undefined points (e.g., 90 degrees)
            if unit == "Degrees" and (abs(num) % 180 == 90):
                error_message = "Math Error: Tangent is undefined at this angle."
            else:
                result = math.tan(calc_num)

elif operation_type == "Logarithms & Exponents":
    num = st.number_input("Enter Value (x):", value=1.0, format="%f")
    op = st.radio("Select Function:", ["Natural Log (ln)", "Base-10 Log (log10)", "Exponential (e^x)"], horizontal=True)
    
    if st.button("Calculate Log/Exp"):
        if op == "Natural Log (ln)":
            if num > 0:
                result = math.log(num)
            else:
                error_message = "Math Error: Logarithm domain must be strictly greater than zero."
        elif op == "Base-10 Log (log10)":
            if num > 0:
                result = math.log10(num)
            else:
                error_message = "Math Error: Logarithm domain must be strictly greater than zero."
        elif op == "Exponential (e^x)":
            try:
                result = math.exp(num)
            except OverflowError:
                error_message = "Math Error: Result value is too large (Overflow)."

elif operation_type == "Powers & Roots":
    col1, col2 = st.columns(2)
    with col1:
        base = st.number_input("Base Value (x):", value=0.0, format="%f")
    with col2:
        exponent = st.number_input("Exponent / Power / Root Level (y):", value=2.0, format="%f")
        
    op = st.radio("Select Function:", ["Raise to Power (x^y)", "Square Root (√x)", "Custom Root (y√x)"], horizontal=True)
    
    if st.button("Calculate Power/Root"):
        if op == "Raise to Power (x^y)":
            try:
                result = math.pow(base, exponent)
            except OverflowError:
                error_message = "Math Error: Result value is too large."
            except ValueError:
                error_message = "Math Error: Incompatible negative base power operations."
        elif op == "Square Root (√x)":
            if base >= 0:
                result = math.sqrt(base)
            else:
                error_message = "Math Error: Cannot extract square roots from negative figures."
        elif op == "Custom Root (y√x)":
            if base >= 0 and exponent != 0:
                result = math.pow(base, 1.0 / exponent)
            elif exponent == 0:
                error_message = "Math Error: Root value index cannot be zero."
            else:
                error_message = "Math Error: Negative base conversion root limits."

# --- 4. RENDER CALCULATION DISPLAY OUTPUT ---
st.markdown("---")
st.subheader("📟 Calculator Display")

if result is not None:
    st.markdown(f"""
    <div class="calc-display">
        <span style="color:#94a3b8; font-size:14px; font-weight:bold; text-transform:uppercase;">Output Solution</span>
        <h2 style="margin:5px 0 0 0; color:#10b981; font-family: monospace;">{result}</h2>
    </div>
    """, unsafe_allow_html=True)
elif error_message:
    st.error(error_message)
else:
    st.info("Input your target numbers above and click the calculation execution button to output metrics.")

# Useful scientific constants reference in sidebar panel
with st.sidebar:
    st.subheader("📚 Scientific Constants")
    st.code(f"π (Pi) ≈ {math.pi}")
    st.code(f"e (Euler's Number) ≈ {math.e}")
