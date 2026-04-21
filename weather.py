"""
Streamlit 天气查询应用
使用 conda 安装的 streamlit 运行
"""

import streamlit as st
import requests
from datetime import datetime
import json

# 页面配置
st.set_page_config(
    page_title="天气查询系统",
    page_icon="🌈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .main-header {
        text-align: center;
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .weather-card {
        background: rgba(255,255,255,0.95);
        border-radius: 20px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 5px 20px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# 标题
st.markdown("""
<div class="main-header">
    <h1>🌈 智能天气查询系统</h1>
    <p>实时天气 | 精准预报 | 贴心建议</p>
</div>
""", unsafe_allow_html=True)

# 侧边栏
with st.sidebar:
    st.markdown("## 🎯 城市选择")

    # 城市输入
    city = st.text_input("请输入城市名称", value="北京", placeholder="如：北京、上海、London")

    st.markdown("---")
    st.markdown("## 🔥 热门城市")

    # 热门城市按钮
    hot_cities = ['北京', '上海', '广州', '深圳', '杭州', '成都', '重庆', '武汉', '西安', '南京']

    # 创建两列按钮
    cols = st.columns(2)
    for i, city_name in enumerate(hot_cities):
        if cols[i % 2].button(city_name, key=f"btn_{city_name}", use_container_width=True):
            city = city_name
            st.rerun()

    st.markdown("---")
    st.markdown("### 📊 功能说明")
    st.info("""
    ✅ 实时天气查询
    ✅ 未来3天预报
    ✅ 温度、湿度、风速
    ✅ 日出日落时间
    ✅ 降雨概率
    """)

    st.markdown("---")
    st.caption("数据来源: wttr.in")
    st.caption("实时更新，准确可靠")

# 主要区域
if city:
    # 创建两列布局
    col1, col2 = st.columns([2, 1])

    with col1:
        with st.spinner(f"🌐 正在查询 {city} 的天气..."):
            try:
                # 获取天气数据
                url = f"https://wttr.in/{city}?format=j1&lang=zh"
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(url, headers=headers, timeout=10)
                data = response.json()

                # 解析数据
                current = data['current_condition'][0]
                today = data['weather'][0]

                # 显示城市名称
                st.markdown(f"""
                <div class="weather-card">
                    <h2 style="text-align:center; color:#667eea;">🌍 {city}</h2>
                    <p style="text-align:center; color:#666;">更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
                """, unsafe_allow_html=True)

                # 主要天气信息
                st.markdown('<div class="weather-card">', unsafe_allow_html=True)

                # 温度和大图标
                temp_col1, temp_col2, temp_col3 = st.columns(3)
                with temp_col1:
                    st.metric("🌡️ 当前温度", f"{current['temp_C']}°C",
                              delta=f"体感 {current['FeelsLikeC']}°C")
                with temp_col2:
                    st.metric("📈 今日最高", f"{today['maxtempC']}°C")
                with temp_col3:
                    st.metric("📉 今日最低", f"{today['mintempC']}°C")

                st.markdown("---")

                # 详细信息
                col_a, col_b, col_c = st.columns(3)

                with col_a:
                    st.markdown("#### 💧 湿度")
                    st.markdown(f"<h2 style='text-align:center'>{current['humidity']}%</h2>",
                                unsafe_allow_html=True)
                    st.markdown("#### 🌬️ 风速")
                    st.markdown(
                        f"<p style='text-align:center'>{current['windspeedKmph']} km/h<br>{current['winddir16Point']}</p>",
                        unsafe_allow_html=True)

                with col_b:
                    st.markdown("#### 🎯 气压")
                    st.markdown(f"<h2 style='text-align:center'>{current['pressure']} mb</h2>",
                                unsafe_allow_html=True)
                    st.markdown("#### 👁️ 能见度")
                    st.markdown(f"<p style='text-align:center'>{current['visibility']} km</p>",
                                unsafe_allow_html=True)

                with col_c:
                    st.markdown("#### ☀️ 紫外线")
                    uv = int(current['uvIndex']) if current['uvIndex'].isdigit() else 0
                    uv_text = "低" if uv <= 2 else "中等" if uv <= 5 else "高" if uv <= 7 else "极高"
                    st.markdown(f"<h2 style='text-align:center'>{current['uvIndex']} ({uv_text})</h2>",
                                unsafe_allow_html=True)
                    st.markdown("#### 🌧️ 降水")
                    st.markdown(f"<p style='text-align:center'>{current['precipMM']} mm</p>",
                                unsafe_allow_html=True)

                st.markdown("---")

                # 天气描述
                desc = current['weatherDesc'][0]['value']
                st.info(f"📝 **天气状况**: {desc}")

                # 日出日落
                sun_col1, sun_col2 = st.columns(2)
                with sun_col1:
                    st.success(f"🌅 日出: {today['astronomy'][0]['sunrise']}")
                with sun_col2:
                    st.warning(f"🌇 日落: {today['astronomy'][0]['sunset']}")

                st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ 查询失败: {str(e)}")
                st.info("💡 提示: 请检查城市名称是否正确，或网络连接是否正常")

    with col2:
        # 天气预报
        st.markdown('<div class="weather-card">', unsafe_allow_html=True)
        st.markdown("## 📅 未来3天预报")

        try:
            # 获取预报数据
            url = f"https://wttr.in/{city}?format=j1&lang=zh"
            response = requests.get(url, headers=headers, timeout=10)
            data = response.json()

            # 显示未来3天预报
            for i, day in enumerate(data['weather'][:3]):
                date = day['date']
                temp_max = day['maxtempC']
                temp_min = day['mintempC']
                desc_day = day['hourly'][0]['weatherDesc'][0]['value']
                rain_chance = day['hourly'][0]['chanceofrain']

                with st.expander(f"📆 {date}", expanded=(i == 0)):
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

        except Exception as e:
            st.error(f"获取预报失败: {e}")

        st.markdown('</div>', unsafe_allow_html=True)

        # 穿衣建议（根据温度）
        try:
            temp = int(current['temp_C'])
            st.markdown('<div class="weather-card">', unsafe_allow_html=True)
            st.markdown("## 👔 穿衣建议")

            if temp < 0:
                st.error(f"❄️ 今日 {temp}°C，天气寒冷！建议穿羽绒服、厚棉衣、围巾手套")
            elif temp < 10:
                st.warning(f"🍂 今日 {temp}°C，天气较冷！建议穿大衣、毛衣、厚外套")
            elif temp < 20:
                st.info(f"🌸 今日 {temp}°C，天气凉爽！建议穿长袖、薄外套、卫衣")
            elif temp < 30:
                st.success(f"☀️ 今日 {temp}°C，天气舒适！建议穿短袖、衬衫、薄裤")
            else:
                st.warning(f"🔥 今日 {temp}°C，天气炎热！建议穿短袖、短裤、注意防晒")

            st.markdown('</div>', unsafe_allow_html=True)
        except:
            pass

else:
    st.info("👆 请在左侧输入或选择城市名称开始查询")

# 页脚
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: rgba(255,255,255,0.7); padding: 20px;">
    <p>🌈 智能天气查询系统 | 数据实时更新 | 支持全球城市</p>
    <p>Powered by wttr.in & Streamlit</p>
</div>
""", unsafe_allow_html=True)