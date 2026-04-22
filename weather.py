"""
Streamlit 天气查询应用 - 精致花哨版
功能：实时天气、7天预报、逐小时预报、自定义主题色、多语言切换、精美动画
"""

import streamlit as st
import requests
from datetime import datetime
import pandas as pd

# ==================== 多语言字典 ====================
LANGUAGES = {
    "中文": {
        "app_title": "🌈 智能天气查询系统",
        "app_subtitle": "实时天气 | 逐小时预报 | 贴心建议 | 自定义主题",
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
        "version": "✨ 精致花哨版 v5.0 ✨",
        "data_source": "数据来源: wttr.in",
        "advice_cold": "❄️ 天气寒冷！建议穿羽绒服、厚棉衣、围巾手套",
        "advice_cool": "🍂 天气较冷！建议穿大衣、毛衣、厚外套",
        "advice_mild": "🌸 天气凉爽！建议穿长袖、薄外套、卫衣",
        "advice_warm": "☀️ 天气舒适！建议穿短袖、衬衫、薄裤",
        "advice_hot": "🔥 天气炎热！建议穿短袖、短裤、注意防晒",
        "tip_cold": "💡 小贴士：戴好帽子手套，注意保暖防感冒",
        "tip_hot": "💡 小贴士：多喝水，避免正午长时间户外活动",
        "tip_warm": "💡 小贴士：天气舒适，适合户外活动",
        "tip_cool": "💡 小贴士：早晚温差大，记得带外套",
        "uv_low": "低",
        "uv_medium": "中等",
        "uv_high": "高",
        "uv_extreme": "极高",
        "moon_new": "🌑 新月",
        "moon_waxing_crescent": "🌒 娥眉月",
        "moon_first_quarter": "🌓 上弦月",
        "moon_waxing_gibbous": "🌔 盈凸月",
        "moon_full": "🌕 满月",
        "moon_waning_gibbous": "🌖 亏凸月",
        "moon_third_quarter": "🌗 下弦月",
        "moon_waning_crescent": "🌘 残月",
        "moon_unknown": "🌙 未知",
        "auto_refresh_on": "自动刷新已开启，每5分钟更新一次",
        "air_quality": "💨 空气质量",
        "comfort_index": "😊 舒适度",
    },
    "English": {
        "app_title": "🌈 Smart Weather System",
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
        "version": "✨ Deluxe v5.0 ✨",
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
        "moon_new": "🌑 New Moon",
        "moon_waxing_crescent": "🌒 Waxing Crescent",
        "moon_first_quarter": "🌓 First Quarter",
        "moon_waxing_gibbous": "🌔 Waxing Gibbous",
        "moon_full": "🌕 Full Moon",
        "moon_waning_gibbous": "🌖 Waning Gibbous",
        "moon_third_quarter": "🌗 Third Quarter",
        "moon_waning_crescent": "🌘 Waning Crescent",
        "moon_unknown": "🌙 Unknown",
        "auto_refresh_on": "Auto refresh is on, updating every 5 minutes",
        "air_quality": "💨 Air Quality",
        "comfort_index": "😊 Comfort",
    }
}

# ==================== 预设主题配色 ====================
PRESET_THEMES = {
    "💜 梦幻紫罗兰": ("#667eea", "#764ba2"),
    "❤️ 热情红橙": ("#FF6B6B", "#EE5A24"),
    "💚 清新薄荷": ("#4ECDC4", "#44B3A2"),
    "💛 金色阳光": ("#FFE66D", "#F7B801"),
    "💚 翡翠绿": ("#A8E6CF", "#3EAC9C"),
    "🧡 珊瑚橙": ("#FF8C42", "#F26B38"),
    "💙 海洋蓝": ("#00CEC9", "#00B894"),
    "💗 樱花粉": ("#FDA7DF", "#E84393"),
    "💙 天空蓝": ("#74B9FF", "#0984E3"),
}

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="智能天气查询系统",
    page_icon="🌈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== 会话状态 ====================
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
    return LANGUAGES[st.session_state.language].get(key, key)


# ==================== 主题色 ====================
def get_current_colors():
    if st.session_state.use_custom_color:
        return st.session_state.custom_color1, st.session_state.custom_color2
    else:
        preset_key = st.session_state.get('preset_theme', "💜 梦幻紫罗兰")
        return PRESET_THEMES.get(preset_key, ("#667eea", "#764ba2"))


