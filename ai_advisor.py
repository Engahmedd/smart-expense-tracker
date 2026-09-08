from google import genai

class AIAdvisor:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

    def analyze_expenses(self, transactions_list):
        if not transactions_list:
            return "لا توجد معاملات مالية لتحليلها حتى الآن."

        prompt = f"""
        أنت مستشار مالي ذكي وخبير. قم بتحليل معاملات المستخدم المالية التالية وتقديم نصائح باللغة العربية:
        البيانات: {transactions_list}

        المطلوب:
        1. ملخص سريع لإجمالي المصاريف والدخل.
        2. أكثر الفئات استهلاكاً للمال مع تحليل بسيط.
        3. 3 نصائح عملية ومخصصة للتوفير بناءً على البيانات.
        """
        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {str(e)}"
