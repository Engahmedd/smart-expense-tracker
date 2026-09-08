import streamlit as st
import pandas as pd
from datetime import date
from database import Database
from model import User, Transaction, Budget
from ai_advisor import AIAdvisor

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="مدير المصاريف الذكي",
    page_icon="💰",
    layout="wide"
)

# 2. تهيئة اتصال قاعدة البيانات والـ AI
@st.cache_resource
def init_db():
    db = Database()
    db.create_tables()
    return db

db = init_db()

# ضع مفتاح Gemini API الخاص بك هنا
GEMINI_API_KEY = "AQ.Ab8RN6I_6VY0KoaV15OAXA0O-sm7QyTYkgBkjaoxi7LgBcOcGg"
ai_advisor = AIAdvisor(api_key=GEMINI_API_KEY)

# 3. إدارة جلسة المستخدم (Session State)
if "logged_user" not in st.session_state:
    st.session_state.logged_user = None

# ==========================================
# شاشة تسجيل الدخول وإنشاء الحساب
# ==========================================
if st.session_state.logged_user is None:
    st.title("💰 نظام إدارة المصاريف الشخصية الذكي")
    
    tab1, tab2 = st.tabs(["تسجيل الدخول", "إنشاء حساب جديد"])

    with tab1:
        st.subheader("تسجيل الدخول")
        login_user = st.text_input("اسم المستخدم", key="l_user")
        login_pass = st.text_input("كلمة المرور", type="password", key="l_pass")
        
        if st.button("دخول", type="primary"):
            if login_user and login_pass:
                user = User.login(db, login_user, login_pass)
                if user:
                    st.session_state.logged_user = user
                    st.success(f"أهلاً بك {user.username}!")
                    st.rerun()
                else:
                    st.error("اسم المستخدم أو كلمة المرور غير صحيحة!")
            else:
                st.warning("يرجى إدخال اسم المستخدم وكلمة المرور.")

    with tab2:
        st.subheader("إنشاء حساب جديد")
        reg_user = st.text_input("اسم المستخدم", key="r_user")
        reg_email = st.text_input("البريد الإلكتروني", key="r_email")
        reg_pass = st.text_input("كلمة المرور", type="password", key="r_pass")
        
        if st.button("تسجيل"):
            if reg_user and reg_pass:
                try:
                    new_user = User(None, reg_user, reg_email, reg_pass)
                    new_user.save(db)
                    st.success("تم إنشاء الحساب بنجاح! يمكنك الآن تسجيل الدخول.")
                except Exception as e:
                    st.error("حدث خطأ أثناء التسجيل، قد يكون اسم المستخدم مكرراً.")
            else:
                st.warning("يرجى ملء الحقول المطلوبة (اسم المستخدم وكلمة المرور).")