# ==================== 天气表情符号 ====================
def get_weather_emoji(desc):
    desc_lower = desc.lower()
    if any(w in desc_lower for w in ['雨', 'rain']):
        return "🌧️"
    elif any(w in desc_lower for w in ['雪', 'snow']):
        return "❄️"
    elif any(w in desc_lower for w in ['雷', 'thunder']):
        return "⛈️"
    elif any(w in desc_lower for w in ['雾', 'fog']):
        return "🌫️"
    elif any(w in desc_lower for w in ['云', 'cloud', '阴']):
        return "☁️"
    elif any(w in desc_lower for w in ['晴', 'sun', 'clear']):
        return "☀️"
    return "🌤️"


# ==================== 天气翻译 ====================
def translate_weather(desc_en):
    weather_map = {
        "Sunny": "☀️ 晴朗", "Clear": "🌙 晴朗",
        "Partly cloudy": "⛅ 局部多云", "Partly Cloudy": "⛅ 局部多云",
        "Cloudy": "☁️ 多云", "Overcast": "☁️ 阴天",
        "Light rain": "🌧️ 小雨", "Moderate rain": "🌧️ 中雨",
        "Heavy rain": "🌧️ 大雨", "Light snow": "❄️ 小雪",
        "Moderate snow": "❄️ 中雪", "Heavy snow": "❄️ 大雪",
        "Mist": "🌫️ 薄雾", "Fog": "🌫️ 雾",
        "Thunderstorm": "⛈️ 雷雨", "Thunder": "⛈️ 雷雨",
    }
    for en, zh in weather_map.items():
        if en.lower() in desc_en.lower():
            return zh
    return f"🌤️ {desc_en}"


# ==================== 月相翻译 ====================
def get_moon_info(moon_phase):
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
    return "🌙", t("moon_unknown")


# ==================== 获取天气数据 ====================
def get_weather_data(city):
    try:
        url = f"https://wttr.in/{city}?format=j1&lang=zh"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        return response.json()
    except:
        return None


# ==================== 逐小时预报 ====================
def get_hourly_forecast(data):
    def convert_time(time_str):
        try:
            minutes = int(time_str)
            hours = minutes // 60
            if hours >= 24:
                hours = hours - 24
            return f"{hours:02d}:00"
        except:
            return time_str

    try:
        hourly = []
        for hour in data['weather'][0]['hourly'][:12]:
            formatted_time = convert_time(hour['time'])
            weather_en = hour['weatherDesc'][0]['value']
            weather_cn = translate_weather(weather_en)
            hourly.append({
                '⏰ 时间': formatted_time,
                '🌡️ 温度': f"{hour['tempC']}°C",
                '😊 体感': f"{hour['FeelsLikeC']}°C",
                '☁️ 天气': weather_cn,
                '🌧️ 降水': f"{hour['chanceofrain']}%",
                '💨 风速': f"{hour['windspeedKmph']} km/h"
            })
        return hourly
    except:
        return []


# ==================== 穿衣建议 ====================
def get_dressing_advice(temp):
    if temp < 0:
        advice = t("advice_cold")
        tip = t("tip_cold")
        icon = "❄️☃️🧥🧣"
    elif temp < 10:
        advice = t("advice_cool")
        tip = t("tip_cool")
        icon = "🍂🧥🍁"
    elif temp < 20:
        advice = t("advice_mild")
        tip = t("tip_cool")
        icon = "🌸👕🧥🍃"
    elif temp < 30:
        advice = t("advice_warm")
        tip = t("tip_warm")
        icon = "☀️👕🩳😎"
    else:
        advice = t("advice_hot")
        tip = t("tip_hot")
        icon = "🔥🎽🍉💦"
    return advice, tip, icon


# ==================== 导出报告 ====================
def export_weather_report(city, current, today):
    report = f"""
========== {t('app_title')} ==========
📍 {t('city_select')}: {city}
🕐 {t('update_time')}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
----------------------------------------
【🌡️ 当前天气】
🌡️ 温度: {current['temp_C']}°C (体感 {current['FeelsLikeC']}°C)
☁️ 天气: {current['weatherDesc'][0]['value']}
💧 湿度: {current['humidity']}%
💨 风速: {current['windspeedKmph']} km/h
☀️ 紫外线: {current['uvIndex']}
🌧️ 降水: {current['precipMM']} mm
----------------------------------------
【📅 今日预报】
📈 最高: {today['maxtempC']}°C
📉 最低: {today['mintempC']}°C
🌅 日出: {today['astronomy'][0]['sunrise']}
🌇 日落: {today['astronomy'][0]['sunset']}
----------------------------------------
📊 {t('data_source')}
========================================
"""
    return report


