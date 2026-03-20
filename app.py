import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- 1. 页面专业化配置 ---
st.set_page_config(page_title="Ultra-Flagship Strategy Lab 2026", layout="wide", initial_sidebar_state="collapsed")

# 自定义 CSS 提升视觉高级感
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    h1, h2 { color: #1e293b; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 核心物料策略数据库 (2026 最新行业口径) ---
@st.cache_data
def get_industry_data():
    # 逻辑：传感器面积按 inch 换算成近似 mm² 以便量化
    data = [
        {"机型": "vivo X300 Ultra", "主摄": "LYT-900(1\")", "长焦": "HPB(1/1.4\")", "超广角": "JN5", "电池": 6000, "重量": 225, "厚度": 9.1, "影像分": 98, "策略": "极致长焦"},
        {"机型": "Xiaomi 15 Ultra", "主摄": "LYT-900(1\")", "长焦": "HP9(1/1.4\")", "超广角": "JN5", "电池": 5600, "重量": 229, "厚度": 9.3, "影像分": 96, "策略": "全焦段光学"},
        {"机型": "Find X8 Ultra", "主摄": "LYT-900(1\")", "长焦": "IMX858 x2", "超广角": "LYT-600", "电池": 6100, "重量": 221, "厚度": 8.8, "影像分": 94, "策略": "双潜望平衡"},
        {"机型": "S26 Ultra", "主摄": "HP2(1/1.3\")", "长焦": "IMX754", "超广角": "IMX564", "电池": 5000, "重量": 210, "厚度": 8.2, "影像分": 85, "策略": "轻薄AI旗舰"}
    ]
    df = pd.DataFrame(data)
    # 计算核心指标：堆料密度 (影像分 / 厚度)
    df['堆料效率'] = (df['影像分'] / df['厚度']).round(2)
    return df

df = get_industry_data()

# --- 3. 顶部 Executive Summary ---
st.title("🛡️ 2026 影像旗舰产品策略分析系统")
st.markdown("针对 **vivo / 小米 / OPPO** 顶峰机型的技术取舍与供应链能力建模")

m1, m2, m3, m4 = st.columns(4)
m1.metric("行业平均电池", f"{int(df['电池'].mean())} mAh", "↑ 200 vs 2025")
m2.metric("主流主摄规格", "1.0-inch LYT-900")
m3.metric("长焦天花板", "ISOCELL HPB", "定制蓝玻璃")
m4.metric("策略趋势", "轻薄化影像")

st.markdown("---")

# --- 4. 核心逻辑：Trade-off 象限图 ---
tab1, tab2 = st.tabs(["📊 竞争格局象限", "📑 详细物料对标"])

with tab1:
    col_left, col_right = st.columns([3, 1])
    
    with col_left:
        # 逻辑：X轴是便携性（重量反比），Y轴是影像能力
        fig = px.scatter(df, x="重量", y="影像分", size="电池", color="机型",
                         text="机型", title="产品定义：性能天花板 vs 物理极限 (气泡大小=电池容量)",
                         labels={"影像分": "影像能力建模得分", "重量": "整机重量 (g)"},
                         range_x=[200, 240], range_y=[80, 105])
        
        # 添加象限中线
        fig.add_hline(y=df['影像分'].mean(), line_dash="dash", line_color="gray", annotation_text="行业均值")
        fig.add_vline(x=df['重量'].mean(), line_dash="dash", line_color="gray")
        
        fig.update_traces(textposition='top center', marker=dict(line=dict(width=2, color='DarkSlateGrey')))
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("💡 竞争态势速递")
        st.write("**右上象限 (Powerhouse):** 极致堆料，代表 vivo 与小米。策略是以重量换取绝对的影像制高点。")
        st.write("**左下象限 (Efficiency):** 三星策略，放弃极致硬件，主打 AI 和极致手感。")
        st.warning("关键洞察：vivo X300 Ultra 在更轻的重量下实现了更高的影像分，体现了定制 HPB 传感器带来的‘高能量密度’优势。")

# --- 5. 详细物料与“推演模拟” ---
with tab2:
    st.subheader("核心 BOM 清单与策略标签")
    
    # 格式化表格显示
    styled_df = df.style.background_gradient(subset=['堆料效率'], cmap='Greens')
    st.table(styled_df)

    # 策略推演模块
    st.markdown("### 🛠️ 产品定义推演 (Sandbox)")
    with st.expander("如果你是 vivo 的 Product Manager，该如何平衡 X400 的定义？"):
        target_battery = st.slider("目标电池容量 (mAh)", 5000, 7000, 6000)
        target_sensor = st.select_slider("主摄传感器级别", options=["1/1.3\"", "1.0-inch", "1.1-inch (Next Gen)"])
        
        # 模拟计算逻辑
        est_thickness = 8.0 + (target_battery - 5000)/500 + (0.5 if "1.1" in target_sensor else 0)
        est_weight = 200 + (target_battery - 5000)/20 + (10 if "1.1" in target_sensor else 0)
        
        c1, c2 = st.columns(2)
        c1.metric("预估整机厚度", f"{est_thickness:.2f} mm")
        c2.metric("预估整机重量", f"{est_weight:.1f} g")
        
        if est_weight > 235:
            st.error("⚠️ 警告：整机重量超过 235g，属于‘坠手’级别，营销端极难转化，建议缩减主摄规格或引入新材料。")
        else:
            st.success("✅ 策略可行：该配置在当前供应链能力下可实现平衡。")

# --- 6. 底部注脚 ---
st.markdown("---")
st.caption("Internal Strategy Tool © 2026 | 基于 GitHub 与 Streamlit Cloud 构建 | 专注于移动影像产品逻辑拆解")
