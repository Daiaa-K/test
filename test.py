import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import locale

# إعدادات اللغة والعملة للسعودية
try:
    locale.setlocale(locale.LC_ALL, 'ar_SA.UTF-8')  # Linux/Mac
except:
    try:
        locale.setlocale(locale.LC_ALL, 'Arabic_Saudi Arabia.1256')  # Windows
    except:
        locale.setlocale(locale.LC_ALL, '')  # fallback to default locale

def format_currency(amount):
    try:
        return locale.currency(amount, symbol=True, grouping=True)
    except:
        return f"ر.س {amount:,.2f}"

def main():
    st.set_page_config(layout="wide")

    # تنسيق واجهة عربية
    st.markdown(
        """
        <style>
        body, .main, .stApp {
            direction: rtl;
            text-align: right;
            font-family: 'Cairo', sans-serif;
        }
        .main-content {
            max-width: 70%;
            margin: auto;
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .intro-text {
            font-size: 28px;
            font-weight: bold;
            color: #4A90E2;
            text-align: center;
            margin-bottom: 20px;
        }
        .stButton>button {
            background-color: #4A90E2;
            color: white;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="main-content">', unsafe_allow_html=True)

    st.markdown('<div class="intro-text">حاسبة التقاعد (السعودية)</div>', unsafe_allow_html=True)
    st.write("احسب كم تحتاج لتوفير حتى التقاعد بناءً على دخلك ونفقاتك.")

    # مصادر الدخل
    st.header("مصادر الدخل")
    income_sources = ["راتب شهري", "دخل إضافي", "عمل حر", "استثمار"]
    income_data = {}

    cols = st.columns(2)
    for i, source in enumerate(income_sources):
        with cols[i % 2]:
            st.subheader(source)
            frequency = st.selectbox(f"تكرار {source}", ["لا شيء", "شهري", "ربع سنوي", "سنوي"], key=source)
            amount = st.number_input(f"المبلغ ({frequency})", min_value=0.0, step=0.01, key=f"{source}_amount")
            if frequency != "لا شيء":
                income_data[source] = (frequency, amount)

    # إجمالي الدخل الشهري
    total_monthly_income = 0
    for _, (frequency, amount) in income_data.items():
        if frequency == "شهري":
            total_monthly_income += amount
        elif frequency == "ربع سنوي":
            total_monthly_income += amount / 3
        elif frequency == "سنوي":
            total_monthly_income += amount / 12

    st.write(f"📊 إجمالي الدخل الشهري: *{format_currency(total_monthly_income)}*")

    # النفقات الشهرية
    st.header("النفقات الشهرية")
    monthly_expenses = st.number_input("إجمالي المصاريف الشهرية", min_value=0.0, step=0.01)

    # أهداف التقاعد
    st.header("أهداف التقاعد")
    col1, col2 = st.columns(2)
    with col1:
        current_age = st.number_input("عمرك الحالي", min_value=0, step=1)
    with col2:
        retirement_age = st.number_input("العمر المتوقع للتقاعد", min_value=current_age + 1, step=1)
    retirement_goal = st.number_input("الهدف المالي عند التقاعد (ر.س)", min_value=0.0, step=0.01)

    # حساب الادخار
    years_left = retirement_age - current_age
    months_left = years_left * 12
    expected_savings = (total_monthly_income - monthly_expenses) * months_left
    monthly_savings_required = (retirement_goal - expected_savings) / months_left if months_left > 0 else 0

    # ملخص
    st.header("الملخص")
    summary_df = pd.DataFrame({
        "الوصف": [
            "إجمالي الدخل الشهري",
            "النفقات الشهرية",
            "العمر الحالي",
            "عمر التقاعد",
            "سنوات التقاعد المتبقية",
            "الادخار الشهري المطلوب"
        ],
        "القيمة": [
            format_currency(total_monthly_income),
            format_currency(monthly_expenses),
            f"{current_age} سنة",
            f"{retirement_age} سنة",
            f"{years_left} سنة",
            format_currency(monthly_savings_required)
        ]
    })

    st.table(summary_df)

    # رسم بياني
    st.header("الرسم البياني للادخار المتوقع")
    months = list(range(1, months_left + 1))
    cumulative_savings = [(total_monthly_income - monthly_expenses) * month for month in months]
    df = pd.DataFrame({'شهر': months, 'الادخار التراكمي': cumulative_savings})

    plt.figure(figsize=(10, 5))
    plt.plot(df['شهر'], df['الادخار التراكمي'], label="الادخار", color='green')
    plt.axhline(y=retirement_goal, color='red', linestyle='--', label="الهدف")
    plt.title("خطة الادخار حتى التقاعد")
    plt.xlabel("الشهر")
    plt.ylabel("الادخار (ر.س)")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "_main_":
    main()