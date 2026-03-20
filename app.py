import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- 1. 页面专业化配置 ---
st.set_page_config(page_title="Ultra-Flagship Strategy Lab 2026", layout="wide")

# --- 2. 核心物料数据库 (2026 最新行业口径) ---
@st.cache_data
def get_industry_data():
    data = [
        {"机型": "vivo X300 Ultra", "影像得分": 98, "续航得分": 92, "手感得分": 85, "屏幕得分": 95, "性能得分": 98, "电池": 6000, "重量": 225, "厚度": 9.1, "主摄": "LYT-900", "长焦": "HPB"},
        {"机型": "Xiaomi 15 Ultra", "影像得分": 96, "续航得分": 88, "手感得分": 82, "屏幕得分": 97, "性能得分": 99, "电池": 5600, "重量": 229, "厚度": 9.3, "主摄": "LYT-900", "长焦": "HP9"},
        {"机型": "Find X8 Ultra", "影像得分": 94, "续航得分": 95, "手感得分": 88, "屏幕得分": 94, "性能得分": 97, "电池": 6100, "重量": 221, "厚度": 8.8, "主摄": "LYT-900", "长焦": "IMX858 x2"},
        {"机型": "S26 Ultra", "影像得分": 85, "续航得分": 82, "手感得分": 95, "屏幕得分": 99, "性能得分": 96, "电池": 5000, "重量": 210, "厚度": 8.2, "主摄": "HP2", "长焦": "IMX754"}
    ]
    return pd.DataFrame(data)

df = get_industry_data()

# --- 3. 顶部导航与全局指标 ---
st.title("🛡️ 2026 影像旗舰产品策略推演系统")
st.markdown("从**产品定义**视角出发，量化分析 vivo 与竞品的战略取舍")

# --- 4. 功能分区 (使用 Tabs 切换) ---
tab_radar, tab_quadrant, tab_vertical, tab_sandbox = st.tabs([
    "🎯 产品基因雷达 (DNA)", 
    "📊 竞争格局象限", 
    "📈 垂直参数对标", 
    "🛠️ 定义推演沙盒"
])

# --- Tab 1: 雷达图 (展示单个产品的平衡感) ---
with tab_radar:
    st.subheader("机型战略基因图谱")
    target_model = st.selectbox("选择要分析的机型", df['机型'].unique())
    model_data = df[df['机型'] == target_model].iloc[0]
    
    categories = ['影像得分', '续航得分', '手感得分', '屏幕得分', '性能得分']
    
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=[model_data[c] for c in categories],
        theta=categories,
        fill='toself',
        name=target_model,
        line_color='#0052D4'
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[80, 100])),
        showlegend=False,
        title=f"{target_model} 的综合产品力分布"
    )
    st.plotly_chart(fig_radar, use_container_width=True)

# --- Tab 2: 象限图 (保留原有能力) ---
with tab_quadrant:
    st.subheader("影像能力 vs. 物理极限 象限分析")
    fig_q = px.scatter(df, x="重量", y="影像得分", size="电池", color="机型",
                       text="机型", hover_data=['厚度'],
                       range_x=[200, 240], range_y=[80, 105])
    fig_q.add_hline(y=df['影像得分'].mean(), line_dash="dash", line_color="red")
    fig_q.add_vline(x=df['重量'].mean(), line_dash="dash", line_color="green")
    st.plotly_chart(fig_q, use_container_width=True)

# --- Tab 3: 垂直对比图 (新增需求) ---
with tab_vertical:
    st.subheader("关键硬件参数垂直对标")
    compare_attr = st.segmented_control(
        "选择对比维度", 
        options=["电池", "重量", "厚度", "影像得分"], 
        default="电池"
    )
    
    fig_v = px.bar(df.sort_values(compare_attr), x="机型", y=compare_attr, 
                   color="机型", text_auto=True,
                   title=f"各旗舰机型 {compare_attr} 垂直对比 (升序)")
    fig_v.update_layout(showlegend=False)
    st.plotly_chart(fig_v, use_container_width=True)

# --- Tab 4: 推演沙盒 (保留原有能力) ---
with tab_sandbox:
    st.subheader("Product Manager 决策模拟器")
    c1, c2 = st.columns([1, 2])
    with c1:
        target_bat = st.slider("目标电池 (mAh)", 5000, 7000, 6000)
        target_cam = st.radio("主摄方案", ["1/1.3\" (轻薄型)", "1.0\" (专业型)", "1.1\" (突破型)"])
    
    with c2:
        # 简单建模逻辑
        base_thick = 8.0 + (target_bat - 5000)/500
        cam_thick = 0.5 if "1.0" in target_cam else (1.2 if "1.1" in target_cam else 0)
        final_thick = base_thick + cam_thick
        
        st.metric("预估整机厚度", f"{final_thick:.2f} mm")
        if final_thick > 9.5:
            st.error("❌ 警告：厚度超过 9.5mm，用户握持感将严重下滑，建议削减规格。")
        else:
            st.success("✅ 策略建议：该厚度在顶级旗舰中属于竞争优势范围。")

# --- 5. 底部数据矩阵 ---
st.markdown("---")
st.dataframe(df[['机型', '主摄', '长焦', '电池', '重量', '厚度']], use_container_width=True)
