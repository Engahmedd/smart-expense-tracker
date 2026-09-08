from google import genai

class AIAdvisor:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

    def analyze_expenses(self, transactions_list):
        if not transactions_list:
            return "لا توجد معاملات مالية لتحليلها حتى الآن."

        prompt = f"""
        أنت مستشار مالي ذكي وخبير. قم بتحليل معاملات المستخدم المالية التالية وتقديم تقرير مالي ونصائح باللغة العربية:
        البيانات: {transactions_list}

        المطلوب منك:
        1. ملخص تحليلي دقيق لإجمالي المصاريف والدخل.
        2. أكثر الفئات استهلاكاً للمال مع توضيح بسيط.
        3. تقديم 3 نصائح مالية عملية ومخصصة جداً للتوفير والادخار بناءً على أرقام المعاملات المرفقة.
        """
        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {str(e)}"
