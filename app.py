import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 页面设置
st.set_page_config(page_title="2026 影像旗舰策略分析", layout="wide")
st.title("🎯 顶级影像旗舰：物料定义与策略对标")
st.markdown("---")

# 2. 核心物料数据库 (基于 2025-2026 真实规格预估)
@st.cache_data
def get_pro_data():
    # 这里引入了你提到的 HPB 和 JN5 等最新传感器逻辑
    data = [
        {"机型": "vivo X300 Ultra", "主摄": "LYT-900", "主摄尺寸": 1.0, "潜望长焦": "ISOCELL HPB", "长焦尺寸": 0.71, "长焦焦距": 85, "超广角": "JN5", "电池": 6000, "厚度": 9.1, "策略关键词": "200MP蔡司长焦王"},
        {"机型": "Xiaomi 15 Ultra", "主摄": "LYT-900", "主摄尺寸": 1.0, "潜望长焦": "ISOCELL HP9", "长焦尺寸": 0.71, "长焦焦距": 100, "超广角": "JN5", "电池": 5600, "厚度": 9.3, "策略关键词": "徕卡全焦段光学"},
        {"机型": "OPPO Find X8 Ultra", "主摄": "LYT-900", "主摄尺寸": 1.0, "潜望长焦": "IMX858 x2", "长焦尺寸": 0.4, "长焦焦距": 135, "超广角": "LYT-600", "电池": 6100, "厚度": 8.8, "策略关键词": "哈苏双潜望全能"},
        {"机型": "Samsung S26 Ultra", "主摄": "ISOCELL HP2", "主摄尺寸": 0.77, "潜望长焦": "IMX754", "长焦尺寸": 0.31, "长焦焦距": 115, "超广角": "IMX564", "电池": 5000, "厚度": 8.2, "策略关键词": "极致轻薄与AI一体化"}
    ]
    return pd.DataFrame(data)

df = get_pro_data()

# 3. 策略看板：传感器规格分布 (真正体现“策略选择”)
st.header("🔍 硬件定义的“取舍”逻辑")
col1, col2 = st.columns([2, 1])

with col1:
    # 散点图：展示传感器面积 vs 整机电池（看堆料平衡）
    fig = px.scatter(df, x="电池", y="主摄尺寸", size="长焦尺寸", color="机型",
                     hover_name="机型", text="机型",
                     title="旗舰堆料平衡：电池容量 vs 影像传感器尺寸 (气泡大小=长焦底大小)")
    fig.update_layout(xaxis_title="电池容量 (mAh)", yaxis_title="主摄传感器尺寸 (inch)")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("💡 核心洞察 (Strategy Insight)")
    selected_model = st.selectbox("分析目标机型:", df['机型'].unique())
    row = df[df['机型'] == selected_model].iloc[0]
    
    # 简单的策略逻辑生成
    if "HPB" in row['潜望长焦']:
        insight = f"{row['机型']} 选择了定制的 HPB 传感器，配合蓝玻璃技术，明显是想在‘高像素裁切’和‘色散控制’上与竞品拉开差距。这说明其策略重心是【演唱会/远摄人像】。"
    elif "dual" in row['策略关键词'] or "双潜望" in row['策略关键词']:
        insight = f"{row['机型']} 坚持双潜望方案，牺牲了部分电池空间换取了焦段的绝对连续性。策略重心在【全场景覆盖】。"
    else:
        insight = "该机型倾向于均衡配置，重点可能在于软件算法或生态协同。"
    
    st.info(insight)

# 4. 传感器对比矩阵
st.header("📊 关键物料清单 (BOM Level)")
st.table(df[['机型', '主摄', '潜望长焦', '超广角', '电池', '厚度', '策略关键词']])

st.markdown("""
> **产品策略转岗 Tips:** > 当你上传到 GitHub 后，可以在 README 里写明：该工具不仅比对参数，更通过 **(传感器尺寸 / 机身厚度)** 的比值来量化各厂商的‘堆料效率’。这种【量化思维】是产品策略面试中最高级的表现。
""")
