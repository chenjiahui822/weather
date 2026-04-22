"""
Streamlit 天气查询应用 - 完整版
功能：实时天气、7天预报、逐小时预报、自定义主题色、多语言切换、像素小人
"""

import streamlit as st
import requests
from datetime import datetime
import pandas as pd

# ==================== 多语言字典 ====================
LANGUAGES = {
    "中文": {
        "app_title": "智能天气查询系统",
        "app_subtitle": "实时天气 | 逐小时预报 | 贴心建议 | 自定义主题色",
        "city_select": "🎯 城市选择",
        "city_placeholder": "请输入城市名称",
        "hot_cities": "🔥 热门城市",
        "search_history": "📜 搜索历史",
        "clear_history": "🗑️ 清除历史",
        "no_history": "暂无搜索历史",
        "theme_settings": "🎨 主题设置",
        "theme_mode": "界面模式",
        "light_mode": "浅色模式",
        "dark_mode": "深色模式",
        "color_scheme": "配色方案",
        "preset_theme": "预设主题",
        "custom_color": "自定义颜色",
        "custom_gradient": "自定义渐变色",
        "color_start": "起始颜色",
        "color_end": "结束颜色",
        "color_preview": "当前配色预览",
        "other_settings": "⚙️ 其他设置",
        "auto_refresh": "🔄 自动刷新（每5分钟）",
        "features": "📊 功能说明",
        "export_report": "📄 导出天气报告",
        "update_time": "更新时间",
        "temp_compare": "🌡️ 温度对比",
        "actual_temp": "实际温度",
        "feels_like": "体感温度",
        "humidity": "💧 湿度",
        "wind_speed": "🌬️ 风速",
        "pressure": "🎯 气压",
        "visibility": "👁️ 能见度",
        "uv": "☀️ 紫外线",
        "precip": "🌧️ 降水",
        "weather_status": "📝 天气状况",
        "sunrise": "🌅 日出",
        "sunset": "🌇 日落",
        "moon_phase": "🌙 月相",
        "hourly_forecast": "⏰ 逐小时预报（未来12小时）",
        "today_overview": "📊 今日概览",
        "temp_range": "今日温度范围",
        "dressing_advice": "👔 穿衣建议",
        "week_forecast": "📅 未来7天预报",
        "temp_diff": "温差",
        "query_failed": "❌ 无法获取天气数据",
        "query_tip": "💡 提示: 请检查城市名称是否正确",
        "no_city": "👆 请在左侧输入或选择城市名称开始查询",
        "footer": "🌈 智能天气查询系统 | 数据实时更新 | 支持全球城市",
        "version": "完整版 v4.0",
        "data_source": "数据来源: wttr.in",
        # 穿衣建议文本
        "advice_cold": "❄️ 天气寒冷！建议穿羽绒服、厚棉衣、围巾手套",
        "advice_cool": "🍂 天气较冷！建议穿大衣、毛衣、厚外套",
        "advice_mild": "🌸 天气凉爽！建议穿长袖、薄外套、卫衣",
        "advice_warm": "☀️ 天气舒适！建议穿短袖、衬衫、薄裤",
        "advice_hot": "🔥 天气炎热！建议穿短袖、短裤、注意防晒",
        "tip_cold": "💡 小贴士：戴好帽子手套，注意保暖防感冒",
        "tip_hot": "💡 小贴士：多喝水，避免正午长时间户外活动",
        "tip_warm": "💡 小贴士：天气舒适，适合户外活动",
        "tip_cool": "💡 小贴士：早晚温差大，记得带外套",
        # UV等级
        "uv_low": "低",
        "uv_medium": "中等",
        "uv_high": "高",
        "uv_extreme": "极高",
        # 月相
        "moon_new": "新月",
        "moon_waxing_crescent": "娥眉月",
        "moon_first_quarter": "上弦月",
        "moon_waxing_gibbous": "盈凸月",
        "moon_full": "满月",
        "moon_waning_gibbous": "亏凸月",
        "moon_third_quarter": "下弦月",
        "moon_waning_crescent": "残月",
        "moon_unknown": "未知",
        # 自动刷新
        "auto_refresh_on": "自动刷新已开启，每5分钟更新一次",
    },
    "English": {
        "app_title": "Smart Weather Query System",
        "app_subtitle": "Live Weather | Hourly Forecast | Smart Tips | Custom Theme",
        "city_select": "🎯 City Selection",
        "city_placeholder": "Enter city name",
        "hot_cities": "🔥 Hot Cities",
        "search_history": "📜 Search History",
        "clear_history": "🗑️ Clear History",
        "no_history": "No search history",
        "theme_settings": "🎨 Theme Settings",
        "theme_mode": "Theme Mode",
        "light_mode": "Light Mode",
        "dark_mode": "Dark Mode",
        "color_scheme": "Color Scheme",
        "preset_theme": "Preset Theme",
        "custom_color": "Custom Color",
        "custom_gradient": "Custom Gradient",
        "color_start": "Start Color",
        "color_end": "End Color",
        "color_preview": "Current Color Preview",
        "other_settings": "⚙️ Other Settings",
        "auto_refresh": "🔄 Auto Refresh (every 5 min)",
        "features": "📊 Features",
        "export_report": "📄 Export Report",
        "update_time": "Update Time",
        "temp_compare": "🌡️ Temperature",
        "actual_temp": "Actual",
        "feels_like": "Feels Like",
        "humidity": "💧 Humidity",
        "wind_speed": "🌬️ Wind Speed",
        "pressure": "🎯 Pressure",
        "visibility": "👁️ Visibility",
        "uv": "☀️ UV",
        "precip": "🌧️ Precip",
        "weather_status": "📝 Weather",
        "sunrise": "🌅 Sunrise",
        "sunset": "🌇 Sunset",
        "moon_phase": "🌙 Moon",
        "hourly_forecast": "⏰ Hourly Forecast (next 12h)",
        "today_overview": "📊 Today's Overview",
        "temp_range": "Today's Temperature Range",
        "dressing_advice": "👔 Dressing Advice",
        "week_forecast": "📅 7-Day Forecast",
        "temp_diff": "Temp Range",
        "query_failed": "❌ Unable to get weather data",
        "query_tip": "💡 Tip: Please check the city name",
        "no_city": "👆 Please enter or select a city on the left",
        "footer": "🌈 Smart Weather System | Real-time Data | Global Cities",
        "version": "Complete v4.0",
        "data_source": "Data source: wttr.in",
        "advice_cold": "❄️ Very cold! Wear down jacket, thick coat, scarf and gloves",
        "advice_cool": "🍂 Cool! Wear coat, sweater, thick jacket",
        "advice_mild": "🌸 Mild! Wear long sleeves, light jacket, hoodie",
        "advice_warm": "☀️ Warm! Wear short sleeves, shirt, light pants",
        "advice_hot": "🔥 Hot! Wear shorts, t-shirt, pay attention to sun protection",
        "tip_cold": "💡 Tip: Wear hat and gloves, keep warm",
        "tip_hot": "💡 Tip: Drink more water, avoid noon outdoor activities",
        "tip_warm": "💡 Tip: Perfect weather for outdoor activities",
        "tip_cool": "💡 Tip: Large temperature difference, bring a jacket",
        "uv_low": "Low",
        "uv_medium": "Medium",
        "uv_high": "High",
        "uv_extreme": "Extreme",
        "moon_new": "New Moon",
        "moon_waxing_crescent": "Waxing Crescent",
        "moon_first_quarter": "First Quarter",
        "moon_waxing_gibbous": "Waxing Gibbous",
        "moon_full": "Full Moon",
        "moon_waning_gibbous": "Waning Gibbous",
        "moon_third_quarter": "Third Quarter",
        "moon_waning_crescent": "Waning Crescent",
        "moon_unknown": "Unknown",
        "auto_refresh_on": "Auto refresh is on, updating every 5 minutes",
    },
    "日本語": {
        "app_title": "スマート天気予報システム",
        "app_subtitle": "リアルタイム天気 | 時間別予報 | おすすめアドバイス | カスタムテーマ",
        "city_select": "🎯 都市選択",
        "city_placeholder": "都市名を入力",
        "hot_cities": "🔥 人気都市",
        "search_history": "📜 検索履歴",
        "clear_history": "🗑️ 履歴を消去",
        "no_history": "検索履歴がありません",
        "theme_settings": "🎨 テーマ設定",
        "theme_mode": "テーマモード",
        "light_mode": "ライトモード",
        "dark_mode": "ダークモード",
        "color_scheme": "配色",
        "preset_theme": "プリセットテーマ",
        "custom_color": "カスタムカラー",
        "custom_gradient": "カスタムグラデーション",
        "color_start": "開始色",
        "color_end": "終了色",
        "color_preview": "現在の配色プレビュー",
        "other_settings": "⚙️ その他設定",
        "auto_refresh": "🔄 自動更新（5分ごと）",
        "features": "📊 機能",
        "export_report": "📄 レポート出力",
        "update_time": "更新時間",
        "temp_compare": "🌡️ 気温比較",
        "actual_temp": "実際の気温",
        "feels_like": "体感温度",
        "humidity": "💧 湿度",
        "wind_speed": "🌬️ 風速",
        "pressure": "🎯 気圧",
        "visibility": "👁️ 視程",
        "uv": "☀️ 紫外線",
        "precip": "🌧️ 降水量",
        "weather_status": "📝 天気状況",
        "sunrise": "🌅 日の出",
        "sunset": "🌇 日の入り",
        "moon_phase": "🌙 月齢",
        "hourly_forecast": "⏰ 時間別予報（未来12時間）",
        "today_overview": "📊 今日の概要",
        "temp_range": "今日の気温範囲",
        "dressing_advice": "👔 服装アドバイス",
        "week_forecast": "📅 7日間予報",
        "temp_diff": "気温差",
        "query_failed": "❌ 天気データを取得できません",
        "query_tip": "💡 ヒント: 都市名を確認してください",
        "no_city": "👆 左側で都市を入力または選択してください",
        "footer": "🌈 スマート天気システム | リアルタイムデータ | 世界中の都市に対応",
        "version": "完全版 v4.0",
        "data_source": "データソース: wttr.in",
        "advice_cold": "❄️ 非常に寒い！ダウンジャケット、厚手のコート、マフラー、手袋",
        "advice_cool": "🍂 寒い！コート、セーター、厚手のジャケット",
        "advice_mild": "🌸 涼しい！長袖、軽いジャケット、パーカー",
        "advice_warm": "☀️ 快適！半袖、シャツ、薄いパンツ",
        "advice_hot": "🔥 暑い！半袖、ショートパンツ、日焼け対策を",
        "tip_cold": "💡 ヒント：帽子と手袋を着用し、暖かくしてお過ごしください",
        "tip_hot": "💡 ヒント：水分を多く摂り、正午の長時間の外出を避ける",
        "tip_warm": "💡 ヒント：屋外活動に最適な天気です",
        "tip_cool": "💡 ヒント：気温差が大きいので、上着を持参してください",
        "uv_low": "低い",
        "uv_medium": "中程度",
        "uv_high": "高い",
        "uv_extreme": "非常に高い",
        "moon_new": "新月",
        "moon_waxing_crescent": "三日月",
        "moon_first_quarter": "上弦の月",
        "moon_waxing_gibbous": "十三夜",
        "moon_full": "満月",
        "moon_waning_gibbous": "十六夜",
        "moon_third_quarter": "下弦の月",
        "moon_waning_crescent": "有明月",
        "moon_unknown": "不明",
        "auto_refresh_on": "自動更新がオンになりました（5分ごとに更新）",
    }
}