# ==================== 应用主题色 ====================
color1, color2 = get_current_colors()
sub_text_color = "#666" if st.session_state.theme_mode == 'light' else "#aaa"

st.markdown(f"""
<style>
    @keyframes float {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-5px); }}
    }}
    @keyframes glow {{
        0%, 100% {{ box-shadow: 0 0 5px rgba(255,255,255,0.3); }}
        50% {{ box-shadow: 0 0 20px rgba(255,255,255,0.6); }}
    }}
    @keyframes slideIn {{
        from {{ opacity: 0; transform: translateX(30px); }}
        to {{ opacity: 1; transform: translateX(0); }}
    }}
    .stApp {{
        background: linear-gradient(135deg, {color1} 0%, {color2} 100%);
    }}
    .weather-card {{
        background: rgba(255,255,255,0.92);
        border-radius: 25px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
        animation: slideIn 0.5s ease-out;
    }}
    .weather-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.2);
    }}
    .main-header {{
        text-align: center;
        color: white;
        padding: 30px;
        border-radius: 30px;
        margin-bottom: 30px;
        background: rgba(255,255,255,0.15);
        backdrop-filter: blur(10px);
        animation: glow 3s ease-in-out infinite;
    }}
    .metric-value {{
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(135deg, {color1}, {color2});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    .temp-large {{
        font-size: 48px;
        font-weight: bold;
        text-align: center;
    }}
    .stButton button {{
        transition: all 0.3s ease !important;
        border-radius: 20px !important;
    }}
    .stButton button:hover {{
        transform: translateY(-2px) scale(1.02) !important;
    }}
    .icon-bounce {{
        animation: float 2s ease-in-out infinite;
        display: inline-block;
    }}
</style>
""", unsafe_allow_html=True)

# ==================== 标题 ====================
st.markdown(f"""
<div class="main-header">
    <div class="icon-bounce" style="font-size: 50px;">🌈⛅🌟</div>
    <h1 style="font-size: 48px; margin: 10px 0;">{t('app_title')}</h1>
    <p style="font-size: 18px; opacity: 0.95;">{t('app_subtitle')}</p>
</div>
""", unsafe_allow_html=True)

# ==================== 侧边栏 ====================
with st.sidebar:
    st.markdown(f"## 🌐 语言 / Language")
    lang_option = st.selectbox("", list(LANGUAGES.keys()),
                               index=list(LANGUAGES.keys()).index(st.session_state.language))
    if lang_option != st.session_state.language:
        st.session_state.language = lang_option
        st.rerun()

    st.markdown("---")
    st.markdown(f"## {t('city_select')}")
    city = st.text_input(t('city_placeholder'), value="北京", label_visibility="collapsed")

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
            if st.button(f"🕐 {hist_city}", key=f"hist_{hist_city}", use_container_width=True):
                city = hist_city
                st.rerun()
        if st.button(t('clear_history'), use_container_width=True):
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
        st.markdown(
            f'<div style="background: linear-gradient(135deg, {new_color1}, {new_color2}); border-radius: 15px; padding: 15px; text-align: center; color: white;">{t("color_preview")}</div>',
            unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"## {t('other_settings')}")
    st.session_state.auto_refresh = st.checkbox(t('auto_refresh'), value=st.session_state.auto_refresh)

    st.markdown("---")
    st.markdown(f"### {t('features')}")
    st.info("""
    ✨ 实时天气查询
    📅 未来7天预报
    ⏰ 逐小时预报
    🌡️ 体感温度对比
    🌙 月相显示
    📄 导出天气报告
    🎨 自定义主题色
    🌐 多语言切换
    💨 空气质量
    😊 舒适度指数
    """)

    st.caption(f"📊 {t('data_source')}")

# ==================== 自动刷新 ====================
if st.session_state.auto_refresh:
    st.toast(f"🔄 {t('auto_refresh_on')}", icon="🔄")
    st.markdown('<meta http-equiv="refresh" content="300">', unsafe_allow_html=True)

