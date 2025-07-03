import streamlit as st
from openai import OpenAI
import requests
import urllib.parse
import re
from datetime import datetime

st.set_page_config(
    page_title="AI Powered Pro Travel Planner with Timothy",
    page_icon="✈️",
    layout="wide"
)

LANGUAGES = {
    "한국어 🇰🇷": {
        "title": "AI Powered Pro Travel Planner with Timothy",
        "tagline": "AI와 함께, 당신만을 위한 완벽한 여행을 계획하세요.",
        "city_label": "어디로 떠나시나요?",
        "city_placeholder": "도시 이름 입력 (예: 파리)",
        "date_label": "언제 출발하시나요?",
        "button_text": "✈️ 나만의 여행 계획 만들기",
        "sidebar_header": "🔑 API 키 설정",
        "openai_key_label": "OpenAI API 키 (필수)",
        "unsplash_key_label": "Unsplash Access Key (선택)",
        "api_info_header": "API 키 안내",
        "api_info_text": """
        **1. OpenAI API 키 (필수)**: 여행 계획을 생성하는 AI를 이용하기 위해 필요합니다.
        * [OpenAI API 키 발급받기](https://platform.openai.com/api-keys)

        **2. Unsplash Access Key (선택)**: 여행지의 실제 사진을 불러오려면 입력해주세요.
        * [Unsplash Access Key 발급받기](https://unsplash.com/developers)

        ---
        입력하신 키는 페이지를 새로고침하면 사라지며, **어디에도 저장되지 않으니 안심하세요.** 😊
        """,
        "error_openai_key": "사이드바에 OpenAI API 키를 먼저 입력해주세요.",
        "error_city": "도시 이름을 입력해주세요.",
        "spinner_photo": "의 실제 사진을 찾는 중... 📸",
        "spinner_plan": "전문가가 여행 칼럼을 작성하고 있습니다... ✍️",
        "summary_title": "오늘의 여행 하이라이트",
        "weather_title": "날씨 및 옷차림 팁",
        "address_keyword": "주소",
        "map_link_text": "[지도에서 보기 🗺️]",
        "prompt_persona": "당신은 세계적인 여행 매거진 **'Lonely Planet'의 수석 여행 칼럼니스트**입니다.",
        "prompt_instruction_summary": "글의 가장 첫 부분에 **[{summary_title}]** 섹션을 만들어, 그날의 전체 동선을 시간 순서대로 요약하여 제시해야 합니다.",
        "prompt_instruction_weather": "사용자가 여행할 **{month}월**을 기준으로, **[{weather_title}]** 섹션을 추가해주세요. 이 섹션에는 해당 월의 평균 기온, 강수량 등 과거 날씨 정보와 '두꺼운 옷을 챙기세요' 또는 '우산을 준비하세요' 같은 실용적인 옷차림 팁을 반드시 포함해야 합니다.",
        "prompt_instruction_address": "추천하는 모든 장소에 대해, 반드시 웹 검색을 통해 **실제 존재하는 정확한 주소**를 찾아 `({address_keyword}: ...)` 형식으로 명시해야 합니다.",
        "prompt_structure_title": "### **{city}에서 보내는 완벽한 하루: [매력적인 전체 타이틀]**",
        "prompt_morning": "오전 (Morning 🌅)",
        "prompt_afternoon": "오후 (Afternoon ☀️)",
        "prompt_evening": "저녁 (Evening 🌙)",
        "prompt_activity": "📌 핵심 활동",
        "prompt_tip": "🤫 시크릿 팁",
        "prompt_photo": "📸 포토 스팟",
        "prompt_restaurant": "🍽️ 추천 맛집"
    },
    "English 🇺🇸": {
        "title": "AI Powered Pro Travel Planner with Timothy",
        "tagline": "Plan your perfect trip, personalized by AI.",
        "city_label": "Where are you going?",
        "city_placeholder": "Enter a city (e.g., Paris)",
        "date_label": "When are you leaving?",
        "button_text": "✈️ Create My Travel Plan",
        "sidebar_header": "🔑 API Key Settings",
        "openai_key_label": "OpenAI API Key (Required)",
        "unsplash_key_label": "Unsplash Access Key (Optional)",
        "api_info_header": "API Key Guide",
        "api_info_text": """
        **1. OpenAI API Key (Required)**: Needed to use the AI that generates travel plans.
        * [Get your OpenAI API Key](https://platform.openai.com/api-keys)

        **2. Unsplash Access Key (Optional)**: Enter this to load real photos of your destination.
        * [Get your Unsplash Access Key](https://unsplash.com/developers)

        ---
        The keys you enter are not stored anywhere and will be gone when you refresh the page. **Your privacy is assured.** 😊
        """,
        "error_openai_key": "Please enter your OpenAI API Key in the sidebar first.",
        "error_city": "Please enter a city name.",
        "spinner_photo": "Finding real photos of",
        "spinner_plan": "A pro travel writer is crafting your itinerary...",
        "summary_title": "Today's Travel Highlights",
        "weather_title": "Weather & Wardrobe Tips",
        "address_keyword": "Address",
        "map_link_text": "[View on Map 🗺️]",
        "prompt_persona": "You are a **Senior Travel Columnist for 'Lonely Planet'** magazine.",
        "prompt_instruction_summary": "At the very beginning of the article, create a section called **[{summary_title}]** that summarizes the entire day's route chronologically.",
        "prompt_instruction_weather": "Based on the user's travel month of **{month}**, please add a section called **[{weather_title}]**. This section must include historical weather information for that month, such as average temperature and precipitation, and practical packing tips like 'pack warm clothes' or 'bring an umbrella'.",
        "prompt_instruction_address": "For every recommended place, you must find the **real, existing address** via web search and state it in the format `({address_keyword}: ...)`.",
        "prompt_structure_title": "### **A Perfect Day in {city}: [A Catchy Title]**",
        "prompt_morning": "Morning 🌅",
        "prompt_afternoon": "Afternoon ☀️",
        "prompt_evening": "Evening 🌙",
        "prompt_activity": "📌 Key Activity",
        "prompt_tip": "🤫 Secret Tip",
        "prompt_photo": "📸 Photo Spot",
        "prompt_restaurant": "🍽️ Recommended Eatery"
    },
    "日本語 🇯🇵": {
        "title": "AI Powered Pro Travel Planner with Timothy",
        "tagline": "AIと共に、あなただけの完璧な旅行を計画しましょう。",
        "city_label": "旅行先はどこですか？",
        "city_placeholder": "都市名を入力 (例: パリ)",
        "date_label": "出発日はいつですか？",
        "button_text": "✈️ 自分だけの旅行計画を作成",
        "sidebar_header": "🔑 APIキー設定",
        "openai_key_label": "OpenAI APIキー (必須)",
        "unsplash_key_label": "Unsplash Access Key (任意)",
        "api_info_header": "APIキーのご案内",
        "api_info_text": """
        **1. OpenAI APIキー (必須)**: 旅行計画を生成するAIを利用するために必要です。
        * [OpenAI APIキーを取得](https://platform.openai.com/api-keys)

        **2. Unsplash Access Key (任意)**: 旅行先の実際の写真を読み込む場合に入力してください。
        * [Unsplash Access Keyを取得](https://unsplash.com/developers)

        ---
        入力されたキーはページを更新すると消え、**どこにも保存されませんのでご安心ください。** 😊
        """,
        "error_openai_key": "まずサイドバーでOpenAI APIキーを入力してください。",
        "error_city": "都市名を入力してください。",
        "spinner_photo": "の実際の写真を探しています... 📸",
        "spinner_plan": "専門家が旅行コラムを作成しています... ✍️",
        "summary_title": "今日の旅行ハイライト",
        "weather_title": "天気と服装のヒント",
        "address_keyword": "住所",
        "map_link_text": "[地図で見る 🗺️]",
        "prompt_persona": "あなたは世界的な旅行雑誌**「Lonely Planet」の首席旅行コラムニスト**です。",
        "prompt_instruction_summary": "記事の冒頭に**[{summary_title}]**セクションを作成し、その日の全ルートを時系列で要約して提示してください。",
        "prompt_instruction_weather": "ユーザーが旅行する**{month}月**を基準に、**[{weather_title}]**セクションを追加してください。このセクションには、その月の平均気温や降水量などの過去の天気情報と、「厚着を準備してください」や「傘を用意してください」のような実用的な服装のヒントを必ず含めてください。",
        "prompt_instruction_address": "推薦するすべての場所について、必ずウェブ検索を通じて**実際に存在する正確な住所**を調べ、`({address_keyword}: ...)`の形式で明記してください。",
        "prompt_structure_title": "### **{city}で過ごす完璧な一日：[魅力的なタイトル]**",
        "prompt_morning": "午前 (Morning 🌅)",
        "prompt_afternoon": "午後 (Afternoon ☀️)",
        "prompt_evening": "夕方 (Evening 🌙)",
        "prompt_activity": "中心となる活動",
        "prompt_tip": "秘密のヒント",
        "prompt_photo": "フォトスポット",
        "prompt_restaurant": "おすすめの飲食店"
    }
}



