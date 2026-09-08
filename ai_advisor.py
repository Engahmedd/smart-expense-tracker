from google import genai

class AIAdvisor:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

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
            # تم التحديث إلى الموديل المطلوب gemini-3.6-flash
            response = self.client.models.generate_content(
                model='gemini-3.6-flash',
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {str(e)}"