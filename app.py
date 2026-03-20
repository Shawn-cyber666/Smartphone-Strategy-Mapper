import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. 页面配置与标题
st.set_page_config(page_title="Smartphone Product Strategy Tracker", layout="wide")
st.title("📱 核心竞品演进追踪器 (离线策略版)")
st.markdown("设计目的：跳出单点参数对比，从时间维度拆解各厂产品定义的取舍逻辑与技术演进路径。")

# 2. 模拟本地数据库 (在实际使用中，你可以替换为读取本地 CSV 文件)
# 预埋了典型的影像旗舰演进路线和关键传感器数据
@st.cache_data
def load_data():
    data = {
        "Brand": ["vivo", "vivo", "vivo", "Xiaomi", "Xiaomi", "OPPO", "OPPO"],
        "Model": ["X100 Ultra", "X200 Ultra", "X300 Ultra", "14 Ultra", "15 Ultra", "Find X7 Ultra", "Find X8 Ultra"],
        "Generation": ["Gen 1", "Gen 2", "Gen 3", "Gen 1", "Gen 2", "Gen 1", "Gen 2"],
        "Main_Sensor": ["LYT-900", "LYT-900", "HPB", "LYT-900", "LYT-900", "LYT-900", "LYT-900"],
        "Main_Sensor_Size_inch": [1.0, 1.0, 1.1, 1.0, 1.0, 1.0, 1.0], # 数值越大底越大
        "Telephoto_Sensor": ["HP9", "HP9", "HPB", "IMX858", "IMX858", "IMX890", "JN1"],
        "Telephoto_Focal_Length_mm": [85, 85, 100, 75, 120, 65, 73],
        "Battery_mAh": [5500, 5800, 6000, 5300, 5500, 5000, 5400],
        "Weight_g": [229, 225, 220, 224, 226, 221, 215],
        "Strategy_Tag": ["演唱会神器", "全焦段人像", "超大底跨界", "徕卡光学", "双长焦影像", "双潜望生态", "轻薄影像"]
    }
    return pd.DataFrame(data)

df = load_data()

# 3. 侧边栏交互：选择要对比的品牌
st.sidebar.header("策略筛选器")
selected_brands = st.sidebar.multiselect("选择对比品牌:", df['Brand'].unique(), default=["vivo", "Xiaomi"])

filtered_df = df[df['Brand'].isin(selected_brands)]

# 4. 主看板逻辑
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔋 核心取舍逻辑：电池容量 vs 整机重量")
    st.markdown("产品洞察：观察竞品是在追求极致堆料（重/大电池），还是在做减法（轻量化）。")
    # 气泡图：X轴重量，Y轴电池，气泡大小为传感器尺寸
    fig_tradeoff = px.scatter(filtered_df, x="Weight_g", y="Battery_mAh", color="Brand",
                              size="Main_Sensor_Size_inch", text="Model",
                              hover_data=["Strategy_Tag"])
    fig_tradeoff.update_traces(textposition='top center')
    st.plotly_chart(fig_tradeoff, use_container_width=True)

with col2:
    st.subheader("📷 影像演进路径：长焦焦距变化")
    st.markdown("产品洞察：拆解各家对中长焦距的定义（如人像黄金焦段 vs 演唱会超长焦）。")
    # 折线图：展示不同代际的焦距演进
    fig_telephoto = px.line(filtered_df, x="Generation", y="Telephoto_Focal_Length_mm", 
                            color="Brand", markers=True, text="Telephoto_Sensor")
    fig_telephoto.update_traces(textposition='bottom right')
    st.plotly_chart(fig_telephoto, use_container_width=True)

# 5. 详细数据矩阵
st.subheader("📊 核心物料与策略标签矩阵")
st.dataframe(filtered_df[['Brand', 'Model', 'Main_Sensor', 'Telephoto_Sensor', 'Strategy_Tag']], use_container_width=True)

# 6. 策略总结生成器 (基于规则的本地化洞察)
st.subheader("💡 自动化策略洞察 (Rule-based Insights)")
if "vivo" in selected_brands and "Xiaomi" in selected_brands:
    st.info("**竞品动态预警 (vivo vs 小米):**\n\n从数据演进可见，小米在长焦端坚持使用小底（如 IMX858）做高倍率，而我们一直倾向于用大底（如 HP 系列）保画质。下一步策略重点应放在**大底长焦的暗光表现**上，这属于竞品的物理盲区。")
