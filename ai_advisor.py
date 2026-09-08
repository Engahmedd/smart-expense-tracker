import requests

class AIAdvisor:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def analyze_expenses(self, transactions_list):
        if not transactions_list:
            return "لا توجد معاملات مالية لتحليلها حتى الآن."

        prompt_text = f"""
        أنت مستشار مالي ذكي وخبير. قم بتحليل معاملات المستخدم المالية التالية وتقديم تقرير مالي ونصائح باللغة العربية:
        البيانات: {transactions_list}

        المطلوب منك:
        1. ملخص تحليلي دقيق لإجمالي المصاريف والدخل.
        2. أكثر الفئات استهلاكاً للمال.
        3. تقديم 3 نصائح مالية عملية ومخصصة للتوفير والادخار بناءً على الأرقام.
        """

        # استخدام REST API مع Gemini 1.5 Flash
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        
        # التوثيق باستخدام Bearer Token الخاص بمفاتيح AQ
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt_text}]
                }
            ]
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            res_json = response.json()

            if response.status_code == 200:
                return res_json['candidates'][0]['content']['parts'][0]['text']
            else:
                error_msg = res_json.get('error', {}).get('message', 'خطأ غير معروف')
                return f"حدث خطأ من السيرفر ({response.status_code}): {error_msg}"

        except Exception as e:
            return f"حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {str(e)}"