# ==================== 预设主题配色方案 ====================
PRESET_THEMES = {
    "💜 梦幻紫罗兰": ("#667eea", "#764ba2"),
    "❤️ 热情红橙": ("#FF6B6B", "#EE5A24"),
    "💚 清新薄荷": ("#4ECDC4", "#44B3A2"),
    "💛 金色阳光": ("#FFE66D", "#F7B801"),
    "💚 翡翠绿": ("#A8E6CF", "#3EAC9C"),
    "🧡 珊瑚橙": ("#FF8C42", "#F26B38"),
    "💜 皇家紫": ("#6C5CE7", "#4834D4"),
    "💙 海洋蓝": ("#00CEC9", "#00B894"),
    "❤️ 樱花粉": ("#FF7675", "#D63031"),
    "💙 天空蓝": ("#74B9FF", "#0984E3"),
    "💗 芭比粉": ("#FDA7DF", "#E84393"),
    "💚 森林绿": ("#55E6C1", "#00B894"),
    "🖤 暗夜黑": ("#2C3E50", "#1A1A2E"),
    "🤍 极简白": ("#ECF0F1", "#BDC3C7"),
}

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="智能天气查询系统",
    page_icon="🌈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== 会话状态初始化 ====================
if 'search_history' not in st.session_state:
    st.session_state.search_history = []
