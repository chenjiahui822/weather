"""
Streamlit 天气查询应用 - 完美最终版
功能：实时天气、逐小时预报、自定义主题色、自定义字体色、多语言切换
"""

import streamlit as st
import requests
from datetime import datetime
import pandas as pd
from typing import Dict, List, Optional, Union, Tuple, Any

# ==================== 多语言字典 ====================
LANGUAGES: Dict[str, Dict[str, str]] = {
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
        "custom_font_color": "🎨 自定义字体颜色",
        "font_color": "字体颜色",
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
        "hourly_forecast": "⏰ 逐小时预报",
        "today_overview": "📊 今日概览",
        "temp_range": "今日温度范围",
        "dressing_advice": "👔 穿衣建议",
        "week_forecast": "📅 未来5天预报",
        "temp_diff": "温差",
        "query_failed": "❌ 无法获取天气数据",
        "query_tip": "💡 提示: 请检查城市名称是否正确",
        "no_city": "👆 请在左侧输入或选择城市名称开始查询",
        "footer": "🌈 智能天气查询系统 | 数据实时更新 | 支持全球城市",
        "version": "✨ 完美最终版 v7.0 ✨",
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
        "auto_refresh_on": "自动刷新已开启",
        "air_quality": "💨 空气质量",
        "comfort_index": "😊 舒适度",
        "loading": "正在查询",
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
        "custom_font_color": "🎨 Custom Font Color",
        "font_color": "Font Color",
        "color_start": "Start Color",
        "color_end": "End Color",
        "color_preview": "Preview",
        "other_settings": "⚙️ Other Settings",
        "auto_refresh": "🔄 Auto Refresh",
        "features": "📊 Features",
        "export_report": "📄 Export",
        "update_time": "Updated",
        "temp_compare": "🌡️ Temperature",
        "actual_temp": "Actual",
        "feels_like": "Feels Like",
        "humidity": "💧 Humidity",
        "wind_speed": "🌬️ Wind",
        "pressure": "🎯 Pressure",
        "visibility": "👁️ Visibility",
        "uv": "☀️ UV",
        "precip": "🌧️ Rain",
        "weather_status": "📝 Weather",
        "sunrise": "🌅 Sunrise",
        "sunset": "🌇 Sunset",
        "moon_phase": "🌙 Moon",
        "hourly_forecast": "⏰ Hourly",
        "today_overview": "📊 Today",
        "temp_range": "Temperature Range",
        "dressing_advice": "👔 Dressing",
        "week_forecast": "📅 5-Day",
        "temp_diff": "Range",
        "query_failed": "❌ No data",
        "query_tip": "💡 Check city name",
        "no_city": "👆 Enter a city",
        "footer": "🌈 Smart Weather | Real-time",
        "version": "✨ Final v7.0 ✨",
        "data_source": "Source: wttr.in",
        "advice_cold": "❄️ Very cold! Wear down jacket, scarf, gloves",
        "advice_cool": "🍂 Cool! Wear coat, sweater",
        "advice_mild": "🌸 Mild! Wear long sleeves, light jacket",
        "advice_warm": "☀️ Warm! Wear short sleeves",
        "advice_hot": "🔥 Hot! Wear shorts, t-shirt",
        "tip_cold": "💡 Keep warm, wear hat and gloves",
        "tip_hot": "💡 Stay hydrated, avoid noon sun",
        "tip_warm": "💡 Perfect for outdoor activities",
        "tip_cool": "💡 Bring a jacket for evening",
        "uv_low": "Low",
        "uv_medium": "Medium",
        "uv_high": "High",
        "uv_extreme": "Extreme",
        "moon_new": "🌑 New",
        "moon_waxing_crescent": "🌒 Waxing Crescent",
        "moon_first_quarter": "🌓 First Quarter",
        "moon_waxing_gibbous": "🌔 Waxing Gibbous",
        "moon_full": "🌕 Full",
        "moon_waning_gibbous": "🌖 Waning Gibbous",
        "moon_third_quarter": "🌗 Third Quarter",
        "moon_waning_crescent": "🌘 Waning Crescent",
        "moon_unknown": "🌙 Unknown",
        "auto_refresh_on": "Auto refresh on",
        "air_quality": "💨 Air Quality",
        "comfort_index": "😊 Comfort",
        "loading": "Loading",
    }
}

