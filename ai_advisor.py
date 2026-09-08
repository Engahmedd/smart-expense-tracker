class AIAdvisor:
    def __init__(self, api_key: str = None):
        pass  # مش محتاجين أي API Key خالص

    def analyze_expenses(self, transactions_list):
        if not transactions_list:
            return "لا توجد معاملات مالية لتحليلها حتى الآن."

        total_income = 0.0
        total_expense = 0.0
        categories = {}

        # تحليل المعاملات من قاعدة البيانات
        for row in transactions_list:
            # row: (id, amount, category, type, date)
            amount = float(row[1])
            category = row[2]
            trans_type = row[3]

            if trans_type == "Income":
                total_income += amount
            elif trans_type == "Expense":
                total_expense += amount
                categories[category] = categories.get(category, 0.0) + amount

        # حساب الصافي
        net_balance = total_income - total_expense

        # بناء التقرير النصي
        report = []
        report.append("### 📊 التقرير والتحليل المالي الذكي:\n")
        report.append(f"- **إجمالي الدخل:** {total_income:,.2f} ج.م")
        report.append(f"- **إجمالي المصاريف:** {total_expense:,.2f} ج.م")
        report.append(f"- **الرصيد المتبقي:** {net_balance:,.2f} ج.م\n")

        # معرفة أعلى فئة صرف
        if categories:
            top_category = max(categories, key=categories.get)
            top_amount = categories[top_category]
            report.append(f"🔍 **أعلى فئة استهلاكاً للمال:** `{top_category}` بمبلغ **{top_amount:,.2f} ج.م**.\n")

        # توليد النصائح المخصصة
        report.append("💡 **نصائح المستشار المالي:**")

        if total_income > 0:
            expense_ratio = (total_expense / total_income) * 100
            report.append(f"- أنت تصرف حالياً حوالي **{expense_ratio:.1f}%** من إجمالي دخلك.")

            if expense_ratio > 80:
                report.append("⚠️ **تحذير:** معدل إنفاقك مرتفع جداً ويفوق 80% من دخلك. حاول الحد من المصاريف غير الضرورية في الأيام القادمة.")
            elif expense_ratio > 50:
                report.append("👍 **وضع متوسط:** إنفاقك في الحدود المقبولة، ولكن حاول تخصيص 20% للادخار أو الميزانيات الطارئة.")
            else:
                report.append("🎉 **أداء ممتاز:** معدل أدخارك عالي جداً وتدير مصاريفك بحكمة ممتازة!")
        else:
            report.append("- لم تقم بإضافة أي دخل بعد. يُفضل تسجيل الدخل لتحديد نسبة الأمان المالي بدقة.")

        if categories:
            report.append(f"- حاول وضع حد أقصى (Budget) لفئة **'{top_category}'** من قائمة إدارة الميزانية لضبط الإنفاق فيها.")

        return "\n".join(report)
