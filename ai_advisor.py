import google.generativeai as genai

class AIAdvisor:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def analyze_expenses(self, transactions_list):
        if not transactions_list:
            return "لا توجد معاملات مالية لتحليلها حتى الآن."

        prompt = f"""
        أنت مستشار مالي ذكي. قم بتحليل معاملات المستخدم التالية من قاعدة البيانات وتقديم نصائح باللغة العربية:
        البيانات: {transactions_list}

        المطلوب:
        1. ملخص سريع لإجمالي المصاريف والدخل.
        2. أكثر الفئات استهلاكاً للمال.
        3. نصيحتان عمليتان للتوفير.
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {str(e)}"