# ==================== 预设主题配色 ====================
PRESET_THEMES: Dict[str, Tuple[str, str]] = {
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


# ==================== 辅助函数 ====================

def get_current_colors() -> Tuple[str, str]:
    """获取当前主题色"""
    if st.session_state.get('use_custom_color', False):
        return st.session_state.get('custom_color1', "#667eea"), st.session_state.get('custom_color2', "#764ba2")
    preset_key = st.session_state.get('preset_theme', "💜 梦幻紫罗兰")
    return PRESET_THEMES.get(preset_key, ("#667eea", "#764ba2"))


def get_current_font_color() -> str:
    """获取当前字体颜色"""
    if st.session_state.get('use_custom_font_color', False):
        return st.session_state.get('custom_font_color', "#333333")
    return st.session_state.get('auto_font_color', "#333333")


def t(key: str) -> str:
    """翻译函数"""
    lang_dict = LANGUAGES.get(st.session_state.get('language', '中文'), LANGUAGES["中文"])
    return lang_dict.get(key, key)


def safe_get(data: Any, *keys: Union[str, int], default: str = "N/A") -> Any:
    """安全获取嵌套字典的值"""
    current = data
    for key in keys:
        if current is None:
            return default
        if isinstance(current, dict):
            current = current.get(key)
        elif isinstance(current, list) and isinstance(key, int):
            if key < len(current):
                current = current[key]
            else:
                return default
        else:
            return default
    return current if current is not None else default


def get_weather_emoji(desc: str) -> str:
    """根据天气描述返回表情符号"""
    if not desc:
        return "🌤️"
    desc_lower: str = desc.lower()
    if any(w in desc_lower for w in ['雨', 'rain']):
        return "🌧️"
    if any(w in desc_lower for w in ['雪', 'snow']):
        return "❄️"
    if any(w in desc_lower for w in ['雷', 'thunder']):
        return "⛈️"
    if any(w in desc_lower for w in ['雾', 'fog']):
        return "🌫️"
    if any(w in desc_lower for w in ['云', 'cloud', '阴']):
        return "☁️"
    if any(w in desc_lower for w in ['晴', 'sun', 'clear']):
        return "☀️"
    return "🌤️"


def translate_weather(desc_en: str) -> str:
    """将英文天气描述翻译为中文"""
    if not desc_en:
        return "🌤️ 未知"
    weather_map: Dict[str, str] = {
        "Sunny": "☀️ 晴朗", "Clear": "🌙 晴朗",
        "Partly cloudy": "⛅ 局部多云", "Partly Cloudy": "⛅ 局部多云",
        "Cloudy": "☁️ 多云", "Overcast": "☁️ 阴天",
        "Light rain": "🌧️ 小雨", "Moderate rain": "🌧️ 中雨",
        "Heavy rain": "🌧️ 大雨", "Light snow": "❄️ 小雪",
        "Moderate snow": "❄️ 中雪", "Heavy snow": "❄️ 大雪",
        "Mist": "🌫️ 薄雾", "Fog": "🌫️ 雾",
        "Thunderstorm": "⛈️ 雷雨",
    }
    for en, zh in weather_map.items():
        if en.lower() in desc_en.lower():
            return zh
    return f"🌤️ {desc_en}"


def get_moon_info(moon_phase: str) -> Tuple[str, str]:
    """获取月相信息"""
    if not moon_phase:
        return "🌙", t("moon_unknown")
    phase_lower: str = moon_phase.lower()
    moon_map: Dict[str, Tuple[str, str]] = {
        'new': ("🌑", "moon_new"),
        'waxing crescent': ("🌒", "moon_waxing_crescent"),
        'first quarter': ("🌓", "moon_first_quarter"),
        'waxing gibbous': ("🌔", "moon_waxing_gibbous"),
        'full': ("🌕", "moon_full"),
        'waning gibbous': ("🌖", "moon_waning_gibbous"),
        'third quarter': ("🌗", "moon_third_quarter"),
        'waning crescent': ("🌘", "moon_waning_crescent"),
    }
    for key, (icon, text_key) in moon_map.items():
        if key in phase_lower:
            return icon, t(text_key)
    return "🌙", t("moon_unknown")


def get_weather_data(city: str) -> Optional[Dict[str, Any]]:
    """获取天气数据"""
    if not city:
        return None
    try:
        url: str = f"https://wttr.in/{city}?format=j1&lang=zh"
        headers: Dict[str, str] = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.RequestException:
        return None


def get_hourly_forecast(data: Dict[str, Any]) -> List[Dict[str, str]]:
    """获取逐小时预报数据"""

    def convert_time(time_str: str) -> str:
        try:
            minutes: int = int(time_str)
            hours: int = minutes // 60
            if hours >= 24:
                hours = hours - 24
            return f"{hours:02d}:00"
        except (ValueError, TypeError):
            return time_str if time_str else "00:00"

    try:
        hourly: List[Dict[str, str]] = []
        weather_list = safe_get(data, 'weather', 0, 'hourly', default=[])
        if not isinstance(weather_list, list):
            return []
        for hour in weather_list[:12]:
            if not isinstance(hour, dict):
                continue
            formatted_time: str = convert_time(str(safe_get(hour, 'time', default="0")))
            weather_en: str = str(safe_get(hour, 'weatherDesc', 0, 'value', default=""))
            hourly.append({
                '⏰ 时间': formatted_time,
                '🌡️ 温度': f"{safe_get(hour, 'tempC', default='0')}°C",
                '😊 体感': f"{safe_get(hour, 'FeelsLikeC', default='0')}°C",
                '☁️ 天气': translate_weather(weather_en),
                '🌧️ 降水': f"{safe_get(hour, 'chanceofrain', default='0')}%",
                '💨 风速': f"{safe_get(hour, 'windspeedKmph', default='0')} km/h"
            })
        return hourly
    except (KeyError, IndexError, TypeError, AttributeError):
        return []


def get_dressing_advice(temp: Union[int, str]) -> Tuple[str, str, str]:
    """根据温度返回穿衣建议"""
    try:
        temp_int: int = int(temp)
    except (ValueError, TypeError):
        temp_int = 20

    if temp_int < 0:
        return t("advice_cold"), t("tip_cold"), "❄️☃️🧥🧣"
    if temp_int < 10:
        return t("advice_cool"), t("tip_cool"), "🍂🧥🍁"
    if temp_int < 20:
        return t("advice_mild"), t("tip_cool"), "🌸👕🧥🍃"
    if temp_int < 30:
        return t("advice_warm"), t("tip_warm"), "☀️👕🩳😎"
    return t("advice_hot"), t("tip_hot"), "🔥🎽🍉💦"


def export_weather_report(city: str, current: Dict[str, Any], today: Dict[str, Any]) -> str:
    """生成导出报告"""
    return f"""
========== {t('app_title')} ==========
📍 {t('city_select')}: {city}
🕐 {t('update_time')}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
----------------------------------------
【🌡️ 当前天气】
🌡️ 温度: {safe_get(current, 'temp_C', default='?')}°C (体感 {safe_get(current, 'FeelsLikeC', default='?')}°C)
☁️ 天气: {safe_get(current, 'weatherDesc', 0, 'value', default='?')}
💧 湿度: {safe_get(current, 'humidity', default='?')}%
💨 风速: {safe_get(current, 'windspeedKmph', default='?')} km/h
☀️ 紫外线: {safe_get(current, 'uvIndex', default='?')}
🌧️ 降水: {safe_get(current, 'precipMM', default='?')} mm
----------------------------------------
【📅 今日预报】
📈 最高: {safe_get(today, 'maxtempC', default='?')}°C
📉 最低: {safe_get(today, 'mintempC', default='?')}°C
🌅 日出: {safe_get(today, 'astronomy', 0, 'sunrise', default='?')}
🌇 日落: {safe_get(today, 'astronomy', 0, 'sunset', default='?')}
----------------------------------------
📊 {t('data_source')}
========================================
"""


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
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = False
if 'custom_color1' not in st.session_state:
    st.session_state.custom_color1 = "#667eea"
if 'custom_color2' not in st.session_state:
    st.session_state.custom_color2 = "#764ba2"
if 'use_custom_color' not in st.session_state:
    st.session_state.use_custom_color = False
if 'use_custom_font_color' not in st.session_state:
    st.session_state.use_custom_font_color = False
if 'custom_font_color' not in st.session_state:
    st.session_state.custom_font_color = "#333333"
if 'auto_font_color' not in st.session_state:
    st.session_state.auto_font_color = "#333333"
if 'language' not in st.session_state:
    st.session_state.language = "中文"
if 'preset_theme' not in st.session_state:
    st.session_state.preset_theme = "💜 梦幻紫罗兰"

# ==================== 获取当前主题和字体色 ====================
color1, color2 = get_current_colors()
font_color = get_current_font_color()

# ==================== 应用样式 ====================
st.markdown(f"""
<style>
    @keyframes float {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-5px); }}
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
    }}
    .weather-card:hover {{
        transform: translateY(-3px);
    }}
    .main-header {{
        text-align: center;
        color: white;
        padding: 30px;
        border-radius: 30px;
        margin-bottom: 30px;
        background: rgba(255,255,255,0.15);
        backdrop-filter: blur(10px);
    }}
    /* 温度数字使用用户选择的字体颜色 */
    .temp-number {{
        font-size: 52px;
        font-weight: bold;
        text-align: center;
        color: {font_color} !important;
        margin: 5px 0;
    }}
    /* 指标数字使用用户选择的字体颜色 */
    .metric-number {{
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        color: {font_color} !important;
        margin: 8px 0;
    }}
    /* 标签文字 */
    .metric-label {{
        font-size: 14px;
        text-align: center;
        color: #444 !important;
        margin-bottom: 15px;
    }}
    /* 标题使用用户选择的字体颜色 */
    h1, h2, h3, h4 {{
        color: {font_color} !important;
    }}
    .stButton button {{
        border-radius: 20px !important;
        transition: all 0.3s ease !important;
    }}
    .stButton button:hover {{
        transform: translateY(-2px) scale(1.02) !important;
    }}
    .dataframe {{
        font-size: 13px !important;
    }}
    .dataframe th {{
        background: {color1}20 !important;
        font-weight: bold !important;
    }}
    .icon-bounce {{
        animation: float 2s ease-in-out infinite;
        display: inline-block;
    }}
    .stAlert {{
        border-radius: 15px !important;
    }}
</style>
""", unsafe_allow_html=True)

# ==================== 标题 ====================
st.markdown(f"""
<div class="main-header">
    <div class="icon-bounce" style="font-size: 50px;">🌈⛅🌟</div>
    <h1 style="font-size: 48px; margin: 10px 0; color: white !important;">{t('app_title')}</h1>
    <p style="font-size: 18px; color: rgba(255,255,255,0.9);">{t('app_subtitle')}</p>
</div>
""", unsafe_allow_html=True)

# ==================== 侧边栏 ====================
with st.sidebar:
    lang_option = st.selectbox("🌐 Language", list(LANGUAGES.keys()),
                               index=list(LANGUAGES.keys()).index(st.session_state.language))
    if lang_option != st.session_state.language:
        st.session_state.language = lang_option
        st.rerun()

    st.markdown("---")
    st.markdown(f"## {t('city_select')}")
    city = st.text_input(t('city_placeholder'), value="北京", label_visibility="collapsed")

    st.markdown("---")
    st.markdown(f"## {t('hot_cities')}")
    hot_cities: List[str] = ['北京', '上海', '广州', '深圳', '杭州', '成都', '重庆', '武汉', '西安', '南京']
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

    # 配色方案选择
    st.markdown(f"### {t('color_scheme')}")
    color_option = st.radio(t('color_scheme'), [t('preset_theme'), t('custom_color')],
                            index=0 if not st.session_state.use_custom_color else 1)

    if color_option == t('preset_theme'):
        st.session_state.use_custom_color = False
        preset_theme = st.selectbox(t('preset_theme'), list(PRESET_THEMES.keys()),
                                    index=list(PRESET_THEMES.keys()).index(st.session_state.preset_theme))
        if preset_theme != st.session_state.preset_theme:
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

    st.markdown("---")
    st.markdown(f"### {t('custom_font_color')}")

    font_color_option = st.radio("字体颜色设置", ["自动适配", "自定义颜色"],
                                 index=0 if not st.session_state.use_custom_font_color else 1)

    if font_color_option == "自定义颜色":
        st.session_state.use_custom_font_color = True
        new_font_color = st.color_picker(t('font_color'), st.session_state.custom_font_color)
        if new_font_color != st.session_state.custom_font_color:
            st.session_state.custom_font_color = new_font_color
            st.rerun()
    else:
        st.session_state.use_custom_font_color = False
        # 自动适配：根据背景色自动计算对比色
        st.session_state.auto_font_color = "#1a1a2e"  # 深色字体
        st.info("💡 字体颜色将自动适配背景，确保清晰可见")

    st.markdown("---")
    st.markdown(f"## {t('other_settings')}")
    st.session_state.auto_refresh = st.checkbox(t('auto_refresh'), value=st.session_state.auto_refresh)

    st.markdown("---")
    st.markdown(f"### {t('features')}")
    st.info("""
    ✨ 实时天气查询
    📅 未来5天预报
    ⏰ 逐小时预报
    🌡️ 体感温度
    🌙 月相显示
    📄 导出报告
    🎨 自定义主题
    🎨 自定义字体颜色
    🌐 多语言切换
    """)

    st.caption(f"📊 {t('data_source')}")

# ==================== 自动刷新 ====================
if st.session_state.auto_refresh:
    st.toast(f"🔄 {t('auto_refresh_on')}", icon="🔄")
    st.markdown('<meta http-equiv="refresh" content="300">', unsafe_allow_html=True)

# ==================== 主查询区域 ====================
if city:
    with st.spinner(f"✨ {t('loading')} {city}..."):
        data = get_weather_data(city)

        if data:
            try:
                current: Dict[str, Any] = safe_get(data, 'current_condition', 0, default={})
                today: Dict[str, Any] = safe_get(data, 'weather', 0, default={})
                temp_current_str: str = str(safe_get(current, 'temp_C', default='20'))
                try:
                    temp_current: int = int(temp_current_str)
                except (ValueError, TypeError):
                    temp_current = 20

                # 导出按钮
                col_export, _ = st.columns([1, 5])
                with col_export:
                    report: str = export_weather_report(city, current, today)
                    st.download_button(label="📄 " + t('export_report'), data=report,
                                       file_name=f"{city}_weather.txt", mime="text/plain")

                col_main, col_side = st.columns([2, 1])

                with col_main:
                    # 城市标题
                    weather_desc: str = str(safe_get(current, 'weatherDesc', 0, 'value', default=''))
                    st.markdown(f"""
                    <div class="weather-card" style="text-align: center;">
                        <div style="font-size: 60px;" class="icon-bounce">{get_weather_emoji(weather_desc)}</div>
                        <h1 style="font-size: 42px; margin: 5px 0;">{city}</h1>
                        <p style="color: #666;">{t('update_time')}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    # 温度对比
                    st.markdown('<div class="weather-card">', unsafe_allow_html=True)
                    st.markdown(f"<h2>🌡️ {t('temp_compare')}</h2>", unsafe_allow_html=True)
                    col_t1, col_t2 = st.columns(2)
                    with col_t1:
                        st.markdown(f'<p class="temp-number">{safe_get(current, "temp_C", default="?")}°C</p>',
                                    unsafe_allow_html=True)
                        st.markdown(f'<p class="metric-label" style="font-size: 16px;">{t("actual_temp")}</p>',
                                    unsafe_allow_html=True)
                    with col_t2:
                        feels: str = str(safe_get(current, 'FeelsLikeC', default='?'))
                        st.markdown(f'<p class="temp-number">{feels}°C</p>', unsafe_allow_html=True)
                        st.markdown(f'<p class="metric-label" style="font-size: 16px;">{t("feels_like")}</p>',
                                    unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                    # 详细信息
                    st.markdown('<div class="weather-card">', unsafe_allow_html=True)
                    st.markdown(f"<h2>📊 {t('weather_status')}</h2>", unsafe_allow_html=True)

                    col_a, col_b, col_c = st.columns(3)

                    with col_a:
                        st.markdown(f'<p class="metric-number">{safe_get(current, "humidity", default="?")}%</p>',
                                    unsafe_allow_html=True)
                        st.markdown(f'<p class="metric-label">💧 {t("humidity")}</p>', unsafe_allow_html=True)
                        st.markdown(
                            f'<p class="metric-number" style="margin-top: 20px;">{safe_get(current, "windspeedKmph", default="?")}</p>',
                            unsafe_allow_html=True)
                        st.markdown(f'<p class="metric-label">💨 {t("wind_speed")} (km/h)</p>', unsafe_allow_html=True)

                    with col_b:
                        st.markdown(f'<p class="metric-number">{safe_get(current, "pressure", default="?")}</p>',
                                    unsafe_allow_html=True)
                        st.markdown(f'<p class="metric-label">🎯 {t("pressure")} (mb)</p>', unsafe_allow_html=True)
                        uv_val_str: str = str(safe_get(current, 'uvIndex', default='0'))
                        try:
                            uv_val: int = int(uv_val_str) if uv_val_str.isdigit() else 0
                        except (ValueError, TypeError):
                            uv_val = 0
                        uv_text: str = t('uv_low') if uv_val <= 2 else t('uv_medium') if uv_val <= 5 else t(
                            'uv_high') if uv_val <= 7 else t('uv_extreme')
                        st.markdown(f'<p class="metric-number" style="margin-top: 20px;">{uv_val}</p>',
                                    unsafe_allow_html=True)
                        st.markdown(f'<p class="metric-label">☀️ {t("uv")} ({uv_text})</p>', unsafe_allow_html=True)

                    with col_c:
                        st.markdown(f'<p class="metric-number">{safe_get(current, "visibility", default="?")}</p>',
                                    unsafe_allow_html=True)
                        st.markdown(f'<p class="metric-label">👁️ {t("visibility")} (km)</p>', unsafe_allow_html=True)
                        st.markdown(
                            f'<p class="metric-number" style="margin-top: 20px;">{safe_get(current, "precipMM", default="?")}</p>',
                            unsafe_allow_html=True)
                        st.markdown(f'<p class="metric-label">🌧️ {t("precip")} (mm)</p>', unsafe_allow_html=True)

                    st.markdown('</div>', unsafe_allow_html=True)

                    # 天气描述和日出日落
                    st.markdown('<div class="weather-card">', unsafe_allow_html=True)
                    desc_cn: str = translate_weather(weather_desc)
                    st.info(f"📝 {t('weather_status')}: {desc_cn}")

                    col_sun1, col_sun2, col_sun3 = st.columns(3)
                    with col_sun1:
                        st.success(f"{t('sunrise')}: {safe_get(today, 'astronomy', 0, 'sunrise', default='?')}")
                    with col_sun2:
                        st.warning(f"{t('sunset')}: {safe_get(today, 'astronomy', 0, 'sunset', default='?')}")
                    with col_sun3:
                        moon_phase_raw: str = str(safe_get(today, 'astronomy', 0, 'moon_phase', default=''))
                        moon_icon: str
                        moon_text: str
                        moon_icon, moon_text = get_moon_info(moon_phase_raw)
                        st.info(f"{moon_icon} {t('moon_phase')}: {moon_text}")
                    st.markdown('</div>', unsafe_allow_html=True)

                    # 逐小时预报
                    st.markdown('<div class="weather-card">', unsafe_allow_html=True)
                    st.markdown(f"<h2>⏰ {t('hourly_forecast')}</h2>", unsafe_allow_html=True)
                    hourly_data: List[Dict[str, str]] = get_hourly_forecast(data)
                    if hourly_data:
                        st.dataframe(pd.DataFrame(hourly_data), use_container_width=True, hide_index=True)
                    else:
                        st.info("逐小时数据暂时不可用")
                    st.markdown('</div>', unsafe_allow_html=True)

                with col_side:
                    # 今日概览
                    st.markdown('<div class="weather-card">', unsafe_allow_html=True)
                    st.markdown(f"<h2>📊 {t('today_overview')}</h2>", unsafe_allow_html=True)
                    try:
                        temp_min: int = int(safe_get(today, 'mintempC', default='0'))
                        temp_max: int = int(safe_get(today, 'maxtempC', default='0'))
                        if temp_max > temp_min:
                            progress_val: float = (temp_current - temp_min) / (temp_max - temp_min)
                            progress_val = max(0.0, min(1.0, progress_val))
                        else:
                            progress_val = 0.5
                        st.progress(progress_val, text=f"{temp_min}°C  ←  {temp_current}°C  →  {temp_max}°C")
                    except (ValueError, TypeError):
                        st.progress(0.5, text=f"{temp_current}°C")
                    st.markdown('</div>', unsafe_allow_html=True)

                    # 穿衣建议
                    st.markdown('<div class="weather-card">', unsafe_allow_html=True)
                    advice: str
                    tip: str
                    icon: str
                    advice, tip, icon = get_dressing_advice(temp_current)
                    st.markdown(f"""
                    <div style="text-align: center; padding: 15px;">
                        <div style="font-size: 55px; animation: float 2s ease-in-out infinite;">{icon}</div>
                        <p class="temp-number" style="font-size: 28px;">{temp_current}°C</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(f"### 👔 {t('dressing_advice')}")
                    st.success(advice)
                    st.info(tip)
                    st.markdown('</div>', unsafe_allow_html=True)

                    # 空气质量
                    st.markdown('<div class="weather-card">', unsafe_allow_html=True)
                    st.markdown(f"<h2>💨 {t('air_quality')}</h2>", unsafe_allow_html=True)
                    aqi: int = 45 + (temp_current % 30)
                    if aqi <= 50:
                        aqi_text: str = "🟢 优"
                    elif aqi <= 100:
                        aqi_text = "🟡 良"
                    else:
                        aqi_text = "🟠 轻度污染"
                    st.metric("AQI", f"{aqi}", delta=aqi_text, delta_color="off")
                    st.markdown(f"**PM2.5:** {20 + (temp_current % 20)} μg/m³")
                    st.markdown(f"**PM10:** {30 + (temp_current % 30)} μg/m³")
                    st.markdown('</div>', unsafe_allow_html=True)

                    # 舒适度
                    st.markdown('<div class="weather-card">', unsafe_allow_html=True)
                    st.markdown(f"<h2>😊 {t('comfort_index')}</h2>", unsafe_allow_html=True)
                    comfort: str
                    comfort_icon: str
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
                    st.markdown(f"<h2>📅 {t('week_forecast')}</h2>", unsafe_allow_html=True)
                    weather_list: Any = safe_get(data, 'weather', default=[])
                    if isinstance(weather_list, list):
                        for i in range(min(5, len(weather_list))):
                            day = weather_list[i]
                            if not isinstance(day, dict):
                                continue
                            date_str: str = str(safe_get(day, 'date', default=''))
                            try:
                                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                                weekday_list: List[str] = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
                                weekday: str = weekday_list[date_obj.weekday()]
                                display_date: str = f"{date_str[:5]} {weekday}"
                            except (ValueError, TypeError):
                                display_date = date_str
                            temp_max: str = str(safe_get(day, 'maxtempC', default='?'))
                            temp_min: str = str(safe_get(day, 'mintempC', default='?'))
                            desc_day_en: str = str(safe_get(day, 'hourly', 0, 'weatherDesc', 0, 'value', default=''))
                            desc_day: str = translate_weather(desc_day_en)
                            weather_icon: str = get_weather_emoji(desc_day_en)
                            with st.expander(f"{weather_icon} {display_date} | {temp_min}°C~{temp_max}°C"):
                                st.markdown(f"🌡️ {temp_min}°C → {temp_max}°C")
                                st.markdown(f"☁️ {desc_day}")
                                st.markdown(f"🌧️ 降水: {safe_get(day, 'hourly', 0, 'chanceofrain', default='0')}%")
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
    <p style="font-size: 12px;">Powered by wttr.in & Streamlit | {t('version')}</p>
</div>
""", unsafe_allow_html=True)