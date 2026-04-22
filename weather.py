"""
Streamlit 天气查询应用 - 增强版
只使用 wttr.in 数据，无需任何API Key
"""

import streamlit as st
import requests
from datetime import datetime, timedelta
import pandas as pd

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
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = False


# ==================== 辅助函数 ====================

def get_weather_emoji(desc):
    """根据天气描述返回表情符号"""
    desc_lower = desc.lower()
    if any(word in desc_lower for word in ['雨', 'rain', 'shower']):
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
    """根据月相返回表情符号"""
    phase_lower = moon_phase.lower()
    if 'new' in phase_lower:
        return "🌑"
    elif 'waxing crescent' in phase_lower:
        return "🌒"
    elif 'first quarter' in phase_lower:
        return "🌓"
    elif 'waxing gibbous' in phase_lower:
        return "🌔"
    elif 'full' in phase_lower:
        return "🌕"
    elif 'waning gibbous' in phase_lower:
        return "🌖"
    elif 'third quarter' in phase_lower:
        return "🌗"
    elif 'waning crescent' in phase_lower:
        return "🌘"
    else:
        return "🌙"


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
    """获取逐小时预报数据"""
    try:
        hourly = []
        for i, hour in enumerate(data['weather'][0]['hourly'][:12]):  # 未来12小时
            hourly.append({
                '时间': hour['time'],
                '温度': f"{hour['tempC']}°C",
                '体感': f"{hour['FeelsLikeC']}°C",
                '天气': hour['weatherDesc'][0]['value'],
                '降水': f"{hour['chanceofrain']}%",
                '风速': f"{hour['windspeedKmph']} km/h"
            })
        return hourly
    except:
        return []


def export_weather_report(city, current, today):
    """生成可导出的天气报告文本"""
    report = f"""
========== 天气报告 ==========
城市: {city}
查询时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
--------------------------------
【当前天气】
温度: {current['temp_C']}°C (体感 {current['FeelsLikeC']}°C)
天气: {current['weatherDesc'][0]['value']}
湿度: {current['humidity']}%
风速: {current['windspeedKmph']} km/h {current['winddir16Point']}
紫外线: {current['uvIndex']}
降水: {current['precipMM']} mm
--------------------------------
【今日预报】
最高温: {today['maxtempC']}°C
最低温: {today['mintempC']}°C
日出: {today['astronomy'][0]['sunrise']}
日落: {today['astronomy'][0]['sunset']}
月相: {today.get('astronomy', [{}])[0].get('moon_phase', '未知')}
--------------------------------
数据来源: wttr.in
================================
"""
    return report


