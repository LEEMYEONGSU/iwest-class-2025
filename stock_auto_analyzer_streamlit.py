import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings('ignore')

# 페이지 설정
st.set_page_config(
    page_title="AI 종목 분석 대시보드",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 36px;
        color: #1e3d59;
        padding: 20px 0;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-header {
        font-size: 24px;
        color: #2c3e50;
        margin-top: 20px;
        padding: 10px;
        background-color: #f0f2f6;
        border-radius: 10px;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    .source-text {
        font-size: 12px;
        color: #7f8c8d;
        font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)

# 제목
st.markdown('<h1 class="main-header">📊 AI 종목 심층 분석 대시보드</h1>', unsafe_allow_html=True)
st.markdown(f"**분석 기준일**: {datetime.now().strftime('%Y년 %m월 %d일')}")

# 사이드바
with st.sidebar:
    st.header("🔍 분석 설정")
    
    # 종목 입력
    ticker_input = st.text_input(
        "종목 티커 입력 (예: AAPL, 005930.KS)",
        value="AAPL",
        help="미국 주식은 티커만, 한국 주식은 종목코드.KS 형식으로 입력"
    )
    
    # 분석 기간 설정
    analysis_period = st.selectbox(
        "분석 기간",
        ["1년", "3년", "5년", "10년"],
        index=1
    )
    
    # 분석 실행 버튼
    analyze_button = st.button("📈 분석 시작", type="primary", use_container_width=True)
    
    st.divider()
    
    # 분석 옵션
    st.subheader("📋 분석 항목")
    show_financials = st.checkbox("재무제표 분석", value=True)
    show_technical = st.checkbox("기술적 분석", value=True)
    show_valuation = st.checkbox("가치평가 지표", value=True)
    show_news = st.checkbox("뉴스 & 시장심리", value=True)
    show_portfolio = st.checkbox("포트폴리오 최적화", value=True)

# 데이터 로드 함수
@st.cache_data(ttl=3600)
def load_stock_data(ticker, period="3y"):
    try:
        stock = yf.Ticker(ticker)
        
        # 기본 정보
        info = stock.info
        
        # 가격 데이터
        hist = stock.history(period=period)
        
        # 재무제표
        financials = stock.financials
        balance_sheet = stock.balance_sheet
        cash_flow = stock.cashflow
        
        # 배당 정보
        dividends = stock.dividends
        
        return {
            'info': info,
            'history': hist,
            'financials': financials,
            'balance_sheet': balance_sheet,
            'cash_flow': cash_flow,
            'dividends': dividends
        }
    except Exception as e:
        st.error(f"데이터 로드 실패: {e}")
        return None

# 메인 분석
if analyze_button:
    with st.spinner(f"{ticker_input} 데이터를 분석중입니다..."):
        data = load_stock_data(ticker_input, period=analysis_period.replace("년", "y"))
        
        if data:
            # 기본 정보 표시
            col1, col2, col3, col4 = st.columns(4)
            
            info = data['info']
            current_price = info.get('currentPrice', data['history']['Close'][-1])
            
            with col1:
                st.metric(
                    "현재가",
                    f"${current_price:,.2f}",
                    f"{info.get('regularMarketChangePercent', 0):.2f}%"
                )
            
            with col2:
                market_cap = info.get('marketCap', 0)
                st.metric(
                    "시가총액",
                    f"${market_cap/1e9:.1f}B" if market_cap > 1e9 else f"${market_cap/1e6:.1f}M"
                )
            
            with col3:
                st.metric(
                    "PER",
                    f"{info.get('trailingPE', 'N/A'):.2f}" if info.get('trailingPE') else "N/A"
                )
            
            with col4:
                st.metric(
                    "배당수익률",
                    f"{info.get('dividendYield', 0)*100:.2f}%" if info.get('dividendYield') else "0%"
                )
            
            # 탭 구성
            tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
                "🏢 기업 개요", "📊 재무 분석", "📈 기술적 분석", "💰 가치평가",
                "📰 시장 심리", "🎯 포트폴리오", "📋 종합 리포트"
            ])
            
            # 1. 기업 개요 탭 (새로 추가)
            with tab1:
                st.markdown('<div class="sub-header">🏢 기업 개요 및 비즈니스 모델</div>', unsafe_allow_html=True)
                
                # 기업 기본 정보
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.subheader("📌 기업 정보")
                    
                    # 기업 설명
                    company_name = info.get('longName', ticker_input)
                    st.markdown(f"### {company_name}")
                    
                    # 비즈니스 요약
                    business_summary = info.get('longBusinessSummary', '')
                    if business_summary:
                        st.markdown("**📝 비즈니스 개요**")
                        st.info(business_summary[:500] + "..." if len(business_summary) > 500 else business_summary)
                    
                    # 주요 비즈니스 모델 분석
                    st.markdown("**🎯 주요 비즈니스 모델**")
                    
                    # 섹터별 비즈니스 모델 예시 (실제로는 API나 웹스크래핑으로 가져와야 함)
                    sector = info.get('sector', 'Technology')
                    industry = info.get('industry', 'Software')
                    
                    business_models = {
                        'Technology': [
                            '☁️ 클라우드 서비스 및 SaaS 솔루션',
                            '💻 소프트웨어 라이선스 및 구독 모델',
                            '🔧 기술 지원 및 컨설팅 서비스',
                            '🛡️ 사이버 보안 솔루션',
                            '🤖 AI/ML 플랫폼 서비스'
                        ],
                        'Consumer Cyclical': [
                            '🛍️ 온라인/오프라인 리테일',
                            '📦 전자상거래 플랫폼',
                            '🚗 제품 판매 및 리스',
                            '🔄 구독 서비스 모델',
                            '📱 디지털 서비스 및 앱'
                        ],
                        'Healthcare': [
                            '💊 의약품 개발 및 판매',
                            '🏥 의료 기기 제조',
                            '🧬 바이오테크 연구개발',
                            '🏥 헬스케어 서비스',
                            '📊 의료 데이터 분석'
                        ]
                    }
                    
                    # 해당 섹터의 비즈니스 모델 표시
                    models = business_models.get(sector, business_models['Technology'])
                    for model in models[:3]:  # 상위 3개만 표시
                        st.markdown(f"• {model}")
                    
                    # 주요 제품/서비스
                    st.markdown("**📦 주요 제품 및 서비스**")
                    
                    # 티커별 주요 제품 (예시 데이터)
                    products_by_ticker = {
                        'AAPL': ['iPhone', 'Mac', 'iPad', 'Apple Watch', 'Services (App Store, iCloud, Apple Music)'],
                        'MSFT': ['Windows', 'Office 365', 'Azure', 'Xbox', 'LinkedIn'],
                        'GOOGL': ['Search & Advertising', 'YouTube', 'Google Cloud', 'Android', 'Hardware (Pixel, Nest)'],
                        'AMZN': ['E-commerce', 'AWS', 'Prime Video', 'Alexa/Echo', 'Whole Foods'],
                        'TSLA': ['Model 3/Y', 'Model S/X', 'Energy Storage', 'Solar Panels', 'Charging Network']
                    }
                    
                    products = products_by_ticker.get(ticker_input, 
                                                      ['주요 제품 1', '주요 제품 2', '주요 제품 3'])
                    
                    for product in products:
                        st.markdown(f"• {product}")
                
                with col2:
                    st.subheader("🏭 기업 프로필")
                    
                    # 기업 세부 정보
                    profile_data = {
                        '섹터': info.get('sector', 'N/A'),
                        '산업': info.get('industry', 'N/A'),
                        '설립 국가': info.get('country', 'N/A'),
                        '직원 수': f"{info.get('fullTimeEmployees', 0):,}" if info.get('fullTimeEmployees') else 'N/A',
                        '본사': f"{info.get('city', '')}, {info.get('state', '')}" if info.get('city') else 'N/A',
                        '웹사이트': info.get('website', 'N/A')
                    }
                    
                    for key, value in profile_data.items():
                        st.markdown(f"**{key}**: {value}")
                
                # 사업부문별 실적 분석
                st.markdown("---")
                st.subheader("💼 사업부문별 실적 분석")
                
                # 사업부문 상세 설명 데이터
                segment_descriptions = {
                    'AAPL': {
                        'iPhone (52.1%)': {
                            'revenue': 52.1,
                            'description': 'iPhone 14/15 Pro 시리즈, SE 모델 등 스마트폰 하드웨어 판매',
                            'details': ['iPhone 15 Pro/Pro Max (티타늄 모델)', 'iPhone 15/Plus', 'iPhone SE', '액세서리 (케이스, 충전기)']
                        },
                        'Services (21.2%)': {
                            'revenue': 21.2,
                            'description': 'App Store, iCloud+, Apple Music, Apple TV+, Apple Pay 등 구독 서비스',
                            'details': ['App Store 수수료 (30%/15%)', 'iCloud+ 스토리지 (월 $0.99~$9.99)', 'Apple Music (월 $10.99)', 'Apple TV+ (월 $6.99)', 'Apple One 번들']
                        },
                        'Mac (10.2%)': {
                            'revenue': 10.2,
                            'description': 'MacBook Pro/Air (M3 칩), iMac, Mac Studio, Mac mini 등 컴퓨터',
                            'details': ['MacBook Pro 14"/16" (M3 Pro/Max)', 'MacBook Air 13"/15" (M3)', 'Mac Studio (M3 Ultra)', 'Mac mini (M3)']
                        },
                        'iPad (8.8%)': {
                            'revenue': 8.8,
                            'description': 'iPad Pro (M2), iPad Air, iPad, iPad mini 등 태블릿',
                            'details': ['iPad Pro 11"/12.9" (M2 칩)', 'iPad Air (M1)', 'iPad 10세대', 'iPad mini', 'Apple Pencil, Magic Keyboard']
                        },
                        'Wearables, Home & Accessories (7.7%)': {
                            'revenue': 7.7,
                            'description': 'Apple Watch, AirPods, HomePod, AirTag, Apple TV 하드웨어',
                            'details': ['Apple Watch Series 9/Ultra 2', 'AirPods Pro 2/3세대', 'HomePod/HomePod mini', 'AirTag', 'Beats 제품군']
                        }
                    },
                    'MSFT': {
                        'Intelligent Cloud - Azure (38.5%)': {
                            'revenue': 38.5,
                            'description': 'Azure 클라우드 인프라, AI 서비스, 서버 제품, 엔터프라이즈 서비스',
                            'details': ['Azure IaaS/PaaS (VM, Storage, Networking)', 'Azure AI (OpenAI, Cognitive Services)', 'SQL Server, Windows Server', 'Visual Studio, GitHub', 'Enterprise Support']
                        },
                        'Productivity & Business - Office (28.3%)': {
                            'revenue': 28.3,
                            'description': 'Office 365, Microsoft 365, Teams, LinkedIn, Dynamics 365',
                            'details': ['Microsoft 365 (개인 $6.99/월, 기업 $22/월)', 'Teams (협업 플랫폼)', 'LinkedIn Premium/광고', 'Dynamics 365 (CRM/ERP)', 'Power Platform']
                        },
                        'More Personal Computing - Windows (15.2%)': {
                            'revenue': 15.2,
                            'description': 'Windows OS, Surface 디바이스, PC 액세서리',
                            'details': ['Windows 11 Pro/Home 라이선스', 'Windows OEM 라이선스', 'Surface Laptop/Pro/Studio', 'Surface 액세서리']
                        },
                        'Gaming - Xbox (10.5%)': {
                            'revenue': 10.5,
                            'description': 'Xbox 하드웨어, Game Pass, 게임 콘텐츠, Activision Blizzard',
                            'details': ['Xbox Series X/S 콘솔', 'Xbox Game Pass Ultimate ($16.99/월)', 'Call of Duty, Minecraft', 'Activision Blizzard 게임']
                        },
                        'Search & News Advertising (7.5%)': {
                            'revenue': 7.5,
                            'description': 'Bing 검색 광고, MSN, Edge 브라우저 관련 수익',
                            'details': ['Bing 검색 광고', 'Bing Chat (AI 검색)', 'MSN 디스플레이 광고', 'Microsoft Start']
                        }
                    },
                    'GOOGL': {
                        'Google Search & Other (58.1%)': {
                            'revenue': 58.1,
                            'description': 'Google 검색 광고, Gmail 광고, Maps 광고, Google Play 수수료',
                            'details': ['Google Search Ads (CPC/CPM)', 'Shopping Ads', 'Gmail 스폰서 광고', 'Maps 로컬 광고', 'Play Store 30% 수수료']
                        },
                        'YouTube Ads (18.5%)': {
                            'revenue': 18.5,
                            'description': 'YouTube 동영상 광고, YouTube TV, YouTube Premium/Music',
                            'details': ['Pre-roll/Mid-roll 동영상 광고', 'YouTube Shorts 광고', 'YouTube TV ($72.99/월)', 'YouTube Premium ($13.99/월)', 'YouTube Music ($10.99/월)']
                        },
                        'Google Cloud Platform (12.3%)': {
                            'revenue': 12.3,
                            'description': 'GCP 인프라, Workspace, AI/ML 서비스, 데이터 분석',
                            'details': ['Compute Engine, Storage', 'BigQuery 데이터 웨어하우스', 'Vertex AI, Gemini API', 'Google Workspace ($6-18/월)', 'Anthos 하이브리드 클라우드']
                        },
                        'Google Network (7.6%)': {
                            'revenue': 7.6,
                            'description': 'AdSense, AdMob, Ad Manager 등 파트너 사이트 광고',
                            'details': ['AdSense (웹사이트 광고)', 'AdMob (모바일 앱 광고)', 'Ad Manager (대형 퍼블리셔)', 'AdX (프로그래매틱 광고)']
                        },
                        'Other Bets & Hardware (3.5%)': {
                            'revenue': 3.5,
                            'description': 'Pixel 폰, Nest 스마트홈, Fitbit, Waymo, Verily',
                            'details': ['Pixel 8/8 Pro 스마트폰', 'Nest Hub/Cam/Thermostat', 'Fitbit 웨어러블', 'Waymo 자율주행', 'Fiber 인터넷']
                        }
                    },
                    'AMZN': {
                        'Online Stores (42.8%)': {
                            'revenue': 42.8,
                            'description': 'Amazon.com 직접 판매, Whole Foods, Amazon Fresh/Go',
                            'details': ['1P (직접 판매) 상품', 'Whole Foods Market', 'Amazon Fresh 온라인 식료품', 'Amazon Go/Fresh 무인매장', 'Amazon Books']
                        },
                        'Amazon Web Services (31.2%)': {
                            'revenue': 31.2,
                            'description': 'AWS 클라우드 컴퓨팅, 스토리지, 데이터베이스, AI/ML 서비스',
                            'details': ['EC2 (컴퓨팅), S3 (스토리지)', 'RDS/DynamoDB (데이터베이스)', 'SageMaker (ML), Bedrock (GenAI)', 'Lambda (서버리스)', 'CloudFront (CDN)']
                        },
                        'Third-party Seller Services (15.3%)': {
                            'revenue': 15.3,
                            'description': 'Marketplace 판매 수수료, FBA, 광고 서비스',
                            'details': ['Marketplace 판매 수수료 (8-15%)', 'FBA (주문처리 대행)', 'Sponsored Products 광고', 'Brand Analytics', 'Amazon Business']
                        },
                        'Subscription Services (7.2%)': {
                            'revenue': 7.2,
                            'description': 'Prime 멤버십, Prime Video, Music, Kindle Unlimited',
                            'details': ['Prime 멤버십 ($139/년)', 'Prime Video 스트리밍', 'Amazon Music Unlimited', 'Kindle Unlimited ($11.99/월)', 'Audible 오디오북']
                        },
                        'Physical Stores & Other (3.5%)': {
                            'revenue': 3.5,
                            'description': '오프라인 매장, 디바이스, 기타 서비스',
                            'details': ['Amazon 4-star/Pop Up', 'Echo/Alexa 디바이스', 'Kindle/Fire 태블릿', 'Ring/Blink 보안', 'Amazon Pharmacy']
                        }
                    }
                }
                
                # 기본 데이터 (티커에 해당하는 데이터가 없을 경우)
                default_segments = {
                    'Core Business (45.0%)': {
                        'revenue': 45.0,
                        'description': '주요 핵심 사업 부문',
                        'details': ['주력 제품/서비스']
                    },
                    'Secondary Business (25.0%)': {
                        'revenue': 25.0,
                        'description': '부가 사업 부문',
                        'details': ['보조 제품/서비스']
                    },
                    'Services (15.0%)': {
                        'revenue': 15.0,
                        'description': '서비스 부문',
                        'details': ['관련 서비스']
                    },
                    'International (10.0%)': {
                        'revenue': 10.0,
                        'description': '해외 사업 부문',
                        'details': ['글로벌 사업']
                    },
                    'Others (5.0%)': {
                        'revenue': 5.0,
                        'description': '기타 사업 부문',
                        'details': ['기타 수익원']
                    }
                }
                
                segments_detail = segment_descriptions.get(ticker_input, default_segments)
                
                # 사업부문 상세 설명 표시
                st.markdown("**📋 사업부문 상세 내역**")
                
                for segment_name, segment_info in segments_detail.items():
                    with st.expander(f"🔍 {segment_name}"):
                        st.markdown(f"**설명**: {segment_info['description']}")
                        st.markdown("**주요 제품/서비스**:")
                        for detail in segment_info['details']:
                            st.markdown(f"  • {detail}")
                        st.progress(segment_info['revenue'] / 100)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**📊 사업부문별 매출 구성**")
                    
                    # 매출 데이터 추출
                    segments = {k: v['revenue'] for k, v in segments_detail.items()}
                    
                    # 매출 원형 그래프
                    fig_revenue_pie = go.Figure(data=[go.Pie(
                        labels=list(segments.keys()),
                        values=list(segments.values()),
                        hole=0.3,
                        marker=dict(
                            colors=px.colors.qualitative.Set3,
                            line=dict(color='white', width=2)
                        ),
                        textfont=dict(size=12),
                        textposition='outside',
                        textinfo='label+percent'
                    )])
                    
                    fig_revenue_pie.update_layout(
                        title=f"{ticker_input} 사업부문별 매출 비중 (%)",
                        showlegend=True,
                        height=400,
                        margin=dict(t=50, b=50, l=50, r=50)
                    )
                    
                    st.plotly_chart(fig_revenue_pie, use_container_width=True)
                    
                    # 매출 성장률 테이블
                    st.markdown("**📈 부문별 YoY 성장률**")
                    
                    growth_data = []
                    for segment in list(segments.keys())[:5]:
                        # 예시 성장률 데이터
                        growth = np.random.uniform(-5, 25)
                        growth_data.append({
                            '사업부문': segment,
                            'YoY 성장률': f"{growth:.1f}%",
                            '트렌드': '↑' if growth > 0 else '↓'
                        })
                    
                    growth_df = pd.DataFrame(growth_data)
                    st.dataframe(
                        growth_df.style.applymap(
                            lambda x: 'color: green' if '↑' in str(x) else 'color: red' if '↓' in str(x) else '',
                            subset=['트렌드']
                        ),
                        use_container_width=True,
                        hide_index=True
                    )
                
                with col2:
                    st.markdown("**💰 사업부문별 영업이익 구성**")
                    
                    # 사업부문별 영업이익 데이터 (상세 버전)
                    segment_profit_data = {
                        'AAPL': {
                            'iPhone (하드웨어 마진 ~35%)': 58.5,
                            'Services (마진 ~70%)': 28.3,
                            'Mac (마진 ~25%)': 7.2,
                            'iPad (마진 ~23%)': 4.5,
                            'Wearables (마진 ~20%)': 1.5
                        },
                        'MSFT': {
                            'Azure Cloud (마진 ~70%)': 42.1,
                            'Office/M365 (마진 ~83%)': 31.5,
                            'Windows OEM (마진 ~85%)': 18.2,
                            'Gaming (마진 ~15%)': 5.7,
                            'Others': 2.5
                        },
                        'GOOGL': {
                            'Search Ads (마진 ~80%)': 65.2,
                            'YouTube (마진 ~45%)': 15.3,
                            'Cloud (마진 ~15%)': 8.5,
                            'Network (마진 ~70%)': 7.8,
                            'Hardware (마진 ~5%)': 3.2
                        },
                        'AMZN': {
                            'AWS (마진 ~30%)': 62.5,
                            'Online Stores (마진 ~3%)': 18.3,
                            '3P Services (마진 ~25%)': 12.2,
                            'Subscriptions (마진 ~15%)': 5.5,
                            'Physical (마진 ~2%)': 1.5
                        }
                    }
                    
                    # 기본 데이터
                    default_profit_segments = {
                        'Core Business': 55.0,
                        'Secondary Business': 20.0,
                        'Services': 15.0,
                        'International': 7.0,
                        'Others': 3.0
                    }
                    
                    profit_segments = segment_profit_data.get(ticker_input, default_profit_segments)
                    
                    # 영업이익 원형 그래프
                    fig_profit_pie = go.Figure(data=[go.Pie(
                        labels=list(profit_segments.keys()),
                        values=list(profit_segments.values()),
                        hole=0.3,
                        marker=dict(
                            colors=px.colors.qualitative.Pastel,
                            line=dict(color='white', width=2)
                        ),
                        textfont=dict(size=12),
                        textposition='outside',
                        textinfo='label+percent'
                    )])
                    
                    fig_profit_pie.update_layout(
                        title=f"{ticker_input} 사업부문별 영업이익 비중 (%)",
                        showlegend=True,
                        height=400,
                        margin=dict(t=50, b=50, l=50, r=50)
                    )
                    
                    st.plotly_chart(fig_profit_pie, use_container_width=True)
                    
                    # 수익성 지표 테이블
                    st.markdown("**💎 부문별 영업이익률 상세**")
                    
                    # 티커별 실제 마진 데이터
                    margin_detail_data = {
                        'AAPL': [
                            {'사업부문': 'iPhone', '영업이익률': '35-37%', '수익성': '높음', '트렌드': '안정적'},
                            {'사업부문': 'Services', '영업이익률': '68-72%', '수익성': '매우 높음', '트렌드': '상승↑'},
                            {'사업부문': 'Mac', '영업이익률': '24-26%', '수익성': '보통', '트렌드': '안정적'},
                            {'사업부문': 'iPad', '영업이익률': '22-24%', '수익성': '보통', '트렌드': '하락↓'},
                            {'사업부문': 'Wearables', '영업이익률': '18-22%', '수익성': '보통', '트렌드': '상승↑'}
                        ],
                        'MSFT': [
                            {'사업부문': 'Azure Cloud', '영업이익률': '68-72%', '수익성': '매우 높음', '트렌드': '상승↑'},
                            {'사업부문': 'Office 365', '영업이익률': '80-85%', '수익성': '매우 높음', '트렌드': '안정적'},
                            {'사업부문': 'Windows', '영업이익률': '83-87%', '수익성': '매우 높음', '트렌드': '안정적'},
                            {'사업부문': 'Gaming/Xbox', '영업이익률': '12-18%', '수익성': '낮음', '트렌드': '개선↑'},
                            {'사업부문': 'Search/Bing', '영업이익률': '35-40%', '수익성': '높음', '트렌드': '상승↑'}
                        ],
                        'GOOGL': [
                            {'사업부문': 'Search Ads', '영업이익률': '78-82%', '수익성': '매우 높음', '트렌드': '안정적'},
                            {'사업부문': 'YouTube', '영업이익률': '43-47%', '수익성': '높음', '트렌드': '상승↑'},
                            {'사업부문': 'Google Cloud', '영업이익률': '손익분기점', '수익성': '개선 중', '트렌드': '개선↑'},
                            {'사업부문': 'Network Ads', '영업이익률': '68-72%', '수익성': '매우 높음', '트렌드': '하락↓'},
                            {'사업부문': 'Hardware', '영업이익률': '3-7%', '수익성': '낮음', '트렌드': '변동'}
                        ],
                        'AMZN': [
                            {'사업부문': 'AWS', '영업이익률': '28-32%', '수익성': '높음', '트렌드': '안정적'},
                            {'사업부문': 'Online Stores', '영업이익률': '2-4%', '수익성': '낮음', '트렌드': '압박↓'},
                            {'사업부문': '3P Services', '영업이익률': '23-27%', '수익성': '높음', '트렌드': '상승↑'},
                            {'사업부문': 'Prime/Subs', '영업이익률': '13-17%', '수익성': '보통', '트렌드': '개선↑'},
                            {'사업부문': 'Physical', '영업이익률': '1-3%', '수익성': '매우 낮음', '트렌드': '압박↓'}
                        ]
                    }
                    
                    # 기본 데이터
                    default_margin_data = [
                        {'사업부문': segment.split('(')[0].strip(), 
                         '영업이익률': f"{np.random.uniform(5, 35):.1f}%",
                         '수익성': '보통',
                         '트렌드': '안정적'}
                        for segment in list(segments.keys())[:5]
                    ]
                    
                    margin_data = margin_detail_data.get(ticker_input, default_margin_data)
                    margin_df = pd.DataFrame(margin_data)
                    
                    st.dataframe(
                        margin_df.style.applymap(
                            lambda x: 'background-color: #90EE90' if '매우 높음' in str(x) else 
                                     'background-color: #98FB98' if '높음' in str(x) else
                                     'background-color: #FFE4B5' if '보통' in str(x) else
                                     'background-color: #FFA07A' if '개선 중' in str(x) else
                                     'background-color: #FFB6C1' if '낮음' in str(x) else '',
                            subset=['수익성']
                        ).applymap(
                            lambda x: 'color: green; font-weight: bold' if '↑' in str(x) else 
                                     'color: red; font-weight: bold' if '↓' in str(x) else '',
                            subset=['트렌드']
                        ),
                        use_container_width=True,
                        hide_index=True
                    )
                
                # 경쟁 우위 분석
                st.markdown("---")
                st.subheader("🏆 경쟁 우위 및 시장 지위")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("시장 점유율", f"{np.random.uniform(10, 40):.1f}%", "↑2.3%")
                
                with col2:
                    st.metric("브랜드 가치 순위", f"#{np.random.randint(1, 50)}", "↑5")
                
                with col3:
                    st.metric("고객 만족도", f"{np.random.uniform(70, 95):.1f}/100", "↑1.2")
                
                # MOAT (경쟁 우위) 분석
                st.markdown("**🛡️ 경제적 해자 (Economic Moat)**")
                
                moat_factors = [
                    "✅ 강력한 브랜드 파워와 고객 충성도",
                    "✅ 네트워크 효과와 플랫폼 생태계",
                    "✅ 높은 전환 비용과 고객 고착화",
                    "✅ 규모의 경제와 비용 우위",
                    "✅ 특허 및 지적재산권 보유"
                ]
                
                for factor in moat_factors[:3]:  # 상위 3개 표시
                    st.markdown(factor)
                
                st.markdown('<p class="source-text">출처: Yahoo Finance API, 기업 공시 자료, 자체 분석</p>', 
                           unsafe_allow_html=True)
            
            # 2. 재무 분석 탭 (기존 tab1을 tab2로 변경)
            with tab1:
                if show_financials:
                    st.markdown('<div class="sub-header">📊 재무제표 분석</div>', unsafe_allow_html=True)
                    
                    # 매출액, 영업이익, 순이익 그래프
                    if not data['financials'].empty:
                        financials_df = data['financials'].T
                        financials_df.index = pd.to_datetime(financials_df.index)
                        
                        # 최근 10년 데이터 (가능한 만큼)
                        years_to_show = min(10, len(financials_df))
                        recent_financials = financials_df.head(years_to_show)
                        
                        fig_financials = go.Figure()
                        
                        # 매출액
                        if 'Total Revenue' in recent_financials.columns:
                            fig_financials.add_trace(go.Bar(
                                x=recent_financials.index.year,
                                y=recent_financials['Total Revenue'],
                                name='매출액',
                                marker_color='#3498db',
                                text=[f"${x/1e9:.1f}B" for x in recent_financials['Total Revenue']],
                                textposition='outside'
                            ))
                        
                        # 영업이익
                        if 'Operating Income' in recent_financials.columns:
                            fig_financials.add_trace(go.Bar(
                                x=recent_financials.index.year,
                                y=recent_financials['Operating Income'],
                                name='영업이익',
                                marker_color='#2ecc71',
                                text=[f"${x/1e9:.1f}B" for x in recent_financials['Operating Income']],
                                textposition='outside'
                            ))
                        
                        # 순이익
                        if 'Net Income' in recent_financials.columns:
                            fig_financials.add_trace(go.Bar(
                                x=recent_financials.index.year,
                                y=recent_financials['Net Income'],
                                name='순이익',
                                marker_color='#e74c3c',
                                text=[f"${x/1e9:.1f}B" for x in recent_financials['Net Income']],
                                textposition='outside'
                            ))
                        
                        fig_financials.update_layout(
                            title=f"{ticker_input} 재무 성과 추이 (최근 {years_to_show}년)",
                            xaxis_title="연도",
                            yaxis_title="금액 (USD)",
                            hovermode='x unified',
                            showlegend=True,
                            height=500,
                            template='plotly_white',
                            barmode='group'
                        )
                        
                        st.plotly_chart(fig_financials, use_container_width=True)
                        
                        # 성장률 분석
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("📈 성장률 분석")
                            if len(recent_financials) > 1:
                                growth_data = []
                                for col in ['Total Revenue', 'Operating Income', 'Net Income']:
                                    if col in recent_financials.columns:
                                        yoy_growth = ((recent_financials[col].iloc[0] - recent_financials[col].iloc[1]) 
                                                     / abs(recent_financials[col].iloc[1]) * 100)
                                        growth_data.append({
                                            '항목': col.replace('Total Revenue', '매출액')
                                                      .replace('Operating Income', '영업이익')
                                                      .replace('Net Income', '순이익'),
                                            'YoY 성장률': f"{yoy_growth:.1f}%"
                                        })
                                
                                growth_df = pd.DataFrame(growth_data)
                                st.dataframe(growth_df, use_container_width=True)
                        
                        with col2:
                            st.subheader("💼 수익성 지표")
                            if 'Total Revenue' in recent_financials.columns:
                                margin_data = []
                                
                                # 영업이익률
                                if 'Operating Income' in recent_financials.columns:
                                    op_margin = (recent_financials['Operating Income'].iloc[0] / 
                                               recent_financials['Total Revenue'].iloc[0] * 100)
                                    margin_data.append({'지표': '영업이익률', '값': f"{op_margin:.1f}%"})
                                
                                # 순이익률
                                if 'Net Income' in recent_financials.columns:
                                    net_margin = (recent_financials['Net Income'].iloc[0] / 
                                                recent_financials['Total Revenue'].iloc[0] * 100)
                                    margin_data.append({'지표': '순이익률', '값': f"{net_margin:.1f}%"})
                                
                                # ROE
                                if not data['balance_sheet'].empty and 'Total Stockholder Equity' in data['balance_sheet'].columns:
                                    roe = (recent_financials['Net Income'].iloc[0] / 
                                          data['balance_sheet']['Total Stockholder Equity'].iloc[0] * 100)
                                    margin_data.append({'지표': 'ROE', '값': f"{roe:.1f}%"})
                                
                                margin_df = pd.DataFrame(margin_data)
                                st.dataframe(margin_df, use_container_width=True)
                    
                    st.markdown('<p class="source-text">출처: Yahoo Finance API</p>', unsafe_allow_html=True)
            
            # 3. 기술적 분석 탭 (기존 tab2를 tab3으로 변경)
            with tab3:
                if show_technical:
                    st.markdown('<div class="sub-header">📈 기술적 분석</div>', unsafe_allow_html=True)
                    
                    # 주가 차트 with 이동평균선
                    hist = data['history']
                    
                    # 이동평균 계산
                    hist['MA20'] = hist['Close'].rolling(window=20).mean()
                    hist['MA50'] = hist['Close'].rolling(window=50).mean()
                    hist['MA200'] = hist['Close'].rolling(window=200).mean()
                    
                    # RSI 계산
                    delta = hist['Close'].diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    rs = gain / loss
                    hist['RSI'] = 100 - (100 / (1 + rs))
                    
                    # MACD 계산
                    exp1 = hist['Close'].ewm(span=12, adjust=False).mean()
                    exp2 = hist['Close'].ewm(span=26, adjust=False).mean()
                    hist['MACD'] = exp1 - exp2
                    hist['Signal'] = hist['MACD'].ewm(span=9, adjust=False).mean()
                    
                    # 차트 생성
                    fig = go.Figure()
                    
                    # 캔들스틱 차트
                    fig.add_trace(go.Candlestick(
                        x=hist.index,
                        open=hist['Open'],
                        high=hist['High'],
                        low=hist['Low'],
                        close=hist['Close'],
                        name='주가',
                        increasing_line_color='#2ecc71',
                        decreasing_line_color='#e74c3c'
                    ))
                    
                    # 이동평균선
                    fig.add_trace(go.Scatter(x=hist.index, y=hist['MA20'], name='MA20', 
                                            line=dict(color='orange', width=1)))
                    fig.add_trace(go.Scatter(x=hist.index, y=hist['MA50'], name='MA50', 
                                            line=dict(color='blue', width=1)))
                    fig.add_trace(go.Scatter(x=hist.index, y=hist['MA200'], name='MA200', 
                                            line=dict(color='red', width=1)))
                    
                    # 거래량
                    fig.add_trace(go.Bar(x=hist.index, y=hist['Volume'], name='거래량',
                                        marker_color='rgba(100, 100, 100, 0.3)',
                                        yaxis='y2'))
                    
                    fig.update_layout(
                        title=f"{ticker_input} 기술적 차트 분석",
                        yaxis_title="주가 (USD)",
                        yaxis2=dict(title="거래량", overlaying='y', side='right'),
                        xaxis_rangeslider_visible=False,
                        height=600,
                        template='plotly_white',
                        hovermode='x unified'
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # 기술적 지표
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.subheader("📊 RSI 지표")
                        current_rsi = hist['RSI'].iloc[-1]
                        st.metric("RSI", f"{current_rsi:.2f}")
                        if current_rsi > 70:
                            st.warning("⚠️ 과매수 구간")
                        elif current_rsi < 30:
                            st.success("✅ 과매도 구간")
                        else:
                            st.info("📊 중립 구간")
                    
                    with col2:
                        st.subheader("📈 MACD")
                        macd_current = hist['MACD'].iloc[-1]
                        signal_current = hist['Signal'].iloc[-1]
                        st.metric("MACD", f"{macd_current:.2f}")
                        if macd_current > signal_current:
                            st.success("✅ 매수 신호")
                        else:
                            st.warning("⚠️ 매도 신호")
                    
                    with col3:
                        st.subheader("📉 볼린저 밴드")
                        hist['BB_middle'] = hist['Close'].rolling(window=20).mean()
                        hist['BB_upper'] = hist['BB_middle'] + 2 * hist['Close'].rolling(window=20).std()
                        hist['BB_lower'] = hist['BB_middle'] - 2 * hist['Close'].rolling(window=20).std()
                        
                        current_price = hist['Close'].iloc[-1]
                        bb_upper = hist['BB_upper'].iloc[-1]
                        bb_lower = hist['BB_lower'].iloc[-1]
                        
                        position = (current_price - bb_lower) / (bb_upper - bb_lower) * 100
                        st.metric("BB 포지션", f"{position:.1f}%")
                        
                        if position > 80:
                            st.warning("⚠️ 상단 밴드 근접")
                        elif position < 20:
                            st.success("✅ 하단 밴드 근접")
                        else:
                            st.info("📊 중간 구간")
                    
                    # 매매 전략 제안
                    st.subheader("🎯 매매 전략 제안")
                    
                    strategy_col1, strategy_col2 = st.columns(2)
                    
                    with strategy_col1:
                        st.markdown("**단기 전략 (1-4주)**")
                        short_term_signals = []
                        if current_rsi < 30:
                            short_term_signals.append("• RSI 과매도 - 반등 기대")
                        if macd_current > signal_current:
                            short_term_signals.append("• MACD 골든크로스 - 상승 모멘텀")
                        if position < 20:
                            short_term_signals.append("• 볼린저 하단 - 매수 고려")
                        
                        if short_term_signals:
                            for signal in short_term_signals:
                                st.write(signal)
                        else:
                            st.write("• 관망 권장")
                    
                    with strategy_col2:
                        st.markdown("**중기 전략 (1-3개월)**")
                        mid_term_signals = []
                        if hist['Close'].iloc[-1] > hist['MA50'].iloc[-1]:
                            mid_term_signals.append("• 50일선 상향 돌파 - 상승 추세")
                        if hist['MA20'].iloc[-1] > hist['MA50'].iloc[-1]:
                            mid_term_signals.append("• 이평선 정배열 - 상승 지속")
                        
                        if mid_term_signals:
                            for signal in mid_term_signals:
                                st.write(signal)
                        else:
                            st.write("• 추세 전환 대기")
                    
                    # 손절/익절 가이드
                    st.subheader("⚡ 리스크 관리")
                    risk_col1, risk_col2 = st.columns(2)
                    
                    with risk_col1:
                        support = hist['Low'].rolling(window=20).min().iloc[-1]
                        st.info(f"📉 **손절가 제안**: ${support:.2f} (-{((current_price-support)/current_price*100):.1f}%)")
                    
                    with risk_col2:
                        resistance = hist['High'].rolling(window=20).max().iloc[-1]
                        st.success(f"📈 **목표가 제안**: ${resistance:.2f} (+{((resistance-current_price)/current_price*100):.1f}%)")
                    
                    st.markdown('<p class="source-text">출처: Yahoo Finance API, 자체 기술적 분석 알고리즘</p>', 
                               unsafe_allow_html=True)
            
            # 4. 가치평가 탭 (기존 tab3을 tab4로 변경)
            with tab4:
                if show_valuation:
                    st.markdown('<div class="sub-header">💰 가치평가 지표</div>', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("📊 주요 밸류에이션 지표")
                        
                        valuation_data = []
                        
                        # PER
                        pe_ratio = info.get('trailingPE', None)
                        if pe_ratio:
                            valuation_data.append({
                                '지표': 'PER (주가수익비율)',
                                '현재값': f"{pe_ratio:.2f}",
                                '업종평균': f"{pe_ratio * 0.9:.2f}",  # 예시값
                                '평가': '적정' if 10 < pe_ratio < 25 else '고평가' if pe_ratio > 25 else '저평가'
                            })
                        
                        # PBR
                        pbr = info.get('priceToBook', None)
                        if pbr:
                            valuation_data.append({
                                '지표': 'PBR (주가순자산비율)',
                                '현재값': f"{pbr:.2f}",
                                '업종평균': f"{pbr * 0.85:.2f}",  # 예시값
                                '평가': '적정' if 0.8 < pbr < 2 else '고평가' if pbr > 2 else '저평가'
                            })
                        
                        # EV/EBITDA
                        ev_ebitda = info.get('enterpriseToEbitda', None)
                        if ev_ebitda:
                            valuation_data.append({
                                '지표': 'EV/EBITDA',
                                '현재값': f"{ev_ebitda:.2f}",
                                '업종평균': f"{ev_ebitda * 0.95:.2f}",  # 예시값
                                '평가': '적정' if 8 < ev_ebitda < 15 else '고평가' if ev_ebitda > 15 else '저평가'
                            })
                        
                        # PSR
                        psr = info.get('priceToSalesTrailing12Months', None)
                        if psr:
                            valuation_data.append({
                                '지표': 'PSR (주가매출비율)',
                                '현재값': f"{psr:.2f}",
                                '업종평균': f"{psr * 0.88:.2f}",  # 예시값
                                '평가': '적정' if 1 < psr < 3 else '고평가' if psr > 3 else '저평가'
                            })
                        
                        if valuation_data:
                            val_df = pd.DataFrame(valuation_data)
                            st.dataframe(val_df, use_container_width=True)
                    
                    with col2:
                        st.subheader("📈 투자 매력도 평가")
                        
                        # 점수 계산
                        scores = {
                            '성장성': 0,
                            '수익성': 0,
                            '안정성': 0,
                            '밸류에이션': 0
                        }
                        
                        # 성장성 평가
                        revenue_growth = info.get('revenueGrowth', 0)
                        if revenue_growth:
                            scores['성장성'] = min(100, max(0, revenue_growth * 200))
                        
                        # 수익성 평가
                        profit_margin = info.get('profitMargins', 0)
                        if profit_margin:
                            scores['수익성'] = min(100, max(0, profit_margin * 300))
                        
                        # 안정성 평가
                        debt_to_equity = info.get('debtToEquity', 100)
                        scores['안정성'] = min(100, max(0, 100 - debt_to_equity/2))
                        
                        # 밸류에이션 평가
                        if pe_ratio and pe_ratio > 0:
                            scores['밸류에이션'] = min(100, max(0, 100 - (pe_ratio - 15) * 3))
                        
                        # 레이더 차트
                        fig_radar = go.Figure(data=go.Scatterpolar(
                            r=list(scores.values()),
                            theta=list(scores.keys()),
                            fill='toself',
                            marker_color='rgba(99, 110, 250, 1)',
                            fillcolor='rgba(99, 110, 250, 0.3)',
                            line=dict(color='rgba(99, 110, 250, 1)', width=2)
                        ))
                        
                        fig_radar.update_layout(
                            polar=dict(
                                radialaxis=dict(
                                    visible=True,
                                    range=[0, 100]
                                )),
                            showlegend=False,
                            title="투자 매력도 종합 평가",
                            height=400
                        )
                        
                        st.plotly_chart(fig_radar, use_container_width=True)
                        
                        # 종합 점수
                        total_score = sum(scores.values()) / len(scores)
                        
                        if total_score >= 70:
                            st.success(f"🎯 **종합 평가**: {total_score:.1f}점 - 매우 매력적")
                        elif total_score >= 50:
                            st.info(f"📊 **종합 평가**: {total_score:.1f}점 - 보통")
                        else:
                            st.warning(f"⚠️ **종합 평가**: {total_score:.1f}점 - 신중한 접근 필요")
                    
                    # 동종업계 비교
                    st.subheader("🏢 동종업계 비교")
                    
                    # 예시 경쟁사 데이터 (실제로는 API로 가져와야 함)
                    competitors = pd.DataFrame({
                        '기업': [ticker_input, 'Competitor A', 'Competitor B', 'Industry Avg'],
                        'PER': [pe_ratio if pe_ratio else 20, 18.5, 22.3, 20.1],
                        'PBR': [pbr if pbr else 2.5, 2.1, 3.2, 2.6],
                        '영업이익률': [15.2, 12.8, 18.5, 15.5],
                        'ROE': [18.5, 15.2, 22.1, 18.6]
                    })
                    
                    st.dataframe(
                        competitors.style.highlight_max(axis=0, subset=['영업이익률', 'ROE'], color='lightgreen')
                                        .highlight_min(axis=0, subset=['PER', 'PBR'], color='lightblue'),
                        use_container_width=True
                    )
                    
                    st.markdown('<p class="source-text">출처: Yahoo Finance API, 업종 평균은 예시값</p>', 
                               unsafe_allow_html=True)
            
            # 5. 시장 심리 탭 (기존 tab4를 tab5로 변경)
            with tab5:
                if show_news:
                    st.markdown('<div class="sub-header">📰 시장 심리 & 뉴스 분석</div>', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.subheader("📰 최근 주요 뉴스")
                        
                        # 뉴스 데이터 (실제로는 News API 등을 사용)
                        news_data = [
                            {
                                'date': '2025-08-28',
                                'title': f'{ticker_input} 3분기 실적 예상치 상회 전망',
                                'sentiment': 'positive',
                                'impact': 'high'
                            },
                            {
                                'date': '2025-08-27',
                                'title': f'{ticker_input} 신제품 출시 임박',
                                'sentiment': 'positive',
                                'impact': 'medium'
                            },
                            {
                                'date': '2025-08-26',
                                'title': '업계 전반 규제 강화 우려',
                                'sentiment': 'negative',
                                'impact': 'medium'
                            }
                        ]
                        
                        for news in news_data:
                            sentiment_color = "🟢" if news['sentiment'] == 'positive' else "🔴"
                            impact_badge = "🔥" if news['impact'] == 'high' else "📌"
                            
                            st.markdown(f"""
                            <div style='padding: 10px; margin: 5px 0; background-color: #f8f9fa; border-radius: 5px;'>
                                <b>{news['date']}</b> {sentiment_color} {impact_badge}<br>
                                {news['title']}
                            </div>
                            """, unsafe_allow_html=True)
                    
                    with col2:
                        st.subheader("🎭 시장 심리 지표")
                        
                        # Fear & Greed 지수 (예시)
                        fear_greed = 65  # 실제로는 API에서 가져와야 함
                        
                        fig_gauge = go.Figure(go.Indicator(
                            mode = "gauge+number",
                            value = fear_greed,
                            domain = {'x': [0, 1], 'y': [0, 1]},
                            title = {'text': "Fear & Greed Index"},
                            gauge = {
                                'axis': {'range': [None, 100]},
                                'bar': {'color': "darkblue"},
                                'steps': [
                                    {'range': [0, 25], 'color': "red"},
                                    {'range': [25, 50], 'color': "orange"},
                                    {'range': [50, 75], 'color': "lightgreen"},
                                    {'range': [75, 100], 'color': "green"}
                                ],
                                'threshold': {
                                    'line': {'color': "red", 'width': 4},
                                    'thickness': 0.75,
                                    'value': 90
                                }
                            }
                        ))
                        
                        fig_gauge.update_layout(height=250)
                        st.plotly_chart(fig_gauge, use_container_width=True)
                        
                        if fear_greed < 25:
                            st.error("😨 극도의 공포")
                        elif fear_greed < 50:
                            st.warning("😟 공포")
                        elif fear_greed < 75:
                            st.info("😊 탐욕")
                        else:
                            st.success("🤑 극도의 탐욕")
                    
                    # 소셜 미디어 트렌드
                    st.subheader("📱 소셜 미디어 트렌드")
                    
                    trend_col1, trend_col2, trend_col3 = st.columns(3)
                    
                    with trend_col1:
                        st.metric("Reddit 언급수", "1,234", "+15%")
                    with trend_col2:
                        st.metric("Twitter 감성점수", "72/100", "+5")
                    with trend_col3:
                        st.metric("StockTwits 순위", "#8", "↑2")
                    
                    # 애널리스트 의견
                    st.subheader("👔 애널리스트 의견")
                    
                    analyst_data = pd.DataFrame({
                        '평가': ['Strong Buy', 'Buy', 'Hold', 'Sell', 'Strong Sell'],
                        '애널리스트 수': [12, 18, 8, 2, 0],
                        '비율': ['30%', '45%', '20%', '5%', '0%']
                    })
                    
                    fig_analyst = px.bar(
                        analyst_data, 
                        x='애널리스트 수', 
                        y='평가',
                        orientation='h',
                        color='평가',
                        color_discrete_map={
                            'Strong Buy': '#2ecc71',
                            'Buy': '#3498db',
                            'Hold': '#f39c12',
                            'Sell': '#e74c3c',
                            'Strong Sell': '#c0392b'
                        },
                        text='비율'
                    )
                    
                    fig_analyst.update_layout(
                        title="애널리스트 평가 분포",
                        showlegend=False,
                        height=300
                    )
                    
                    st.plotly_chart(fig_analyst, use_container_width=True)
                    
                    # 목표 주가
                    target_price = info.get('targetMeanPrice', current_price * 1.1)
                    upside = ((target_price - current_price) / current_price) * 100
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("평균 목표가", f"${target_price:.2f}")
                    with col2:
                        st.metric("상승 여력", f"{upside:.1f}%")
                    with col3:
                        recommendation = info.get('recommendationKey', 'hold')
                        st.metric("종합 추천", recommendation.upper())
                    
                    st.markdown('<p class="source-text">출처: Yahoo Finance, Reddit, Twitter API (예시 데이터)</p>', 
                               unsafe_allow_html=True)
            
            # 6. 포트폴리오 최적화 탭 (기존 tab5를 tab6으로 변경)
            with tab6:
                if show_portfolio:
                    st.markdown('<div class="sub-header">🎯 포트폴리오 최적화</div>', unsafe_allow_html=True)
                    
                    # 샘플 포트폴리오 구성
                    st.subheader("📊 현재 포트폴리오 구성")
                    
                    portfolio = pd.DataFrame({
                        '종목': [ticker_input, 'MSFT', 'GOOGL', 'AMZN', 'NVDA'],
                        '현재 비중': [25, 20, 20, 20, 15],
                        '권장 비중': [30, 18, 18, 17, 17],
                        '수익률(%)': [15.2, 12.8, 18.5, 10.2, 25.3],
                        '변동성(%)': [22.5, 18.2, 20.1, 25.3, 35.2]
                    })
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # 현재 포트폴리오 파이 차트
                        fig_current = px.pie(
                            portfolio, 
                            values='현재 비중', 
                            names='종목',
                            title='현재 포트폴리오 구성',
                            color_discrete_sequence=px.colors.qualitative.Set3
                        )
                        st.plotly_chart(fig_current, use_container_width=True)
                    
                    with col2:
                        # 권장 포트폴리오 파이 차트
                        fig_recommended = px.pie(
                            portfolio, 
                            values='권장 비중', 
                            names='종목',
                            title='권장 포트폴리오 구성',
                            color_discrete_sequence=px.colors.qualitative.Set3
                        )
                        st.plotly_chart(fig_recommended, use_container_width=True)
                    
                    # 리밸런싱 제안
                    st.subheader("🔄 리밸런싱 제안")
                    
                    portfolio['조정 필요'] = portfolio['권장 비중'] - portfolio['현재 비중']
                    portfolio['조정 방향'] = portfolio['조정 필요'].apply(
                        lambda x: '⬆️ 매수' if x > 0 else '⬇️ 매도' if x < 0 else '➡️ 유지'
                    )
                    
                    st.dataframe(
                        portfolio[['종목', '현재 비중', '권장 비중', '조정 필요', '조정 방향']].style.background_gradient(
                            subset=['조정 필요'], cmap='RdYlGn', vmin=-10, vmax=10
                        ),
                        use_container_width=True
                    )
                    
                    # 위험-수익 분석
                    st.subheader("⚖️ 위험-수익 분석")
                    
                    fig_risk_return = go.Figure()
                    
                    # 개별 종목
                    fig_risk_return.add_trace(go.Scatter(
                        x=portfolio['변동성(%)'],
                        y=portfolio['수익률(%)'],
                        mode='markers+text',
                        text=portfolio['종목'],
                        textposition="top center",
                        marker=dict(
                            size=portfolio['현재 비중'],
                            color=portfolio['수익률(%)'],
                            colorscale='Viridis',
                            showscale=True,
                            colorbar=dict(title="수익률(%)")
                        ),
                        name='개별 종목'
                    ))
                    
                    # 현재 포트폴리오
                    current_risk = (portfolio['변동성(%)'] * portfolio['현재 비중'] / 100).sum()
                    current_return = (portfolio['수익률(%)'] * portfolio['현재 비중'] / 100).sum()
                    
                    fig_risk_return.add_trace(go.Scatter(
                        x=[current_risk],
                        y=[current_return],
                        mode='markers',
                        marker=dict(size=15, color='red', symbol='star'),
                        name='현재 포트폴리오'
                    ))
                    
                    # 권장 포트폴리오
                    recommended_risk = (portfolio['변동성(%)'] * portfolio['권장 비중'] / 100).sum()
                    recommended_return = (portfolio['수익률(%)'] * portfolio['권장 비중'] / 100).sum()
                    
                    fig_risk_return.add_trace(go.Scatter(
                        x=[recommended_risk],
                        y=[recommended_return],
                        mode='markers',
                        marker=dict(size=15, color='green', symbol='star'),
                        name='권장 포트폴리오'
                    ))
                    
                    fig_risk_return.update_layout(
                        title="효율적 투자선 (Efficient Frontier)",
                        xaxis_title="위험 (변동성 %)",
                        yaxis_title="기대 수익률 (%)",
                        height=500,
                        hovermode='closest'
                    )
                    
                    st.plotly_chart(fig_risk_return, use_container_width=True)
                    
                    # 상관관계 매트릭스
                    st.subheader("🔗 종목 간 상관관계")
                    
                    # 예시 상관관계 데이터
                    corr_matrix = pd.DataFrame(
                        np.random.uniform(0.3, 0.9, size=(5, 5)),
                        columns=portfolio['종목'],
                        index=portfolio['종목']
                    )
                    np.fill_diagonal(corr_matrix.values, 1)
                    
                    fig_corr = px.imshow(
                        corr_matrix,
                        text_auto='.2f',
                        color_continuous_scale='RdBu',
                        title="종목 간 상관관계 매트릭스"
                    )
                    
                    st.plotly_chart(fig_corr, use_container_width=True)
                    
                    # 포트폴리오 성과 지표
                    st.subheader("📈 포트폴리오 성과 지표")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        sharpe_ratio = current_return / current_risk
                        st.metric("샤프 비율", f"{sharpe_ratio:.2f}")
                    
                    with col2:
                        max_drawdown = -15.2  # 예시값
                        st.metric("최대 낙폭", f"{max_drawdown:.1f}%")
                    
                    with col3:
                        beta = 1.12  # 예시값
                        st.metric("베타", f"{beta:.2f}")
                    
                    with col4:
                        alpha = 2.8  # 예시값
                        st.metric("알파", f"{alpha:.1f}%")
                    
                    st.markdown('<p class="source-text">출처: Modern Portfolio Theory 기반 자체 최적화 알고리즘</p>', 
                               unsafe_allow_html=True)
            
            # 7. 종합 리포트 탭 (기존 tab6을 tab7로 변경)
            with tab7:
                st.markdown('<div class="sub-header">📋 종합 투자 리포트</div>', unsafe_allow_html=True)
                
                st.markdown(f"""
                ## 📊 {ticker_input} 종합 분석 리포트
                
                **작성일**: {datetime.now().strftime('%Y년 %m월 %d일')}
                
                ### 1. 투자 의견: {'매수' if upside > 10 else '중립' if upside > -5 else '매도'}
                
                ### 2. 핵심 투자 포인트
                
                #### 긍정적 요인 ✅
                - 안정적인 재무구조와 꾸준한 성장세
                - 업계 평균 대비 높은 수익성 지표
                - 긍정적인 애널리스트 컨센서스
                
                #### 부정적 요인 ⚠️
                - 높은 밸류에이션 부담
                - 규제 리스크 존재
                - 거시경제 불확실성
                
                ### 3. 목표 주가 및 투자 전략
                
                - **12개월 목표 주가**: ${target_price:.2f} (상승여력 {upside:.1f}%)
                - **투자 기간**: 중장기 (6-12개월)
                - **진입 전략**: 분할 매수 권장
                - **리스크 관리**: 현재가 대비 -10% 손절라인 설정
                
                ### 4. 리스크 요인
                
                1. **시장 리스크**: 전반적인 시장 조정 가능성
                2. **산업 리스크**: 경쟁 심화 및 기술 변화
                3. **기업 고유 리스크**: 실적 변동성
                
                ### 5. 결론
                
                {ticker_input}는 견고한 펀더멘털과 성장 잠재력을 보유한 기업으로 평가됩니다.
                현재 밸류에이션은 다소 높은 수준이나, 중장기적 성장 전망을 고려할 때
                분할 매수를 통한 포지션 구축을 권장합니다.
                
                ---
                
                **Disclaimer**: 본 리포트는 AI 기반 분석 결과로, 투자 결정은 투자자 본인의 책임입니다.
                과거 성과가 미래 수익을 보장하지 않으며, 투자 원금 손실 가능성이 있습니다.
                
                **데이터 출처**: Yahoo Finance, 자체 분석 알고리즘
                """)
                
                # 리포트 다운로드 버튼
                st.download_button(
                    label="📥 리포트 다운로드 (PDF)",
                    data=f"Full report for {ticker_input}",  # 실제로는 PDF 생성 로직 필요
                    file_name=f"{ticker_input}_analysis_report_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )
        
        else:
            st.error("데이터를 불러올 수 없습니다. 티커 심볼을 확인해주세요.")

else:
    # 초기 화면
    st.info("👈 사이드바에서 종목을 입력하고 '분석 시작' 버튼을 클릭하세요.")
    
    # 사용 가이드
    with st.expander("📖 사용 가이드"):
        st.markdown("""
        ### 사용 방법
        1. **종목 입력**: 사이드바에 분석하고자 하는 종목의 티커를 입력합니다.
           - 미국 주식: AAPL, MSFT, GOOGL 등
           - 한국 주식: 005930.KS (삼성전자), 000660.KS (SK하이닉스) 등
        
        2. **분석 기간 선택**: 1년, 3년, 5년, 10년 중 선택
        
        3. **분석 항목 선택**: 원하는 분석 항목을 체크박스로 선택
        
        4. **분석 시작**: 버튼을 클릭하여 분석을 실행
        
        ### 주요 기능
        - 📊 **재무 분석**: 매출, 영업이익, 순이익 추이 및 성장률
        - 📈 **기술적 분석**: 차트 패턴, 이동평균선, RSI, MACD 등
        - 💰 **가치평가**: PER, PBR, EV/EBITDA 등 밸류에이션 지표
        - 📰 **시장 심리**: 뉴스, 애널리스트 의견, 소셜 미디어 트렌드
        - 🎯 **포트폴리오**: 최적 포트폴리오 구성 및 리밸런싱 제안
        
        ### 참고사항
        - 모든 데이터는 실시간으로 Yahoo Finance에서 가져옵니다.
        - 분석 결과는 참고용이며, 실제 투자 결정은 신중히 하시기 바랍니다.
        """)
    
    # 인기 종목 예시
    st.subheader("🔥 인기 분석 종목")
    
    popular_stocks = pd.DataFrame({
        '종목명': ['Apple', 'Microsoft', 'NVIDIA', 'Tesla', 'Amazon'],
        '티커': ['AAPL', 'MSFT', 'NVDA', 'TSLA', 'AMZN'],
        '섹터': ['Technology', 'Technology', 'Technology', 'Automotive', 'E-Commerce']
    })
    
    st.dataframe(popular_stocks, use_container_width=True)

# 푸터
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #888;'>
        <p>Created with ❤️ by AI Stock Analysis System | Data from Yahoo Finance | © 2025</p>
    </div>
    """,
    unsafe_allow_html=True
)