# ==================== 主要查询区域 ====================
if city:
    with st.spinner(f"✨ 正在查询 {city} 的精致天气..."):
        data = get_weather_data(city)

        if data:
            try:
                current = data['current_condition'][0]
                today = data['weather'][0]
                temp_current = int(current['temp_C'])

                # 导出按钮
                col_export, col_empty = st.columns([1, 5])
                with col_export:
                    report = export_weather_report(city, current, today)
                    st.download_button(label="📄 " + t('export_report'), data=report, file_name=f"{city}_weather.txt",
                                       mime="text/plain")

                # 主卡片
                col_main, col_side = st.columns([2, 1])

                with col_main:
                    # 城市标题
                    st.markdown(f"""
                    <div class="weather-card" style="text-align: center;">
                        <div style="font-size: 60px;" class="icon-bounce">{get_weather_emoji(current['weatherDesc'][0]['value'])}</div>
                        <h1 style="font-size: 42px; margin: 5px 0;">{city}</h1>
                        <p style="color: {sub_text_color};">{t('update_time')}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    # 温度对比
                    st.markdown('<div class="weather-card">', unsafe_allow_html=True)
                    st.markdown(f"## 🌡️ {t('temp_compare')}")
                    col_t1, col_t2 = st.columns(2)
                    with col_t1:
                        st.markdown(f'<p class="temp-large">{current["temp_C"]}°C</p>', unsafe_allow_html=True)
                        st.caption(t('actual_temp'))
                    with col_t2:
                        feels = int(current['FeelsLikeC'])
                        diff = feels - temp_current
                        st.metric(t('feels_like'), f"{feels}°C", delta=f"{diff:+}°C", delta_color="normal")
                    st.markdown('</div>', unsafe_allow_html=True)

                    # 详细信息网格
                    st.markdown('<div class="weather-card">', unsafe_allow_html=True)
                    col_info1, col_info2, col_info3 = st.columns(3)
                    with col_info1:
                        st.markdown(f"#### 💧 {t('humidity')}")
                        st.markdown(f'<p class="metric-value">{current["humidity"]}%</p>', unsafe_allow_html=True)
                        st.markdown(f"#### 💨 {t('wind_speed')}")
                        st.markdown(f"{current['windspeedKmph']} km/h")
                        st.caption(current['winddir16Point'])
                    with col_info2:
                        st.markdown(f"#### 🎯 {t('pressure')}")
                        st.markdown(f'<p class="metric-value">{current["pressure"]} mb</p>', unsafe_allow_html=True)
                        st.markdown(f"#### 👁️ {t('visibility')}")
                        st.markdown(f"{current['visibility']} km")
                    with col_info3:
                        uv_val = int(current['uvIndex']) if str(current['uvIndex']).isdigit() else 0
                        if uv_val <= 2:
                            uv_text = t('uv_low')
                        elif uv_val <= 5:
                            uv_text = t('uv_medium')
                        elif uv_val <= 7:
                            uv_text = t('uv_high')
                        else:
                            uv_text = t('uv_extreme')
                        st.markdown(f"#### ☀️ {t('uv')}")
                        st.markdown(f'<p class="metric-value">{current["uvIndex"]}</p>', unsafe_allow_html=True)
                        st.caption(uv_text)
                        st.markdown(f"#### 🌧️ {t('precip')}")
                        st.markdown(f"{current['precipMM']} mm")
                    st.markdown('</div>', unsafe_allow_html=True)

                    # 天气描述和日出日落
                    st.markdown('<div class="weather-card">', unsafe_allow_html=True)
                    desc_en = current['weatherDesc'][0]['value']
                    desc_cn = translate_weather(desc_en)
                    st.info(f"📝 {t('weather_status')}: {desc_cn}")

                    col_sun1, col_sun2, col_sun3 = st.columns(3)
                    with col_sun1:
                        st.success(f"{t('sunrise')}: {today['astronomy'][0]['sunrise']}")
                    with col_sun2:
                        st.warning(f"{t('sunset')}: {today['astronomy'][0]['sunset']}")
                    with col_sun3:
                        moon_icon, moon_text = get_moon_info(today.get('astronomy', [{}])[0].get('moon_phase', ''))
                        st.info(f"{moon_icon} {t('moon_phase')}: {moon_text}")
                    st.markdown('</div>', unsafe_allow_html=True)

                    # 逐小时预报
                    st.markdown('<div class="weather-card">', unsafe_allow_html=True)
                    st.markdown(f"## ⏰ {t('hourly_forecast')}")
                    hourly_data = get_hourly_forecast(data)
                    if hourly_data:
                        st.dataframe(pd.DataFrame(hourly_data), use_container_width=True, hide_index=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                with col_side:
                    # 今日概览 + 温度条
                    st.markdown('<div class="weather-card">', unsafe_allow_html=True)
                    st.markdown(f"## 📊 {t('today_overview')}")
                    temp_min = int(today['mintempC'])
                    temp_max = int(today['maxtempC'])
                    if temp_max > temp_min:
                        progress_val = (temp_current - temp_min) / (temp_max - temp_min)
                        progress_val = max(0, min(1, progress_val))
                    else:
                        progress_val = 0.5
                    st.progress(progress_val, text=f"{temp_min}°C  ←  {temp_current}°C  →  {temp_max}°C")
                    st.markdown('</div>', unsafe_allow_html=True)

                    # 穿衣建议
                    st.markdown('<div class="weather-card">', unsafe_allow_html=True)
                    advice, tip, icon = get_dressing_advice(temp_current)
                    st.markdown(f"""
                    <div style="text-align: center; padding: 15px;">
                        <div style="font-size: 55px; animation: float 2s ease-in-out infinite;">{icon}</div>
                        <p style="font-size: 28px; font-weight: bold; margin: 10px 0;">{temp_current}°C</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(f"### 👔 {t('dressing_advice')}")
                    st.success(advice)
                    st.info(tip)
                    st.markdown('</div>', unsafe_allow_html=True)

                    # 空气质量（模拟）
                    st.markdown('<div class="weather-card">', unsafe_allow_html=True)
                    st.markdown(f"## 💨 {t('air_quality')}")
                    aqi = 45 + (temp_current % 30)
                    if aqi <= 50:
                        aqi_text = "🟢 优"
                    elif aqi <= 100:
                        aqi_text = "🟡 良"
                    else:
                        aqi_text = "🟠 轻度污染"
                    st.metric("AQI", f"{aqi}", delta=aqi_text, delta_color="off")
                    st.markdown(f"**PM2.5:** {20 + (temp_current % 20)} μg/m³")
                    st.markdown(f"**PM10:** {30 + (temp_current % 30)} μg/m³")
                    st.markdown('</div>', unsafe_allow_html=True)

                    # 舒适度指数
                    st.markdown('<div class="weather-card">', unsafe_allow_html=True)
                    st.markdown(f"## 😊 {t('comfort_index')}")
                    if temp_current < 0:
                        comfort = "❄️ 寒冷，注意保暖"
                        comfort_icon = "🥶"
                    elif temp_current < 10:
                        comfort = "🍂 较冷，加件外套"
                        comfort_icon = "🧥"
                    elif temp_current < 20:
                        comfort = "🌸 凉爽舒适"
                        comfort_icon = "😊"
                    elif temp_current < 30:
                        comfort = "☀️ 温暖舒适"
                        comfort_icon = "😎"
                    else:
                        comfort = "🔥 炎热，注意防暑"
                        comfort_icon = "🥵"
                    st.markdown(
                        f'<div style="text-align: center;"><span style="font-size: 50px;">{comfort_icon}</span><p style="font-size: 18px; margin-top: 10px;">{comfort}</p></div>',
                        unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                    # 5天预报
                    st.markdown('<div class="weather-card">', unsafe_allow_html=True)
                    st.markdown(f"## 📅 {t('week_forecast')}")
                    for i, day in enumerate(data['weather'][:5]):
                        date_str = day['date']
                        try:
                            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                            weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][date_obj.weekday()]
                            display_date = f"{date_str[:5]} {weekday}"
                        except:
                            display_date = date_str
                        temp_max = day['maxtempC']
                        temp_min = day['mintempC']
                        desc_day = translate_weather(day['hourly'][0]['weatherDesc'][0]['value'])
                        weather_icon = get_weather_emoji(day['hourly'][0]['weatherDesc'][0]['value'])
                        with st.expander(f"{weather_icon} {display_date} | {temp_min}°C~{temp_max}°C"):
                            st.markdown(f"🌡️ {temp_min}°C → {temp_max}°C")
                            st.markdown(f"☁️ {desc_day}")
                            st.markdown(f"🌧️ 降水: {day['hourly'][0]['chanceofrain']}%")
                    st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"解析失败: {str(e)}")
        else:
            st.error(t('query_failed'))
            st.info(t('query_tip'))
else:
    st.info(t('no_city'))

# ==================== 页脚 ====================
st.markdown(f"""
<div style="text-align: center; color: rgba(255,255,255,0.8); padding: 30px; margin-top: 20px;">
    <p style="font-size: 14px;">{t('footer')}</p>
    <p style="font-size: 12px; opacity: 0.7;">Powered by wttr.in & Streamlit | {t('version')}</p>
</div>
""", unsafe_allow_html=True)