# ==================== 自定义CSS（支持主题切换）====================
if st.session_state.theme == 'dark':
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        }
        .weather-card {
            background: rgba(30,30,50,0.95);
            color: #eee;
        }
        .main-header h1, .main-header p {
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .weather-card {
            background: rgba(255,255,255,0.95);
        }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .weather-card {
        border-radius: 20px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 5px 20px rgba(0,0,0,0.2);
    }
    .temp-large {
        font-size: 48px;
        font-weight: bold;
        text-align: center;
    }
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ==================== 标题 ====================
st.markdown("""
<div class="main-header">
    <h1>🌈 智能天气查询系统</h1>
    <p>实时天气 | 逐小时预报 | 贴心建议</p>
</div>
""", unsafe_allow_html=True)

# ==================== 侧边栏 ====================
with st.sidebar:
    st.markdown("## 🎯 城市选择")

    # 城市输入
    city = st.text_input("请输入城市名称", value="北京", placeholder="如：北京、上海、London")

    st.markdown("---")
    st.markdown("## 🔥 热门城市")

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
    st.markdown("## 📜 搜索历史")

    if st.session_state.search_history:
        for hist_city in st.session_state.search_history[:5]:
            if st.button(f"🕐 {hist_city}", key=f"hist_{hist_city}"):
                city = hist_city
                st.rerun()
        if st.button("🗑️ 清除历史"):
            st.session_state.search_history = []
            st.rerun()
    else:
        st.caption("暂无搜索历史")

    st.markdown("---")
    st.markdown("## ⚙️ 设置")

    # 主题切换
    theme_option = st.selectbox("🎨 主题模式", ["浅色", "深色"], index=0 if st.session_state.theme == 'light' else 1)
    if theme_option == "深色" and st.session_state.theme != 'dark':
        st.session_state.theme = 'dark'
        st.rerun()
    elif theme_option == "浅色" and st.session_state.theme != 'light':
        st.session_state.theme = 'light'
        st.rerun()

    # 自动刷新
    st.session_state.auto_refresh = st.checkbox("🔄 自动刷新（每5分钟）", value=st.session_state.auto_refresh)

    st.markdown("---")
    st.markdown("### 📊 功能说明")
    st.info("""
    ✅ 实时天气查询
    ✅ 未来7天预报
    ✅ 逐小时预报
    ✅ 体感温度对比
    ✅ 月相显示
    ✅ 导出天气报告
    ✅ 深色/浅色主题
    ✅ 搜索历史记录
    """)

    st.markdown("---")
    st.caption("数据来源: wttr.in")

# ==================== 自动刷新 ====================
if st.session_state.auto_refresh:
    st.toast("🔄 自动刷新已开启，每5分钟更新一次", icon="🔄")
    # 使用 meta 标签实现自动刷新
    st.markdown('<meta http-equiv="refresh" content="300">', unsafe_allow_html=True)

# ==================== 主要查询区域 ====================
if city:
    col1, col2 = st.columns([2, 1])

    with col1:
        with st.spinner(f"🌐 正在查询 {city} 的天气..."):
            data = get_weather_data(city)

            if data:
                try:
                    current = data['current_condition'][0]
                    today = data['weather'][0]

                    # 导出报告按钮
                    report = export_weather_report(city, current, today)
                    st.download_button(
                        label="📄 导出天气报告",
                        data=report,
                        file_name=f"{city}_天气报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )

                    # 城市名称和更新时间
                    st.markdown(f"""
                    <div class="weather-card">
                        <h2 style="text-align:center;">{get_weather_emoji(current['weatherDesc'][0]['value'])} {city}</h2>
                        <p style="text-align:center; color: #888;">更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    # 温度对比卡片
                    st.markdown('<div class="weather-card">', unsafe_allow_html=True)
                    st.markdown("## 🌡️ 温度对比")

                    temp_col1, temp_col2 = st.columns(2)
                    with temp_col1:
                        st.markdown(f'<p class="metric-value">{current["temp_C"]}°C</p>', unsafe_allow_html=True)
                        st.caption("实际温度")
                    with temp_col2:
                        feels_like = current['FeelsLikeC']
                        feels_diff = int(feels_like) - int(current['temp_C'])
                        delta_color = "normal" if feels_diff >= 0 else "inverse"
                        st.metric("体感温度", f"{feels_like}°C", delta=f"{feels_diff:+}°C", delta_color=delta_color)

                    st.markdown("---")

                    # 详细信息网格
                    col_a, col_b, col_c = st.columns(3)

                    with col_a:
                        st.markdown("#### 💧 湿度")
                        st.markdown(f'<p class="metric-value">{current["humidity"]}%</p>', unsafe_allow_html=True)
                        st.markdown("#### 🌬️ 风速")
                        st.markdown(f"{current['windspeedKmph']} km/h")
                        st.caption(current['winddir16Point'])

                    with col_b:
                        st.markdown("#### 🎯 气压")
                        st.markdown(f'<p class="metric-value">{current["pressure"]} mb</p>', unsafe_allow_html=True)
                        st.markdown("#### 👁️ 能见度")
                        st.markdown(f"{current['visibility']} km")

                    with col_c:
                        uv = int(current['uvIndex']) if str(current['uvIndex']).isdigit() else 0
                        uv_text = "低" if uv <= 2 else "中等" if uv <= 5 else "高" if uv <= 7 else "极高"
                        st.markdown("#### ☀️ 紫外线")
                        st.markdown(f'<p class="metric-value">{current["uvIndex"]}</p>', unsafe_allow_html=True)
                        st.caption(uv_text)
                        st.markdown("#### 🌧️ 降水")
                        st.markdown(f"{current['precipMM']} mm")

                    st.markdown("---")

                    # 天气描述和日出日落
                    desc = current['weatherDesc'][0]['value']
                    st.info(f"📝 **天气状况**: {desc}")

                    sun_col1, sun_col2, sun_col3 = st.columns(3)
                    with sun_col1:
                        st.success(f"🌅 日出: {today['astronomy'][0]['sunrise']}")
                    with sun_col2:
                        st.warning(f"🌇 日落: {today['astronomy'][0]['sunset']}")
                    with sun_col3:
                        moon_phase = today.get('astronomy', [{}])[0].get('moon_phase', '未知')
                        st.info(f"{get_moon_icon(moon_phase)} 月相: {moon_phase}")

                    st.markdown('</div>', unsafe_allow_html=True)

                    # 逐小时预报
                    st.markdown('<div class="weather-card">', unsafe_allow_html=True)
                    st.markdown("## ⏰ 逐小时预报（未来12小时）")

                    hourly_data = get_hourly_forecast(data)
                    if hourly_data:
                        # 用表格显示
                        hourly_df = pd.DataFrame(hourly_data)
                        st.dataframe(hourly_df, use_container_width=True, hide_index=True)
                    else:
                        st.info("逐小时数据暂时不可用")

                    st.markdown('</div>', unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"解析数据失败: {str(e)}")
            else:
                st.error(f"❌ 无法获取 {city} 的天气数据")
                st.info("💡 提示: 请检查城市名称是否正确")

    with col2:
        # ==================== 今日预报卡片 ====================
        if data:
            try:
                today = data['weather'][0]

                st.markdown('<div class="weather-card">', unsafe_allow_html=True)
                st.markdown("## 📊 今日概览")

                # 今日温度范围条
                temp_min = int(today['mintempC'])
                temp_max = int(today['maxtempC'])
                temp_current = int(current['temp_C'])

                st.markdown(f"**今日温度范围**")
                st.progress((temp_current - temp_min) / max(1, (temp_max - temp_min)),
                            text=f"{temp_min}°C ← {temp_current}°C → {temp_max}°C")

                # 穿衣建议
                st.markdown("---")
                st.markdown("## 👔 穿衣建议")

                if temp_current < 0:
                    st.error("❄️ 天气寒冷！建议穿羽绒服、厚棉衣、围巾手套")
                elif temp_current < 10:
                    st.warning("🍂 天气较冷！建议穿大衣、毛衣、厚外套")
                elif temp_current < 20:
                    st.info("🌸 天气凉爽！建议穿长袖、薄外套、卫衣")
                elif temp_current < 30:
                    st.success("☀️ 天气舒适！建议穿短袖、衬衫、薄裤")
                else:
                    st.warning("🔥 天气炎热！建议穿短袖、短裤、注意防晒")

                st.markdown('</div>', unsafe_allow_html=True)

            except:
                pass

        # ==================== 未来7天预报 ====================
        if data:
            st.markdown('<div class="weather-card">', unsafe_allow_html=True)
            st.markdown("## 📅 未来7天预报")

            for i, day in enumerate(data['weather'][:7]):
                date_str = day['date']
                try:
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                    weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][date_obj.weekday()]
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
                    - 🌡️ 温度: {temp_min}°C ~ {temp_max}°C
                    - ☁️ 天气: {desc_day}
                    - 🌧️ 降雨概率: {rain_chance}%
                    - 🌅 日出: {day['astronomy'][0]['sunrise']}
                    - 🌇 日落: {day['astronomy'][0]['sunset']}
                    """)

                    # 温度条
                    temp_range = int(temp_max) - int(temp_min)
                    st.progress(min(1.0, temp_range / 30), text=f"温差 {temp_range}°C")

            st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("👆 请在左侧输入或选择城市名称开始查询")

# ==================== 页脚 ====================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: rgba(255,255,255,0.7); padding: 20px;">
    <p>🌈 智能天气查询系统 | 数据实时更新 | 支持全球城市</p>
    <p>Powered by wttr.in & Streamlit | 增强版 v2.0</p>
</div>
""", unsafe_allow_html=True)