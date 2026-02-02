import streamlit as st
import sqlite3
import uuid
import datetime
import os
import time

# ==========================================
# 1. 全局配置
# ==========================================
st.set_page_config(
    page_title="80后老登的工具箱 | AI.Fun",
    page_icon="🦕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 初始化所有状态
for key, default in {
    'language': 'zh',
    'coffee_num': 1
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ==========================================
# 2. 自动检测浏览器语言
# ==========================================
def detect_browser_language():
    try:
        headers = st.context.headers
        accept_language = headers.get('Accept-Language', 'zh')
        lang_codes = re.findall(r'([a-z]{2})(?:-[A-Z]{2})?', accept_language.lower())
        if 'zh' in lang_codes: return 'zh'
        elif 'en' in lang_codes: return 'en'
        else: return 'zh'
    except: return 'zh'

if 'lang' not in st.session_state:
    st.session_state.lang = detect_browser_language()

# ==========================================
# 2. 多语言文本配置 (已增强，补充3个新应用)
# ==========================================
lang_texts = {
    'zh': {
        'page_title': '80后老登的工具箱',
        'subtitle': '守住底裤的 AI 网页小应用',
        'footer_title': '关于本站',
        'footer_text': '这里收录了我这些年做的一系列小玩意儿。它们算不上什么实用的东西，但玩起来都还挺有意思的。',
        'footer_btn2': '关注老登公众号 🐦',
        'footer_btn3': '请老登一杯咖啡 ☕', 
        'qrcode_desc': '第一时间获取最新应用更新',
        # --- 咖啡新逻辑专用文本 ---
        'custom_count': '自定义数量 (杯)',
        'total_label': '总计投入',
        'paid_btn': '🎉 我已支付，给老登打气！',
        'paid_toast': '收到！感谢你的 {count} 杯咖啡！代码写得更有劲了！❤️',
        'presets': [("☕ 提神", "由衷感谢"), ("🍗 鸡腿", "动力加倍"), ("🚀 续命", "老登不朽")],


        "coffee_btn": "☕ 请开发者喝咖啡",
        "coffee_title": " ",
        "coffee_desc": "如果这个小游戏让你摸鱼更快乐，欢迎投喂！",
        "pay_wechat": "微信支付",
        "pay_alipay": "支付宝",
        "pay_paypal": "PayPal",
        "unit_cn": "杯",
        "unit_total": "总计投入",
        "pay_success": "收到！感谢打赏。代码写得更有劲了！❤️",
        "pay_choose": "选择支付方式",
        "coffee_amount": "请输入打赏杯数",
        # -----------------------
        'games': [
            ("财富榜", "我能排第几", "💰", "https://youqian.streamlit.app/"),
            ("AI兔子", "一键检测AI内容痕迹", "🐰", "https://aituzi.streamlit.app/"),
            ("巴菲特", "伯克希尔投资演变", "📈", "https://buffett.streamlit.app/"),
            ("染红", "国资投资A股可视化", "🔴", "https://ranhong.streamlit.app/"),
            ("世界房价", "世界城市房价对比", "🌍", "https://fangchan.streamlit.app/"),
            ("中国房市", "城区房市价格趋势", "🏙️", "https://fangjia.streamlit.app/"),
            ("百万投资", "顶尖理财回报对比", "💹", "https://nblawyer.streamlit.app/"),
            ("国际律师", "全球AI法律咨询", "⚖️", "https://chuhai.streamlit.app/"),
            ("Legal1000", "全球合规机构导航", "📚", "https://iterms.streamlit.app/"),
            # 新增3个应用 - 中文配置
            ("生死观测台", "生命状态监测查询", "⚰️", "https://baobei.streamlit.app/"),
            ("花光三马的钱", "模拟消耗巨额财富", "💸", "https://mababa.streamlit.app/"),
            ("国宝私有化", "中国文物私有化大拍卖", "🏺", "https://bowuguan.streamlit.app/"),
            # 新增3个应用 - 中文配置
            ("为什么要抓马杜罗", "委内瑞拉的石油和毒品", "🛢️", "https://venezuela.streamlit.app/"),  # 🌍 对应国家、地缘政治主题
            ("MBTI对话助手", "用AI对付MBTI", "🧠", "https://mbtibot.streamlit.app/"),  # 🧠 对应人格、AI对话核心功能
            ("MBTI亿万富翁", "我的性格怎么发财", "🧬", "https://1000000.streamlit.app/")  # 💰 直接关联财富、发财主题
        ]
    },
    'en': {
        'page_title': 'AI.Fun',
        'subtitle': 'Silly but fun AI web apps',
        'footer_title': 'About this site',
        'footer_text': 'A collection of silly little projects. Not particularly useful, but fun to play with.',
        'footer_btn2': 'Follow Me 🐦',
        'footer_btn3': 'Support Me ☕',
        'qrcode_desc': 'Get the latest app updates',
        # --- 咖啡新逻辑专用文本 ---
        'custom_count': 'Custom count (cups)',
        'total_label': 'Total',
        'paid_btn': '🎉 I have paid!',
        'paid_toast': 'Received! Thanks for the {count} coffees! ❤️',

        "coffee_btn": "☕ Buy me a coffee",
        "coffee_title": " ",
        "coffee_desc": "If you enjoyed this, consider buying me a coffee!",
        "pay_wechat": "WeChat Pay",
        "pay_alipay": "Alipay",
        "pay_paypal": "PayPal",
        "unit_cn": "Cups",
        "unit_total": "Total",
        "pay_success": "Received! Thanks for the coffee! ❤️",
        "pay_choose": "Choose Payment Method",
        "coffee_amount": "Enter Coffee Count",

        
        # -----------------------
        'games': [
            ("Wealth", "Where do I stand?", "💰", "https://youqian.streamlit.app/"),
            ("AI Rabbit", "Content detection", "🐰", "https://aituzi.streamlit.app/"),
            ("Buffett", "Investment evolution", "📈", "https://buffett.streamlit.app/"),
            ("Red Stain", "State investment", "🔴", "https://ranhong.streamlit.app/"),
            ("Housing", "Global price comparison", "🌍", "https://fangchan.streamlit.app/"),
            ("China Home", "Urban price trends", "🏙️", "https://fangjia.streamlit.app/"),
            ("Million Invest", "Financial returns", "💹", "https://nblawyer.streamlit.app/"),
            ("AI Lawyer", "Global legal consultation", "⚖️", "https://chuhai.streamlit.app/"),
            ("Legal1000", "Global Compliance", "📚", "https://iterms.streamlit.app/"),
            # 新增3个应用 - 英文配置（保持功能对应，符合英文用户认知）
            ("Life & Death Observer", "Life status monitoring & inquiry", "⚰️", "https://baobei.streamlit.app/"),
            ("Spend Three Tycoons' Wealth", "Simulate spending huge wealth", "💸", "https://mababa.streamlit.app/"),
            ("National Treasure Privatization", "Cultural relic ownership simulation", "🏺", "https://bowuguan.streamlit.app/"),
            ("Why arrest Maduro?", "Venezuela's oil and drugs", "🛢️", "https://venezuela.streamlit.app/"),
            ("MBTI Chat Assistant", "AI-powered MBTI interactions", "🧠", "https://mbtibot.streamlit.app/"),
            ("MBTI Billionaire", "How my personality leads to wealth", "🧬", "https://1000000.streamlit.app/")
        ]
    }
}
current_text = lang_texts[st.session_state.language]

if 'coffee_num' not in st.session_state: st.session_state.coffee_num = 1
if 'payment_method' not in st.session_state: st.session_state.payment_method = 'wechat'

# ==========================================
# 3. 核心 CSS (合并了咖啡卡片样式)
# ==========================================
st.markdown(f"""
<style>
    /* 基础重置 */
    .stApp {{ background-color: #FFFFFF !important; }}
    .block-container {{ padding-top: 2rem; max-width: 1000px !important; }}
    #MainMenu, footer, header {{visibility: hidden;}}
    .stDeployButton {{display: none;}}
    /* 标题排版 */
    .main-title {{
        text-align: center; font-size: 3.5rem; font-weight: 900;
        letter-spacing: -0.1rem; color: #111; margin-bottom: 0.5rem;
    }}
    .subtitle {{
        text-align: center; font-size: 1.25rem; color: #666;
        margin-bottom: 3.5rem; font-weight: 400;
    }}
    /* Neal.fun 风格卡片 */
    .neal-card {{
        background: white; border-radius: 16px; padding: 1.5rem;
        height: 120px; border: 1px solid #e5e7eb;
        display: flex; align-items: center; gap: 1.2rem;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        text-decoration: none !important; margin-bottom: 1rem;
    }}
    .neal-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.06);
        border-color: #d1d5db;
    }}
    .card-icon {{ font-size: 2.5rem; }}
    .card-title {{ font-weight: 700; font-size: 1.15rem; color: #111; }}
    .card-desc {{ font-size: 0.9rem; color: #6b7280; margin-top: 2px; }}
    /* Footer 按钮样式 */
    .stButton > button {{
        background: white !important; border: 1px solid #e5e7eb !important;
        border-radius: 10px !important; padding: 0.5rem 1rem !important;
        font-weight: 600 !important; transition: all 0.2s !important;
        width: 100%;
    }}
    .stButton > button:hover {{
        background: #f9fafb !important; transform: translateY(-1px);
    }}
    /* --- ☕ 咖啡打赏 2.0 专用样式 --- */
    .coffee-card {{
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border: 1px solid #e5e7eb; border-radius: 16px;
        padding: 5px; box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        margin-bottom: 5px; text-align: center;
    }}
    .price-tag-container {{
        background: #fff0f0; border: 1px dashed #ffcccc;
        border-radius: 12px; padding: 10px; text-align: center;
        margin-top: 5px; transition: all 0.3s;
    }}
    .price-tag-container:hover {{ transform: scale(1.02); }}
    .price-label {{ color: #888; font-size: 0.8rem; margin-bottom: 2px; }}
    .price-number {{ color: #d9534f; font-weight: 900; font-size: 1.8rem; }}
    /* 统计容器 */
    .metric-container {{
        display: flex; justify-content: center; gap: 2rem;
        margin-top: 4rem; padding: 2rem 0;
        border-top: 1px solid #f3f4f6;
        color: #9ca3af; font-size: 0.85rem;
    }}
    .plant-container {{ position: fixed; bottom: 30px; right: 30px; z-index: 100; }}

    
    /* =================================================================
       New Styles: Unified Payment Card Layout
       ================================================================= */
    .pay-card {{
        background: #fdfdfd;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-top: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }}
    .pay-amount-display {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.8rem;
        font-weight: 800;
        margin: 10px 0;
    }}
    .pay-label {{
        font-size: 0.85rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 5px;
    }}
    .pay-instruction {{
        font-size: 0.8rem;
        color: #94a3b8;
        margin-top: 15px;
        margin-bottom: 5px;
    }}
    
    /* Colors for different payment methods */
    .color-wechat {{ color: #2AAD67; }}
    .color-alipay {{ color: #1677ff; }}
    .color-paypal {{ color: #003087; }}
    
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. 数据库与统计逻辑
# ==========================================
DB_DIR = os.path.expanduser("~/")
DB_FILE = os.path.join(DB_DIR, "visit_stats.db")

def init_db():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS daily_traffic (date TEXT PRIMARY KEY, pv_count INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS visitors (visitor_id TEXT PRIMARY KEY, first_visit_date TEXT)''')
    c.execute("PRAGMA table_info(visitors)")
    columns = [info[1] for info in c.fetchall()]
    if "last_visit_date" not in columns:
        try:
            c.execute("ALTER TABLE visitors ADD COLUMN last_visit_date TEXT")
            c.execute("UPDATE visitors SET last_visit_date = first_visit_date WHERE last_visit_date IS NULL")
        except:
            pass
    conn.commit()
    conn.close()

def get_visitor_id():
    if "visitor_id" not in st.session_state:
        st.session_state["visitor_id"] = str(uuid.uuid4())
    return st.session_state["visitor_id"]

def track_and_get_stats():
    init_db()
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = conn.cursor()
    today_str = datetime.datetime.utcnow().date().isoformat()
    visitor_id = get_visitor_id()
    if "has_counted" not in st.session_state:
        try:
            c.execute("INSERT OR IGNORE INTO daily_traffic (date, pv_count) VALUES (?, 0)", (today_str,))
            c.execute("UPDATE daily_traffic SET pv_count = pv_count + 1 WHERE date=?", (today_str,))
            c.execute("SELECT visitor_id FROM visitors WHERE visitor_id=?", (visitor_id,))
            if c.fetchone():
                c.execute("UPDATE visitors SET last_visit_date=? WHERE visitor_id=?", (today_str, visitor_id))
            else:
                c.execute("INSERT INTO visitors (visitor_id, first_visit_date, last_visit_date) VALUES (?, ?, ?)", 
                          (visitor_id, today_str, today_str))
            conn.commit()
            st.session_state["has_counted"] = True
        except Exception as e:
            st.error(f"DB Error: {e}")
    c.execute("SELECT COUNT(*) FROM visitors WHERE last_visit_date=?", (today_str,))
    today_uv = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM visitors")
    total_uv = c.fetchone()[0]
    c.execute("SELECT pv_count FROM daily_traffic WHERE date=?", (today_str,))
    res_pv = c.fetchone()
    today_pv = res_pv[0] if res_pv else 0
    conn.close()
    return today_uv, total_uv, today_pv

# ==========================================
# 5. 弹窗逻辑 (含升级版咖啡打赏)
# ==========================================
# --- 公众号弹窗 ---
@st.dialog("扫码关注，获取新应用")
def show_qrcode_window():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if os.path.exists("qrcode_for_gh.jpg"):
            st.image("qrcode_for_gh.jpg", use_container_width=True)
        else:
            st.info("请放置 qrcode_for_gh.jpg")
    st.markdown(f"""
        <div style='text-align:center; margin-top:10px; color:#666;'>
            {lang_texts[st.session_state.language]['qrcode_desc']}
        </div>
    """, unsafe_allow_html=True)
    if st.button("完成", use_container_width=True):
        st.rerun()

# --- 咖啡赞赏弹窗 (升级版 V2.0) ---
 @st.dialog(" " + get_txt('coffee_title'), width="small")
    def show_coffee_window():
        st.markdown(f"""<div style="text-align:center; color:#666; margin-bottom:15px;">{get_txt('coffee_desc')}</div>""", unsafe_allow_html=True)
        
        # 快捷按钮
        presets = [("☕", 1), ("🍗", 3), ("🚀", 5)]
        def set_val(n): st.session_state.coffee_num = n
        cols = st.columns(3, gap="small")
        for i, (icon, num) in enumerate(presets):
            with cols[i]:
                if st.button(f"{icon} {num}", use_container_width=True, key=f"p_btn_{i}"): set_val(num)
        st.write("")

        # 输入与计算
        col_amount, col_total = st.columns([1, 1], gap="small")
        with col_amount: 
            cnt = st.number_input(get_txt('coffee_amount'), 1, 100, step=1, key='coffee_num')
        
        cny_total = cnt * 10
        usd_total = cnt * 2
        
        #with col_total: 
        #    st.markdown(f"""<div style="background:#fff1f2; border-radius:8px; padding:8px; text-align:center; color:#e11d48; font-weight:bold; font-size:1.5rem; height: 100%; display: flex; align-items: center; justify-content: center;">¥{cny_total}</div>""", unsafe_allow_html=True)
                
        # 4. 统一支付卡片渲染函数 (核心复用逻辑)
        def render_pay_tab(title, amount_str, color_class, img_path, qr_data_suffix, link_url=None):
            # 使用 st.container 并开启 border 边框
            with st.container(border=True):
                # 卡片头部 (包含支付名称和金额)
                st.markdown(f"""
                    <div style="text-align: center; padding-bottom: 10px;">
                        <div class="pay-label {color_class}" style="margin-bottom: 5px;">{title}</div>
                        <div class="pay-amount-display {color_class}" style="margin: 0; font-size: 1.8rem;">{amount_str}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                # 卡片中部：二维码或图片
                # 调整列比例让图片在边框内更协调
                c_img_1, c_img_2, c_img_3 = st.columns([1, 4, 1])
                with c_img_2:
                    if os.path.exists(img_path): 
                        st.image(img_path, use_container_width=True)
                    else: 
                        # 本地图片不存在时，生成 API 二维码作为演示
                        qr_data = f"Donate_{cny_total}_{qr_data_suffix}"
                        # PayPal 如果是链接模式，二维码也可以指向链接
                        if link_url: qr_data = link_url
                        st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=180x180&data={qr_data}", use_container_width=True)
                
                # 卡片底部：按钮或提示文字
                if link_url:
                    # PayPal 等外链跳转
                    st.write("") # 增加一点间距
                    st.link_button(f"👉 Pay {amount_str}", link_url, type="primary", use_container_width=True)
                else:
                    # 扫码提示
                    st.markdown(f"""
                        <div class="pay-instruction" style="text-align: center; padding-top: 10px;">
                            请使用手机扫描上方二维码
                        </div>
                    """, unsafe_allow_html=True)
        
                    
        # 支付方式 Tabs
        st.write("")
        t1, t2, t3 = st.tabs([get_txt('pay_wechat'), get_txt('pay_alipay'), get_txt('pay_paypal')])
        
        with t1:
            render_pay_tab("WeChat Pay", f"¥{cny_total}", "color-wechat", "wechat_pay.jpg", "WeChat")
            
        with t2:
            render_pay_tab("Alipay", f"¥{cny_total}", "color-alipay", "ali_pay.jpg", "Alipay")
            
        with t3:
            # PayPal 特殊处理：使用 paypal.png (如果不存在则用API生成二维码作为占位), 并提供链接
            # 这里的 qr_data_suffix 设为 PayPal 仅用于生成备用图
            render_pay_tab("PayPal", f"${usd_total}", "color-paypal", "paypal.png", "PayPal", "https://paypal.me/ytqz")
        
        st.write("")
        if st.button("🎉 " + get_txt('pay_success').split('!')[0], type="primary", use_container_width=True):
            st.balloons()
            st.success(get_txt('pay_success').format(count=cnt))
            time.sleep(1)
            st.rerun()

    if st.button(get_txt('coffee_btn'), use_container_width=True):
        show_coffee_window()

# ==========================================
# 6. 主渲染逻辑
# ==========================================
def render_home():
    # --- 顶部导航 ---
    t_col1, t_col2 = st.columns([8, 2])
    with t_col2:
        inner_col1, inner_col2 = st.columns(2)
        with inner_col1:
            l_btn = "En" if st.session_state.language == 'zh' else "中"
            if st.button(l_btn):
                st.session_state.language = 'en' if st.session_state.language == 'zh' else 'zh'
                st.rerun()
        with inner_col2:
            if st.button("✨"):
                show_qrcode_window()
    # --- 标题区 ---
    st.markdown(f'<div class="main-title">{current_text["page_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">{current_text["subtitle"]}</div>', unsafe_allow_html=True)
    # --- 卡片网格 ---
    cols = st.columns(3)
    for idx, (title, desc, icon, url) in enumerate(current_text['games']):
        with cols[idx % 3]:
            st.markdown(f"""
            <a href="{url}" target="_blank" style="text-decoration:none">
                <div class="neal-card">
                    <div class="card-icon">{icon}</div>
                    <div>
                        <div class="card-title">{title}</div>
                        <div class="card-desc">{desc}</div>
                    </div>
                </div>
            </a>
            """, unsafe_allow_html=True)
    # --- Footer 区域 ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="text-align:center; max-width:600px; margin: 0 auto;">
        <h2 style="font-weight:800; font-size:1.8rem;">{current_text['footer_title']}</h2>
        <p style="color:#666; line-height:1.6; margin: 1.5rem 0;">{current_text['footer_text']}</p>
    </div>
    """, unsafe_allow_html=True)
    f_btns = st.columns([1,1,1,1])
    with f_btns[1]:
        if st.button(current_text['footer_btn2']): 
            show_qrcode_window()
    with f_btns[2]:
        if st.button(current_text['footer_btn3']): 
            show_coffee_window() # 调用新的咖啡弹窗
    # --- 统计与彩蛋 ---
    try:
        today_uv, total_uv, today_pv = track_and_get_stats()
    except Exception as e:
        today_uv, total_uv, today_pv = 0, 0, 0
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-box">
            <div class="metric-sub">今日 UV: {today_uv} 访客数</div>
        </div>
        <div class="metric-box" style="border-left: 1px solid #dee2e6; border-right: 1px solid #dee2e6; padding-left: 20px; padding-right: 20px;">
            <div class="metric-sub">历史总 UV: {total_uv} 总独立访客</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f'<div class="plant-container"><span style="font-size:3rem; cursor:pointer">🪴</span></div>', unsafe_allow_html=True)

# ==========================================
# 7. 入口
# ==========================================
if __name__ == "__main__":
    render_home()