if 'theme_mode' not in st.session_state:
    st.session_state.theme_mode = 'light'
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = False
if 'custom_color1' not in st.session_state:
    st.session_state.custom_color1 = "#667eea"
if 'custom_color2' not in st.session_state:
    st.session_state.custom_color2 = "#764ba2"
if 'use_custom_color' not in st.session_state:
    st.session_state.use_custom_color = False
if 'language' not in st.session_state:
    st.session_state.language = "中文"


# ==================== 翻译函数 ====================
def t(key):
    """获取当前语言的翻译文本"""
    return LANGUAGES[st.session_state.language].get(key, key)


# ==================== 获取当前主题色 ====================
def get_current_colors():
    """获取当前使用的主题色"""
    if st.session_state.use_custom_color:
        return st.session_state.custom_color1, st.session_state.custom_color2
    else:
        preset_key = st.session_state.get('preset_theme', "💜 梦幻紫罗兰")
        return PRESET_THEMES.get(preset_key, ("#667eea", "#764ba2"))


# ==================== 精致像素小人组件 ====================

def get_pixel_character_css(temp):
    """使用 CSS Grid 绘制精致像素小人"""

    # 根据温度选择服装颜色和配饰
    if temp < 0:
        # 寒冷 - 蓝色羽绒服
        body_color = "#5DADE2"
        pants_color = "#2C3E50"
        hat = "🧣"
        accessory = "❄️"
        face = "🥶"
        action = "瑟瑟发抖"
        clothes_icon = "🧥"
    elif temp < 10:
        # 较冷 - 棕色大衣
        body_color = "#8B6914"
        pants_color = "#4A3728"
        hat = "🧢"
        accessory = "🧤"
        face = "😊"
        action = "快步行走"
        clothes_icon = "🧥"
    elif temp < 20:
        # 凉爽 - 绿色外套
        body_color = "#52BE80"
        pants_color = "#2E4053"
        hat = "🧢"
        accessory = "🍃"
        face = "😎"
        action = "悠闲散步"
        clothes_icon = "👕"
    elif temp < 30:
        # 舒适 - 黄色短袖
        body_color = "#F4D03F"
        pants_color = "#1B4F72"
        hat = "🕶️"
        accessory = "☀️"
        face = "😄"
        action = "神清气爽"
        clothes_icon = "👕"
    else:
        # 炎热 - 红色背心
        body_color = "#E74C3C"
        pants_color = "#1B4F72"
        hat = "🕶️"
        accessory = "🍉"
        face = "🥵"
        action = "擦汗中"
        clothes_icon = "🎽"

    # 像素小人 HTML/CSS
    character_html = f"""
    <div style="text-align: center; margin: 10px 0;">
        <style>
            @keyframes walk {{
                0%, 100% {{ transform: translateX(0px); }}
                25% {{ transform: translateX(3px); }}
                75% {{ transform: translateX(-3px); }}
            }}
            @keyframes bounce {{
                0%, 100% {{ transform: translateY(0px); }}
                50% {{ transform: translateY(-5px); }}
            }}
            @keyframes wave {{
                0%, 100% {{ transform: rotate(0deg); }}
                50% {{ transform: rotate(10deg); }}
            }}
            .pixel-container {{
                display: inline-block;
                background: linear-gradient(135deg, #667eea20 0%, #764ba220 100%);
                border-radius: 20px;
                padding: 20px;
                animation: bounce 1.5s ease-in-out infinite;
            }}
            .pixel-face {{
                font-size: 40px;
                margin-bottom: 5px;
            }}
            .pixel-body {{
                display: grid;
                grid-template-columns: repeat(5, 12px);
                grid-template-rows: repeat(5, 12px);
                gap: 1px;
                justify-content: center;
                margin: 5px auto;
            }}
            .pixel-cell {{
                width: 12px;
                height: 12px;
            }}
            .pixel-legs {{
                display: flex;
                justify-content: center;
                gap: 15px;
                margin-top: 5px;
                animation: walk 0.8s ease-in-out infinite;
            }}
            .pixel-leg {{
                width: 12px;
                height: 20px;
                background-color: {pants_color};
                border-radius: 3px;
            }}
            .pixel-accessory {{
                font-size: 24px;
                animation: wave 1s ease-in-out infinite;
                display: inline-block;
            }}
            .pixel-temp {{
                font-size: 24px;
                font-weight: bold;
                margin-top: 10px;
                color: #333;
            }}
            .pixel-action {{
                font-size: 12px;
                color: #666;
                margin-top: 8px;
            }}
        </style>

        <div class="pixel-container">
            <div class="pixel-face">{face} {clothes_icon}</div>

            <!-- 身体 (5x5 像素网格) -->
            <div class="pixel-body">
                <!-- 第1行 -->
                <div class="pixel-cell" style="background-color: {body_color};"></div>
                <div class="pixel-cell" style="background-color: {body_color};"></div>
                <div class="pixel-cell" style="background-color: {body_color};"></div>
                <div class="pixel-cell" style="background-color: {body_color};"></div>
                <div class="pixel-cell" style="background-color: {body_color};"></div>
                <!-- 第2行 -->
                <div class="pixel-cell" style="background-color: {body_color};"></div>
                <div class="pixel-cell" style="background-color: {body_color};"></div>
                <div class="pixel-cell" style="background-color: {body_color};"></div>
                <div class="pixel-cell" style="background-color: {body_color};"></div>
                <div class="pixel-cell" style="background-color: {body_color};"></div>
                <!-- 第3行 -->
                <div class="pixel-cell" style="background-color: {body_color};"></div>
                <div class="pixel-cell" style="background-color: {body_color};"></div>
                <div class="pixel-cell" style="background-color: {body_color};"></div>
                <div class="pixel-cell" style="background-color: {body_color};"></div>
                <div class="pixel-cell" style="background-color: {body_color};"></div>
                <!-- 第4行 -->
                <div class="pixel-cell" style="background-color: {body_color};"></div>
                <div class="pixel-cell" style="background-color: {body_color};"></div>
                <div class="pixel-cell" style="background-color: {body_color};"></div>
                <div class="pixel-cell" style="background-color: {body_color};"></div>
                <div class="pixel-cell" style="background-color: {body_color};"></div>
                <!-- 第5行 -->
                <div class="pixel-cell" style="background-color: {body_color};"></div>
                <div class="pixel-cell" style="background-color: {body_color};"></div>
                <div class="pixel-cell" style="background-color: {body_color};"></div>
                <div class="pixel-cell" style="background-color: {body_color};"></div>
                <div class="pixel-cell" style="background-color: {body_color};"></div>
            </div>

            <!-- 腿部 -->
            <div class="pixel-legs">
                <div class="pixel-leg"></div>
                <div class="pixel-leg"></div>
            </div>

            <!-- 配饰和动作 -->
            <div style="margin-top: 10px;">
                <span class="pixel-accessory">{accessory}</span>
                <span style="margin-left: 10px;">{hat}</span>
            </div>
            <div class="pixel-temp">{temp}°C</div>
            <div class="pixel-action">{action}</div>
        </div>
    </div>
    """
    return character_html