def apply_styles():
    petal_svg = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMDAgMTAwIj48cGF0aCBkPSJNNTAsMEMyMi40LDAsMCwyMi40LDAsNTBjMCwxMy4yLDguNCwzMC42LDIxLjYsNDMuMUMzNC44LDMxLjgsNTAsMTQuMyw1MCwxNC4zcy0xNS4yLDE3LjUtMjguNCwzOC45QzguNCw2OS40LDAsODQuOCwwLDEwMEw1MCwxMDBjMjcuNiwwLDUwLTIyLjQsNTAtNTBTMzc3LjYsMCw1MCwwWiIgZmlsbD0iI2ZmYjZkYiIvPjwvc3ZnPg=="

    st.markdown(f"""
    <style>
        .lang_selector {{ display: flex; justify-content: center; margin-bottom: 2rem; gap: 0.5rem; }}
        .stRadio > div {{ flex-direction: row; }}
        .stButton>button {{ border: none; border-radius: 8px; color: white; background: linear-gradient(to right, #E61E4D 0%, #E31C5F 50%, #D70466 100%); width: 100%; height: 50px; font-size: 16px; font-weight: 600; }}
        .stTextInput>label, .stDateInput>label {{ font-size: 16px; font-weight: 600; color: #444444; }}
        .hero_image img {{ border-radius: 12px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); }}
        a {{ color: #007bff; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}

        .plan-theme-container {{
            position: relative;
            padding: 2rem;
            border-radius: 16px;
            background: linear-gradient(135deg, #87CEEB 0%, #B0E0E6 100%);
            overflow: hidden;
            margin-top: 2rem;
        }}
        
        .plan-content {{
            position: relative;
            z-index: 2;
        }}

        .summary_box {{ background-color: rgba(255, 255, 255, 0.8); backdrop-filter: blur(5px); border: 1px solid rgba(255, 255, 255, 0.4); border-radius: 12px; padding: 1.5rem 2rem; margin-bottom: 2rem; }}
        .summary_title {{ font-size: 20px; font-weight: 700; color: #1E3A8A; margin-bottom: 1rem; }}
        
        .travel_plan_card {{ background-color: rgba(255, 255, 255, 0.8); backdrop-filter: blur(5px); border: 1px solid rgba(255, 255, 255, 0.4); border-radius: 12px; padding: 2.5rem; }}
        .address_link {{ font-size: 14px; }}

        .falling-petal {{
            position: absolute;
            top: -10%;
            width: 20px;
            height: 20px;
            background-image: url("{petal_svg}");
            background-size: contain;
            opacity: 0.7;
            z-index: 1;
            animation: fall linear infinite;
        }}

        @keyframes fall {{
            0% {{ transform: translate(0, 0) rotateZ(0deg); }}
            100% {{ transform: translate(100px, 120vh) rotateZ(360deg); opacity: 0; }}
        }}

        .falling-petal:nth-of-type(1) {{ left: 5%; animation-duration: 15s; animation-delay: -5s; }}
        .falling-petal:nth-of-type(2) {{ left: 15%; animation-duration: 12s; animation-delay: -3s; }}
        .falling-petal:nth-of-type(3) {{ left: 25%; animation-duration: 18s; animation-delay: -8s; }}
        .falling-petal:nth-of-type(4) {{ left: 35%; animation-duration: 10s; animation-delay: -1s; }}
        .falling-petal:nth-of-type(5) {{ left: 45%; animation-duration: 20s; animation-delay: -10s; }}
        .falling-petal:nth-of-type(6) {{ left: 55%; animation-duration: 13s; animation-delay: -4s; }}
        .falling-petal:nth-of-type(7) {{ left: 65%; animation-duration: 16s; animation-delay: -6s; }}
        .falling-petal:nth-of-type(8) {{ left: 75%; animation-duration: 11s; animation-delay: -2s; }}
        .falling-petal:nth-of-type(9) {{ left: 85%; animation-duration: 19s; animation-delay: -9s; }}
        .falling-petal:nth-of-type(10) {{ left: 95%; animation-duration: 14s; animation-delay: -7s; }}

    </style>
    """, unsafe_allow_html=True)