# ==========================================
# الشاشة الرئيسية بعد تسجيل الدخول
# ==========================================
else:
    current_user = st.session_state.logged_user

    # القائمة الجانبية
    st.sidebar.title(f"مرحباً، {current_user.username} 👋")
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.logged_user = None
        st.rerun()

    menu = st.sidebar.radio(
        "القائمة الرئيسية",
        ["لوحة التحكم", "إضافة معاملة", "إدارة الميزانية", "المستشار الذكي AI"]
    )

    # ------------------------------------------
    # 1. لوحة التحكم (Dashboard)
    # ------------------------------------------
    if menu == "لوحة التحكم":
        st.title("📊 لوحة التحكم والإحصائيات")
        
        raw_transactions = Transaction.get_user_transactions(db, current_user.id)
        
        if raw_transactions:
            # إنشاء DataFrame تلقائياً والتوافق مع أي عدد من الأعمدة
            df = pd.DataFrame(raw_transactions)
            
            # إعادة تسمية الأعمدة بناءً على ترتيبها في الاستعلام لتجنب أي تعارض
            cols_count = df.shape[1]
            if cols_count >= 6:
                df.columns = ["ID", "المبلغ", "التصنيف", "النوع", "التاريخ", "ملاحظات"][:cols_count]
            elif cols_count == 5:
                df.columns = ["المبلغ", "التصنيف", "النوع", "التاريخ", "ملاحظات"]

            df["المبلغ"] = df["المبلغ"].astype(float)

            # الحسابات الإجمالية
            total_income = df[df["النوع"] == "Income"]["المبلغ"].sum()
            total_expense = df[df["النوع"] == "Expense"]["المبلغ"].sum()
            net_balance = total_income - total_expense

            c1, c2, c3 = st.columns(3)
            c1.metric("إجمالي الدخل", f"{total_income:,.2f} ج.م")
            c2.metric("إجمالي المصاريف", f"{total_expense:,.2f} ج.م")
            c3.metric("الرصيد الصافي", f"{net_balance:,.2f} ج.م")

            st.divider()

            col_chart, col_table = st.columns([1, 1])

            with col_chart:
                st.subheader("المصاريف حسب الفئة")
                exp_df = df[df["النوع"] == "Expense"]
                if not exp_df.empty:
                    chart_data = exp_df.groupby("التصنيف")["المبلغ"].sum()
                    st.bar_chart(chart_data)
                else:
                    st.info("لا توجد مصاريف مسجلة حتى الآن.")

            with col_table:
                st.subheader("أحدث المعاملات")
                display_cols = [col for col in ["المبلغ", "التصنيف", "النوع", "التاريخ", "ملاحظات"] if col in df.columns]
                st.dataframe(df[display_cols], use_container_width=True)

        else:
            st.info("لا توجد معاملات مسجلة بعد. استخدم قائمة 'إضافة معاملة' للبدء.")

    # ------------------------------------------
    # 2. إضافة معاملة جديدة
    # ------------------------------------------
    elif menu == "إضافة معاملة":
        st.title("➕ إضافة معاملة جديدة")

        trans_type = st.selectbox("نوع المعاملة", ["Expense", "Income"], format_func=lambda x: "مصروف" if x == "Expense" else "دخل")
        amount = st.number_input("المبلغ", min_value=1.0, step=10.0)
        category = st.selectbox("الفئة", ["طعام", "مواصلات", "تسوق", "فواتير", "ترفيه", "صحة", "راتب", "أخرى"])
        trans_date = st.date_input("التاريخ", value=date.today())
        note = st.text_input("ملاحظات / وصف")

        if st.button("حفظ المعاملة", type="primary"):
            new_trans = Transaction(
                user_id=current_user.id,
                amount=amount,
                category=category,
                trans_type=trans_type,
                date=trans_date.strftime("%Y-%m-%d"),
                note=note
            )
            new_trans.save(db)
            st.success("تم حفظ المعاملة بنجاح!")

            # فحص الميزانية لو كانت المعاملة مصروف
            if trans_type == "Expense":
                raw_trans = Transaction.get_user_transactions(db, current_user.id)
                if raw_trans:
                    df = pd.DataFrame(raw_trans)
                    cols_count = df.shape[1]
                    if cols_count >= 6:
                        df.columns = ["ID", "المبلغ", "التصنيف", "النوع", "التاريخ", "ملاحظات"][:cols_count]
                    elif cols_count == 5:
                        df.columns = ["المبلغ", "التصنيف", "النوع", "التاريخ", "ملاحظات"]

                    df["المبلغ"] = df["المبلغ"].astype(float)
                    current_spending = df[(df["التصنيف"] == category) & (df["النوع"] == "Expense")]["المبلغ"].sum()

                    status = Budget.check_status(db, current_user.id, category, current_spending)
                    if "Over Budget" in status:
                        st.error(f"⚠️ تنبيه: {status}")
                    elif "Within Limit" in status:
                        st.info(f"ℹ️ حالة الميزانية: {status}")

    # ------------------------------------------
    # 3. إدارة الميزانية
    # ------------------------------------------
    elif menu == "إدارة الميزانية":
        st.title("🎯 تحديد ميزانية شهرية للفئات")

        category = st.selectbox("اختر الفئة", ["طعام", "مواصلات", "تسوق", "فواتير", "ترفيه", "صحة"])
        limit = st.number_input("الحد الأقصى المسموح به شهرياً", min_value=100.0, step=500.0)

        if st.button("حفظ الميزانية", type="primary"):
            b = Budget(user_id=current_user.id, category=category, monthly_limit=limit)
            b.save(db)
            st.success(f"تم تحديث الميزانية للفئة '{category}' بنجاح!")

    # ------------------------------------------
    # 4. المستشار الذكي AI
    # ------------------------------------------
    elif menu == "المستشار الذكي AI":
        st.title("🤖 المستشار المالي الذكي")
        st.write("احصل على تحليل مخصص ورؤى ذكية بناءً على سجل معاملاتك المسجلة.")

        if st.button("تحليل بياناتي الآن", type="primary"):
            raw_trans = Transaction.get_user_transactions(db, current_user.id)
            if raw_trans:
                with st.spinner("جاري استخراج البيانات وتحليلها عبر الذكاء الاصطناعي..."):
                    response = ai_advisor.analyze_expenses(raw_trans)
                    st.markdown("### 📋 التقرير والنصائح المالية:")
                    st.write(response)
            else:
                st.warning("أضف بعض المعاملات أولاً ليتمكن الذكاء الاصطناعي من تحليلها.")