def get_dressing_advice_with_avatar(temp):
    """带精致像素小人的穿衣建议"""

    if temp < 0:
        advice = t("advice_cold")
        tip = t("tip_cold")
    elif temp < 10:
        advice = t("advice_cool")
        tip = t("tip_cool")
    elif temp < 20:
        advice = t("advice_mild")
        tip = t("tip_cool")
    elif temp < 30:
        advice = t("advice_warm")
        tip = t("tip_warm")
    else:
        advice = t("advice_hot")
        tip = t("tip_hot")

    # 使用两列布局
    col_left, col_right = st.columns([1, 2])

    with col_left:
        st.markdown(get_pixel_character_css(temp), unsafe_allow_html=True)

    with col_right:
        st.markdown(f"### {t('dressing_advice')}")
        st.markdown(f"{advice}")
        st.info(tip)
# ==================== 辅助函数 ====================

def get_weather_emoji(desc):
    """根据天气描述返回表情符号"""
    desc_lower = desc.lower()
    if any(word in desc_lower for word in ['雨', 'rain']):
        return "🌧️"
    elif any(word in desc_lower for word in ['雪', 'snow']):
        return "❄️"
    elif any(word in desc_lower for word in ['雷', 'thunder', 'storm']):
        return "⛈️"
    elif any(word in desc_lower for word in ['雾', 'fog', 'mist']):
        return "🌫️"
    elif any(word in desc_lower for word in ['云', 'cloud']):
        return "☁️"
    elif any(word in desc_lower for word in ['晴', 'sun', 'clear']):
        return "☀️"
    else:
        return "🌤️"