def get_real_photo_url(query, unsplash_access_key):
    if not unsplash_access_key: return None
    try:
        response = requests.get(
            "https://api.unsplash.com/search/photos",
            params={'query': f"{query} landmark", 'per_page': 1, 'orientation': 'landscape', 'client_id': unsplash_access_key}
        )
        response.raise_for_status()
        data = response.json()
        if data['results']:
            return data['results'][0]['urls']['regular']
    except requests.exceptions.RequestException as e:
        st.warning(f"사진 검색 중 오류 발생: {e}")
    return None

def generate_Maps_link(place_name):
    encoded_place = urllib.parse.quote_plus(place_name)
    return f"https://www.google.com/maps/search/?api=1&query={encoded_place}"

def generate_travel_plan(city, date, client, lang_dict):
    month = date.month
    lang_name = st.session_state.lang_key.split(" ")[0]
    address_keyword = lang_dict['address_keyword']

    prompt = f"""
    ## Persona & Role
    {lang_dict['prompt_persona']}

    ## CRITICAL Instructions
    1.  **Language**: You must write the entire response in **{lang_name}**.
    2.  **Executive Summary**: {lang_dict['prompt_instruction_summary'].format(summary_title=lang_dict['summary_title'])}
    3.  **Weather Section**: {lang_dict['prompt_instruction_weather'].format(month=month, weather_title=lang_dict['weather_title'])}
    4.  **Address**: {lang_dict['prompt_instruction_address'].format(address_keyword=address_keyword)}
    5.  **Structure**: You must follow the Article Structure below precisely.

    ## Article Structure

    **[{lang_dict['summary_title']}]**
    * {lang_dict['prompt_morning'].split(" ")[0]}: [Place 1] → [Place 2]
    * {lang_dict['prompt_afternoon'].split(" ")[0]}: [Place 3] → [Place 4]
    * {lang_dict['prompt_evening'].split(" ")[0]}: [Place 5] → [Place 6]
    * Key Theme: A perfect day experiencing the [theme] of {city}.

    ---

    {lang_dict['prompt_structure_title'].format(city=city)}

    #### **{lang_dict['weather_title']}**
    * [Provide weather and packing tips here]

    #### **{lang_dict['prompt_morning']}**
    * `[{lang_dict['prompt_activity']}]`: Activity Name ({address_keyword}: Exact Address)
    * `[{lang_dict['prompt_tip']}]`: A secret tip.
    * `[{lang_dict['prompt_photo']}]`: Photo Spot Name ({address_keyword}: Exact Address)
    * `[{lang_dict['prompt_restaurant']}]`: Restaurant Name - Signature Dish ({address_keyword}: Exact Address)

    #### **{lang_dict['prompt_afternoon']}**
    * `[{lang_dict['prompt_activity']}]`: ... (Follow the same structure)

    #### **{lang_dict['prompt_evening']}**
    * `[{lang_dict['prompt_activity']}]`: ... (Follow the same structure)
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"여행 계획 생성 중 오류가 발생했습니다: {e}")
        return None

def process_and_display_plan(plan_text, lang_dict):
    address_keyword = lang_dict['address_keyword']
    map_link_text = lang_dict['map_link_text']
    
    pattern = re.compile(f"([\\w\\s\\d가-힣'·,.-]+)\\s*\\({re.escape(address_keyword)}:\\s*([^)]+)\\)")

    def replace_with_link(match):
        place_name = match.group(1).strip()
        address = match.group(2).strip()
        maps_link = generate_Maps_link(f"{place_name}, {address}")
        return f"<strong>{place_name}</strong><br><span class='address_link'>({address_keyword}: {address}) <a href='{maps_link}' target='_blank'>{map_link_text}</a></span>"

    formatted_text = plan_text.replace('\n', '<br>')
    formatted_text = re.sub(pattern, replace_with_link, formatted_text)
    
    formatted_text = re.sub(r'###\s*(.*?)(?=<br>)', r'<h3>\1</h3>', formatted_text)
    formatted_text = re.sub(r'####\s*(.*?)(?=<br>)', r'<h4>\1</h4>', formatted_text)

    for item in ['📌', '🤫', '📸', '🍽️', '🌡️', '✨']:
        formatted_text = formatted_text.replace(f'[{item}', f"<br><strong>[{item}")

    summary_html = ""
    main_content_html = ""
    summary_title_keyword = lang_dict['summary_title']
    if f"[{summary_title_keyword}]" in formatted_text:
        parts = formatted_text.split(f"[{summary_title_keyword}]", 1)
        if len(parts) > 1:
            summary_part = parts[1].split('---')[0]
            main_content_part = parts[1].split('---', 1)[1] if '---' in parts[1] else ''
            
            summary_html = f'<div class="summary_box"><div class="summary_title">✨ {summary_title_keyword}</div>{summary_part}</div>'
            if main_content_part:
                main_content_html = f'<div class="travel_plan_card">{main_content_part}</div>'
    
    if not summary_html and not main_content_html:
        main_content_html = f'<div class="travel_plan_card">{formatted_text}</div>'

    petals_html = "".join(['<div class="falling-petal"></div>' for _ in range(10)])

    final_html = f"""
    <div class="plan-theme-container">
        {petals_html}
        <div class="plan-content">
            {summary_html}
            {main_content_html}
        </div>
    </div>
    """
    st.markdown(final_html, unsafe_allow_html=True)

def main():
    apply_styles()

    if 'lang_key' not in st.session_state:
        st.session_state.lang_key = "한국어 🇰🇷"

    st.markdown('<div class="lang_selector">', unsafe_allow_html=True)
    lang_options = list(LANGUAGES.keys())
    selected_lang = st.radio(
        label="Language Selection", options=lang_options,
        index=lang_options.index(st.session_state.lang_key),
        horizontal=True, label_visibility="collapsed"
    )
    if selected_lang != st.session_state.lang_key:
        st.session_state.lang_key = selected_lang
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    lang_dict = LANGUAGES[st.session_state.lang_key]

    with st.sidebar:
        st.header(lang_dict['sidebar_header'])
        openai_api_key = st.text_input(lang_dict['openai_key_label'], type="password")
        unsplash_access_key = st.text_input(lang_dict['unsplash_key_label'], type="password")
        client = OpenAI(api_key=openai_api_key) if openai_api_key else None
        st.markdown(lang_dict['api_info_text'], unsafe_allow_html=True)

    st.title(lang_dict['title'])
    st.write(lang_dict['tagline'])

    col1, col2 = st.columns([2, 1])
    with col1:
        city = st.text_input(lang_dict['city_label'], placeholder=lang_dict['city_placeholder'])
    with col2:
        travel_date = st.date_input(lang_dict['date_label'], datetime.now())

    if st.button(lang_dict['button_text']):
        if not client:
            st.error(lang_dict['error_openai_key']); st.stop()
        if not city:
            st.warning(lang_dict['error_city']); st.stop()

        with st.spinner(f"'{city}'{lang_dict['spinner_photo']}"):
            hero_image_url = get_real_photo_url(city, unsplash_access_key)
            if hero_image_url:
                 st.markdown('<div class="hero_image">', unsafe_allow_html=True)
                 st.image(hero_image_url, use_container_width=True)
                 st.markdown('</div>', unsafe_allow_html=True)

        with st.spinner(f"'{city}' {lang_dict['spinner_plan']}"):
            travel_plan_text = generate_travel_plan(city, travel_date, client, lang_dict)
            if travel_plan_text:
                process_and_display_plan(travel_plan_text, lang_dict)

if __name__ == "__main__":
    main()