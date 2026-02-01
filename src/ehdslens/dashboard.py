"""
EHDSLens Interactive Dashboard
Streamlit-based web application for exploring EHDS systematic review data.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from collections import Counter

from .core import EHDSAnalyzer
from .data import ThematicAxis, QualityRating, StudyType


def create_dashboard():
    """Launch the Streamlit dashboard."""

    # Page configuration
    st.set_page_config(
        page_title="EHDSLens Dashboard",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #1E3A5F;
            margin-bottom: 0;
        }
        .sub-header {
            font-size: 1.1rem;
            color: #666;
            margin-top: 0;
        }
        .metric-card {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 24px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Initialize analyzer
    @st.cache_resource
    def load_data():
        analyzer = EHDSAnalyzer()
        analyzer.load_default_data()
        return analyzer

    analyzer = load_data()
    stats = analyzer.get_statistics()

    # Header
    st.markdown('<p class="main-header">🏥 EHDSLens Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">European Health Data Space - Systematic Literature Review Analysis</p>', unsafe_allow_html=True)
    st.markdown("---")

    # Sidebar
    with st.sidebar:
        st.image("https://img.shields.io/badge/EHDS-Regulation%202025%2F327-blue", width=200)
        st.markdown("## 🔍 Filters")

        # Year filter
        years = [s.year for s in analyzer.db.studies]
        year_range = st.slider(
            "Publication Year",
            min_value=min(years),
            max_value=max(years),
            value=(min(years), max(years))
        )

        # Axis filter
        selected_axes = st.multiselect(
            "Thematic Axes",
            options=[a.value for a in ThematicAxis],
            default=[a.value for a in ThematicAxis]
        )

        # Quality filter
        selected_quality = st.multiselect(
            "Quality Rating",
            options=[q.value for q in QualityRating],
            default=[q.value for q in QualityRating]
        )

        st.markdown("---")
        st.markdown("### 📊 Quick Stats")
        st.metric("Total Studies", stats['total'])
        st.metric("Year Range", f"{stats['year_range'][0]}-{stats['year_range'][1]}")

    # Filter studies based on sidebar
    filtered_studies = [
        s for s in analyzer.db.studies
        if year_range[0] <= s.year <= year_range[1]
        and s.primary_axis.value in selected_axes
        and s.quality_rating.value in selected_quality
    ]

    # Main content tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview",
        "📚 Studies",
        "🔬 Analysis",
        "📈 GRADE-CERQual",
        "🔍 Search"
    ])

    # Tab 1: Overview
    with tab1:
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Filtered Studies",
                len(filtered_studies),
                delta=f"{len(filtered_studies) - stats['total']} from total" if len(filtered_studies) != stats['total'] else None
            )
        with col2:
            high_quality = len([s for s in filtered_studies if s.quality_rating == QualityRating.HIGH])
            st.metric("High Quality", high_quality, delta=f"{high_quality/len(filtered_studies)*100:.0f}%" if filtered_studies else "0%")
        with col3:
            empirical = len([s for s in filtered_studies if s.study_type in [StudyType.QUALITATIVE, StudyType.QUANTITATIVE, StudyType.MIXED_METHODS]])
            st.metric("Empirical Studies", empirical)
        with col4:
            latest_year = max([s.year for s in filtered_studies]) if filtered_studies else 0
            st.metric("Latest Year", latest_year)

        st.markdown("---")

        # Charts row
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📅 Publications by Year")
            year_counts = Counter(s.year for s in filtered_studies)
            df_years = pd.DataFrame({
                'Year': list(year_counts.keys()),
                'Studies': list(year_counts.values())
            }).sort_values('Year')

            fig = px.bar(
                df_years, x='Year', y='Studies',
                color='Studies',
                color_continuous_scale='Blues'
            )
            fig.update_layout(showlegend=False, coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("🎯 Studies by Thematic Axis")
            axis_counts = Counter(s.primary_axis.value for s in filtered_studies)

            # Shorten names for display
            short_names = {
                'governance_rights_ethics': 'Governance & Ethics',
                'secondary_use_pets': 'Secondary Use & PETs',
                'national_implementation': 'National Implementation',
                'citizen_engagement': 'Citizen Engagement',
                'federated_learning_ai': 'Federated Learning & AI'
            }

            df_axis = pd.DataFrame({
                'Axis': [short_names.get(k, k) for k in axis_counts.keys()],
                'Studies': list(axis_counts.values())
            })

            fig = px.pie(df_axis, values='Studies', names='Axis', hole=0.4)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

        # Second row
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("⭐ Quality Distribution")
            quality_counts = Counter(s.quality_rating.value for s in filtered_studies)

            colors = {'high': '#2E7D32', 'moderate': '#FBC02D', 'low': '#E65100', 'not_applicable': '#9E9E9E'}

            df_quality = pd.DataFrame({
                'Quality': list(quality_counts.keys()),
                'Count': list(quality_counts.values())
            })

            fig = px.bar(
                df_quality, x='Quality', y='Count',
                color='Quality',
                color_discrete_map=colors
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("📋 Study Types")
            type_counts = Counter(s.study_type.value for s in filtered_studies)

            df_types = pd.DataFrame({
                'Type': list(type_counts.keys()),
                'Count': list(type_counts.values())
            })

            fig = px.bar(df_types, x='Count', y='Type', orientation='h')
            fig.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig, use_container_width=True)

    # Tab 2: Studies Browser
    with tab2:
        st.subheader(f"📚 Study Database ({len(filtered_studies)} studies)")

        # Convert to DataFrame for display
        df_studies = pd.DataFrame([
            {
                'ID': s.id,
                'Authors': s.authors,
                'Year': s.year,
                'Title': s.title[:80] + '...' if len(s.title) > 80 else s.title,
                'Journal': s.journal,
                'Axis': s.primary_axis.value,
                'Quality': s.quality_rating.value,
                'Type': s.study_type.value
            }
            for s in filtered_studies
        ])

        # Sortable table
        st.dataframe(
            df_studies,
            use_container_width=True,
            hide_index=True,
            column_config={
                'ID': st.column_config.NumberColumn('ID', width='small'),
                'Year': st.column_config.NumberColumn('Year', width='small'),
                'Quality': st.column_config.TextColumn('Quality', width='small'),
            }
        )

        # Download button
        csv = df_studies.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="ehds_studies.csv",
            mime="text/csv"
        )

    # Tab 3: Thematic Analysis
    with tab3:
        st.subheader("🔬 Thematic Axis Analysis")

        selected_axis = st.selectbox(
            "Select Thematic Axis",
            options=[a for a in ThematicAxis],
            format_func=lambda x: x.value.replace('_', ' ').title()
        )

        analysis = analyzer.analyze_axis(selected_axis)

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(f"### {selected_axis.value.replace('_', ' ').title()}")
            st.metric("Total Studies", analysis['total_studies'])
            st.metric("Peer-reviewed", analysis.get('peer_reviewed', 0))
            st.metric("High Quality", analysis.get('high_quality_count', 0))

            st.markdown("#### Study Types")
            for stype, count in analysis.get('type_distribution', {}).items():
                st.markdown(f"- {stype.replace('_', ' ').title()}: {count}")

        with col2:
            st.markdown("#### Quality Distribution")
            qual_data = analysis['quality_distribution']
            fig = px.pie(
                values=list(qual_data.values()),
                names=list(qual_data.keys()),
                color_discrete_sequence=['#2E7D32', '#FBC02D', '#E65100', '#9E9E9E']
            )
            st.plotly_chart(fig, use_container_width=True)

        # Research gaps
        st.markdown("---")
        st.markdown("### 🔍 Research Gaps")
        gaps = analyzer.get_research_gaps()
        for i, gap in enumerate(gaps, 1):
            st.info(f"**Gap {i}:** {gap}")

    # Tab 4: GRADE-CERQual
    with tab4:
        st.subheader("📈 GRADE-CERQual Confidence Assessments")

        findings = analyzer.get_grade_cerqual_summary()

        # Group by confidence
        confidence_colors = {
            'high': '🟢',
            'moderate': '🟡',
            'low': '🟠',
            'very_low': '🔴'
        }

        for f in findings:
            conf = f['confidence'].lower()  # Normalize to lowercase
            emoji = confidence_colors.get(conf, '⚪')

            with st.expander(f"{emoji} **{conf.upper()}** - {f['finding'][:60]}...", expanded=conf=='high'):
                st.markdown(f"**Finding:** {f['finding']}")
                st.markdown(f"**Contributing Studies:** {f['studies']}")
                st.markdown(f"**Confidence Level:** {conf.upper()}")

        # Hypotheses
        st.markdown("---")
        st.subheader("🧪 Testable Hypotheses")

        hypotheses = analyzer.get_testable_hypotheses()

        for category, hyps in hypotheses.items():
            with st.expander(f"**{category}** ({len(hyps)} hypotheses)"):
                for h in hyps:
                    st.markdown(f"- {h}")

    # Tab 5: Search
    with tab5:
        st.subheader("🔍 Search Studies")

        search_query = st.text_input("Enter search terms", placeholder="e.g., federated learning, privacy, GDPR")

        if search_query:
            results = analyzer.search_studies(search_query)

            st.markdown(f"**Found {len(results)} studies matching '{search_query}'**")

            for study in results:
                with st.expander(f"**{study.authors}** ({study.year})"):
                    st.markdown(f"**Title:** {study.title}")
                    st.markdown(f"**Journal:** {study.journal}")
                    st.markdown(f"**Type:** {study.study_type.value}")
                    st.markdown(f"**Axis:** {study.primary_axis.value}")
                    st.markdown(f"**Quality:** {study.quality_rating.value}")
                    if study.doi:
                        st.markdown(f"**DOI:** [{study.doi}](https://doi.org/{study.doi})")

                    st.code(study.get_citation(style="apa"), language=None)

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>EHDSLens v1.0.0 |
            <a href='https://github.com/FabioLiberti/EHDSLens'>GitHub</a> |
            <a href='https://fabioliberti.github.io/EHDSLens/'>Documentation</a></p>
            <p>© 2025 Fabio Liberti | MIT License</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def main():
    """Entry point for the dashboard."""
    create_dashboard()


if __name__ == "__main__":
    main()