def get_moon_icon(moon_phase):
    """根据月相返回表情符号和翻译"""
    phase_lower = moon_phase.lower()
    if 'new' in phase_lower:
        return "🌑", t("moon_new")
    elif 'waxing crescent' in phase_lower:
        return "🌒", t("moon_waxing_crescent")
    elif 'first quarter' in phase_lower:
        return "🌓", t("moon_first_quarter")
    elif 'waxing gibbous' in phase_lower:
        return "🌔", t("moon_waxing_gibbous")
    elif 'full' in phase_lower:
        return "🌕", t("moon_full")
    elif 'waning gibbous' in phase_lower:
        return "🌖", t("moon_waning_gibbous")
    elif 'third quarter' in phase_lower:
        return "🌗", t("moon_third_quarter")
    elif 'waning crescent' in phase_lower:
        return "🌘", t("moon_waning_crescent")
    else:
        return "🌙", t("moon_unknown")


def get_weather_data(city):
    """获取天气数据"""
    try:
        url = f"https://wttr.in/{city}?format=j1&lang=zh"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        return response.json()
    except:
        return None


def get_hourly_forecast(data):
    """获取逐小时预报数据，时间格式转换为 HH:MM"""

    def convert_time(time_str):
        try:
            minutes = int(time_str)
            hours = minutes // 60
            return f"{hours:02d}:00"
        except:
            return time_str

    try:
        hourly = []
        for i, hour in enumerate(data['weather'][0]['hourly'][:12]):
            formatted_time = convert_time(hour['time'])
            hourly.append({
                t('时间'): formatted_time,
                t('温度'): f"{hour['tempC']}°C",
                t('feels_like'): f"{hour['FeelsLikeC']}°C",
                t('天气'): hour['weatherDesc'][0]['value'],
                t('降水'): f"{hour['chanceofrain']}%",
                t('wind_speed'): f"{hour['windspeedKmph']} km/h"
            })
        return hourly
    except:
        return []


def export_weather_report(city, current, today):
    """生成可导出的天气报告文本"""
    report = f"""
========== {t('app_title')} ==========
{t('city_select')}: {city}
{t('update_time')}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
--------------------------------
【{t('current_weather')}】
{t('温度')}: {current['temp_C']}°C ({t('feels_like')} {current['FeelsLikeC']}°C)
{t('weather_status')}: {current['weatherDesc'][0]['value']}
{t('humidity')}: {current['humidity']}%
{t('wind_speed')}: {current['windspeedKmph']} km/h {current['winddir16Point']}
{t('uv')}: {current['uvIndex']}
{t('precip')}: {current['precipMM']} mm
--------------------------------
【{t('today_overview')}】
{t('today_high')}: {today['maxtempC']}°C
{t('today_low')}: {today['mintempC']}°C
{t('sunrise')}: {today['astronomy'][0]['sunrise']}
{t('sunset')}: {today['astronomy'][0]['sunset']}
--------------------------------
{t('data_source')}
================================
"""
    return report


# ==================== 应用主题色 ====================
color1, color2 = get_current_colors()

if st.session_state.theme_mode == 'dark':
    card_bg = "rgba(30,30,50,0.95)"
    text_color = "#eee"
    sub_text_color = "#888"
else:
    card_bg = "rgba(255,255,255,0.95)"
    text_color = "#333"
    sub_text_color = "#666"

st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(135deg, {color1} 0%, {color2} 100%);
    }}
    .weather-card {{
        background: {card_bg};
        border-radius: 20px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 5px 20px rgba(0,0,0,0.2);
        color: {text_color};
    }}
    .main-header {{
        text-align: center;
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 30px;
    }}
    .metric-value {{
        font-size: 28px;
        font-weight: bold;
        text-align: center;
    }}
    .stButton button:hover {{
        transform: translateY(-2px);
        transition: all 0.3s ease;
    }}
</style>
""", unsafe_allow_html=True)

# ==================== 标题 ====================
st.markdown(f"""
<div class="main-header">
    <h1>{t('app_title')}</h1>
    <p>{t('app_subtitle')}</p>
</div>
""", unsafe_allow_html=True)

# ==================== 侧边栏 ====================
with st.sidebar:
    # 语言选择
    lang_option = st.selectbox("🌐 Language / 语言", list(LANGUAGES.keys()),
                               index=list(LANGUAGES.keys()).index(st.session_state.language))
    if lang_option != st.session_state.language:
        st.session_state.language = lang_option
        st.rerun()

    st.markdown("---")
    st.markdown(f"## {t('city_select')}")

    city = st.text_input(t('city_placeholder'), value="北京")

    st.markdown("---")
    st.markdown(f"## {t('hot_cities')}")

    hot_cities = ['北京', '上海', '广州', '深圳', '杭州', '成都', '重庆', '武汉', '西安', '南京']

    cols = st.columns(2)
    for i, city_name in enumerate(hot_cities):
        if cols[i % 2].button(city_name, key=f"btn_{city_name}", use_container_width=True):
            city = city_name
            if city not in st.session_state.search_history:
                st.session_state.search_history.insert(0, city)
                st.session_state.search_history = st.session_state.search_history[:10]
            st.rerun()

    st.markdown("---")
    st.markdown(f"## {t('search_history')}")

    if st.session_state.search_history:
        for hist_city in st.session_state.search_history[:5]:
            if st.button(f"🕐 {hist_city}", key=f"hist_{hist_city}"):
                city = hist_city
                st.rerun()
        if st.button(t('clear_history')):
            st.session_state.search_history = []
            st.rerun()
    else:
        st.caption(t('no_history'))

    st.markdown("---")
    st.markdown(f"## {t('theme_settings')}")

    theme_mode_option = st.selectbox(t('theme_mode'), [t('light_mode'), t('dark_mode')],
                                     index=0 if st.session_state.theme_mode == 'light' else 1)
    new_mode = 'light' if theme_mode_option == t('light_mode') else 'dark'
    if new_mode != st.session_state.theme_mode:
        st.session_state.theme_mode = new_mode
        st.rerun()

    st.markdown("---")
    st.markdown(f"### {t('color_scheme')}")

    color_option = st.radio(t('color_scheme'), [t('preset_theme'), t('custom_color')],
                            index=0 if not st.session_state.use_custom_color else 1)

    if color_option == t('preset_theme'):
        st.session_state.use_custom_color = False
        preset_theme = st.selectbox(t('preset_theme'), list(PRESET_THEMES.keys()),
                                    index=list(PRESET_THEMES.keys()).index(
                                        st.session_state.get('preset_theme', "💜 梦幻紫罗兰")))
        if preset_theme != st.session_state.get('preset_theme'):
            st.session_state.preset_theme = preset_theme
            st.rerun()
    else:
        st.session_state.use_custom_color = True
        st.markdown(f"### {t('custom_gradient')}")
        col1_picker, col2_picker = st.columns(2)
        with col1_picker:
            new_color1 = st.color_picker(t('color_start'), st.session_state.custom_color1)
        with col2_picker:
            new_color2 = st.color_picker(t('color_end'), st.session_state.custom_color2)

        if new_color1 != st.session_state.custom_color1 or new_color2 != st.session_state.custom_color2:
            st.session_state.custom_color1 = new_color1
            st.session_state.custom_color2 = new_color2
            st.rerun()

        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {new_color1}, {new_color2}); 
                    border-radius: 10px; padding: 10px; text-align: center; color: white; margin-top: 10px;">
            {t('color_preview')}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"## {t('other_settings')}")

    st.session_state.auto_refresh = st.checkbox(t('auto_refresh'), value=st.session_state.auto_refresh)

    st.markdown("---")
    st.markdown(f"### {t('features')}")
    st.info("""
    ✅ 实时天气查询
    ✅ 未来7天预报
    ✅ 逐小时预报
    ✅ 体感温度对比
    ✅ 月相显示
    ✅ 导出天气报告
    ✅ 深色/浅色模式
    ✅ 自定义主题色
    ✅ 多语言切换
    ✅ 会动的像素小人
    ✅ 搜索历史记录
    """)

    st.markdown("---")
    st.caption(t('data_source'))

# ==================== 自动刷新 ====================
if st.session_state.auto_refresh:
    st.toast(f"🔄 {t('auto_refresh_on')}", icon="🔄")
    st.markdown('<meta http-equiv="refresh" content="300">', unsafe_allow_html=True)

# ==================== 主要查询区域 ====================
if city:
    col1, col2 = st.columns([2, 1])

    with col1:
        with st.spinner(
                f"🌐 {t('loading') if 'loading' in LANGUAGES[st.session_state.language] else 'Loading'} {city}..."):
            data = get_weather_data(city)

            if data:
                try:
                    current = data['current_condition'][0]
                    today = data['weather'][0]

                    report = export_weather_report(city, current, today)
                    st.download_button(
                        label=t('export_report'),
                        data=report,
                        file_name=f"{city}_weather_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )

                    st.markdown(f"""
                    <div class="weather-card">
                        <h2 style="text-align:center;">{get_weather_emoji(current['weatherDesc'][0]['value'])} {city}</h2>
                        <p style="text-align:center; color: {sub_text_color};">{t('update_time')}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown('<div class="weather-card">', unsafe_allow_html=True)
                    st.markdown(f"## {t('temp_compare')}")

                    temp_col1, temp_col2 = st.columns(2)
                    with temp_col1:
                        st.markdown(f'<p class="metric-value">{current["temp_C"]}°C</p>', unsafe_allow_html=True)
                        st.caption(t('actual_temp'))
                    with temp_col2:
                        feels_like = current['FeelsLikeC']
                        feels_diff = int(feels_like) - int(current['temp_C'])
                        delta_color = "normal" if feels_diff >= 0 else "inverse"
                        st.metric(t('feels_like'), f"{feels_like}°C", delta=f"{feels_diff:+}°C",
                                  delta_color=delta_color)

                    st.markdown("---")

                    col_a, col_b, col_c = st.columns(3)

                    with col_a:
                        st.markdown(f"#### {t('humidity')}")
                        st.markdown(f'<p class="metric-value">{current["humidity"]}%</p>', unsafe_allow_html=True)
                        st.markdown(f"#### {t('wind_speed')}")
                        st.markdown(f"{current['windspeedKmph']} km/h")
                        st.caption(current['winddir16Point'])

                    with col_b:
                        st.markdown(f"#### {t('pressure')}")
                        st.markdown(f'<p class="metric-value">{current["pressure"]} mb</p>', unsafe_allow_html=True)
                        st.markdown(f"#### {t('visibility')}")
                        st.markdown(f"{current['visibility']} km")

                    with col_c:
                        uv = int(current['uvIndex']) if str(current['uvIndex']).isdigit() else 0
                        if uv <= 2:
                            uv_text = t('uv_low')
                        elif uv <= 5:
                            uv_text = t('uv_medium')
                        elif uv <= 7:
                            uv_text = t('uv_high')
                        else:
                            uv_text = t('uv_extreme')
                        st.markdown(f"#### {t('uv')}")
                        st.markdown(f'<p class="metric-value">{current["uvIndex"]}</p>', unsafe_allow_html=True)
                        st.caption(uv_text)
                        st.markdown(f"#### {t('precip')}")
                        st.markdown(f"{current['precipMM']} mm")

                    st.markdown("---")

                    desc = current['weatherDesc'][0]['value']
                    st.info(f"📝 {t('weather_status')}: {desc}")

                    sun_col1, sun_col2, sun_col3 = st.columns(3)
                    with sun_col1:
                        st.success(f"{t('sunrise')}: {today['astronomy'][0]['sunrise']}")
                    with sun_col2:
                        st.warning(f"{t('sunset')}: {today['astronomy'][0]['sunset']}")
                    with sun_col3:
                        moon_phase_raw = today.get('astronomy', [{}])[0].get('moon_phase', '')
                        moon_icon, moon_text = get_moon_icon(moon_phase_raw)
                        st.info(f"{moon_icon} {t('moon_phase')}: {moon_text}")

                    st.markdown('</div>', unsafe_allow_html=True)

                    st.markdown('<div class="weather-card">', unsafe_allow_html=True)
                    st.markdown(f"## {t('hourly_forecast')}")

                    hourly_data = get_hourly_forecast(data)
                    if hourly_data:
                        hourly_df = pd.DataFrame(hourly_data)
                        st.dataframe(hourly_df, use_container_width=True, hide_index=True)
                    else:
                        st.info("逐小时数据暂时不可用")

                    st.markdown('</div>', unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"解析数据失败: {str(e)}")
            else:
                st.error(f"{t('query_failed')}")
                st.info(t('query_tip'))

    with col2:
        if data:
            try:
                current = data['current_condition'][0]
                today = data['weather'][0]
                temp_current = int(current['temp_C'])

                st.markdown('<div class="weather-card">', unsafe_allow_html=True)
                st.markdown(f"## {t('today_overview')}")

                temp_min = int(today['mintempC'])
                temp_max = int(today['maxtempC'])

                st.markdown(f"**{t('temp_range')}**")
                st.progress((temp_current - temp_min) / max(1, (temp_max - temp_min)),
                            text=f"{temp_min}°C ← {temp_current}°C → {temp_max}°C")

                st.markdown("---")

                get_dressing_advice_with_avatar(temp_current)

                st.markdown('</div>', unsafe_allow_html=True)

            except:
                pass

        if data:
            st.markdown('<div class="weather-card">', unsafe_allow_html=True)
            st.markdown(f"## {t('week_forecast')}")

            for i, day in enumerate(data['weather'][:7]):
                date_str = day['date']
                try:
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                    weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][date_obj.weekday()]
                    if st.session_state.language != "中文":
                        weekday_en = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][date_obj.weekday()]
                        display_date = f"{date_str} {weekday_en}"
                    else:
                        display_date = f"{date_str} {weekday}"
                except:
                    display_date = date_str

                temp_max = day['maxtempC']
                temp_min = day['mintempC']
                desc_day = day['hourly'][0]['weatherDesc'][0]['value']
                rain_chance = day['hourly'][0]['chanceofrain']
                icon = get_weather_emoji(desc_day)

                with st.expander(f"{icon} {display_date} | {temp_min}°C ~ {temp_max}°C", expanded=(i == 0)):
                    st.markdown(f"""
                    - 🌡️ {t('温度')}: {temp_min}°C ~ {temp_max}°C
                    - ☁️ {t('天气')}: {desc_day}
                    - 🌧️ {t('降水')}: {rain_chance}%
                    - 🌅 {t('sunrise')}: {day['astronomy'][0]['sunrise']}
                    - 🌇 {t('sunset')}: {day['astronomy'][0]['sunset']}
                    """)

                    temp_range = int(temp_max) - int(temp_min)
                    st.progress(min(1.0, temp_range / 30), text=f"{t('temp_diff')} {temp_range}°C")

            st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info(t('no_city'))

# ==================== 页脚 ====================
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: rgba(255,255,255,0.7); padding: 20px;">
    <p>{t('footer')}</p>
    <p>Powered by wttr.in & Streamlit | {t('version')}</p>
</div>
""", unsafe_allow_html=True)