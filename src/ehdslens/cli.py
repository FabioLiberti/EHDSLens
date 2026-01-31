#!/usr/bin/env python3
"""
EHDSLens Command Line Interface

Usage:
    ehdslens stats           Show database statistics
    ehdslens analyze AXIS    Analyze specific thematic axis
    ehdslens search QUERY    Search studies
    ehdslens report FORMAT   Generate report (markdown/html/json)
    ehdslens export FORMAT   Export data (csv/json/bibtex)
    ehdslens grade           Show GRADE-CERQual summary
    ehdslens hypotheses      List testable hypotheses
    ehdslens dashboard       Launch interactive Streamlit dashboard
    ehdslens api             Start REST API server
"""

import argparse
import sys
import json
from pathlib import Path

from .core import EHDSAnalyzer
from .data import ThematicAxis


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        prog="ehdslens",
        description="EHDS Literature Analysis Toolkit",
        epilog="For more information, visit: https://github.com/FabioLiberti/EHDSLens"
    )

    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s 1.2.0'
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show database statistics')
    stats_parser.add_argument('--json', action='store_true', help='Output as JSON')

    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze thematic axis')
    analyze_parser.add_argument(
        'axis',
        choices=['governance', 'pets', 'implementation', 'engagement', 'ai', 'all'],
        help='Thematic axis to analyze'
    )
    analyze_parser.add_argument('--json', action='store_true', help='Output as JSON')

    # Search command
    search_parser = subparsers.add_parser('search', help='Search studies')
    search_parser.add_argument('query', help='Search query')

    # Report command
    report_parser = subparsers.add_parser('report', help='Generate analysis report')
    report_parser.add_argument(
        'format',
        choices=['markdown', 'html', 'json'],
        help='Report format'
    )
    report_parser.add_argument('-o', '--output', help='Output file path')

    # Export command
    export_parser = subparsers.add_parser('export', help='Export study data')
    export_parser.add_argument(
        'format',
        choices=['csv', 'json', 'bibtex', 'ris'],
        help='Export format'
    )
    export_parser.add_argument('-o', '--output', help='Output file path')

    # GRADE-CERQual command
    grade_parser = subparsers.add_parser('grade', help='Show GRADE-CERQual summary')

    # Hypotheses command
    hypo_parser = subparsers.add_parser('hypotheses', help='List testable hypotheses')

    # PRISMA command
    prisma_parser = subparsers.add_parser('prisma', help='Show PRISMA flow statistics')

    # Dashboard command
    dashboard_parser = subparsers.add_parser('dashboard', help='Launch interactive Streamlit dashboard')
    dashboard_parser.add_argument('--port', type=int, default=8501, help='Port number (default: 8501)')

    # API command
    api_parser = subparsers.add_parser('api', help='Start REST API server')
    api_parser.add_argument('--host', default='0.0.0.0', help='Host address (default: 0.0.0.0)')
    api_parser.add_argument('--port', type=int, default=8000, help='Port number (default: 8000)')
    api_parser.add_argument('--reload', action='store_true', help='Enable auto-reload for development')

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    # Initialize analyzer with default data
    analyzer = EHDSAnalyzer()
    analyzer.load_default_data()

    # Execute command
    if args.command == 'stats':
        cmd_stats(analyzer, args)
    elif args.command == 'analyze':
        cmd_analyze(analyzer, args)
    elif args.command == 'search':
        cmd_search(analyzer, args)
    elif args.command == 'report':
        cmd_report(analyzer, args)
    elif args.command == 'export':
        cmd_export(analyzer, args)
    elif args.command == 'grade':
        cmd_grade(analyzer)
    elif args.command == 'hypotheses':
        cmd_hypotheses(analyzer)
    elif args.command == 'prisma':
        cmd_prisma(analyzer)
    elif args.command == 'dashboard':
        cmd_dashboard(args)
    elif args.command == 'api':
        cmd_api(args)


def cmd_stats(analyzer: EHDSAnalyzer, args):
    """Handle stats command."""
    stats = analyzer.get_statistics()

    if args.json:
        print(json.dumps(stats, indent=2))
        return

    print("\n" + "=" * 60)
    print("EHDS SYSTEMATIC LITERATURE REVIEW - DATABASE STATISTICS")
    print("=" * 60)
    print(f"\nTotal studies: {stats['total']}")
    print(f"Peer-reviewed: {stats['peer_reviewed']}")
    print(f"Year range: {stats['year_range'][0]} - {stats['year_range'][1]}")

    print("\nBy Publication Year:")
    for year, count in sorted(stats['by_year'].items()):
        bar = "█" * count
        print(f"  {year}: {bar} ({count})")

    print("\nBy Thematic Axis:")
    for axis, count in stats['by_axis'].items():
        pct = count / stats['total'] * 100
        print(f"  {axis.replace('_', ' ').title()}: {count} ({pct:.1f}%)")

    print("\nBy Quality Rating:")
    for quality, count in stats['by_quality'].items():
        print(f"  {quality.title()}: {count}")

    print("\nTop Countries:")
    for country, count in list(stats['by_country'].items())[:5]:
        print(f"  {country}: {count}")

    print("\n" + "=" * 60)


def cmd_analyze(analyzer: EHDSAnalyzer, args):
    """Handle analyze command."""
    axis_map = {
        'governance': ThematicAxis.GOVERNANCE_RIGHTS_ETHICS,
        'pets': ThematicAxis.SECONDARY_USE_PETS,
        'implementation': ThematicAxis.NATIONAL_IMPLEMENTATION,
        'engagement': ThematicAxis.CITIZEN_ENGAGEMENT,
        'ai': ThematicAxis.FEDERATED_LEARNING_AI
    }

    if args.axis == 'all':
        results = analyzer.analyze_all_axes()
    else:
        axis = axis_map[args.axis]
        results = {args.axis: analyzer.analyze_axis(axis)}

    if args.json:
        print(json.dumps(results, indent=2))
        return

    for axis_name, data in results.items():
        print(f"\n{'=' * 60}")
        print(f"ANALYSIS: {axis_name.replace('_', ' ').upper()}")
        print(f"{'=' * 60}")
        print(f"Total studies: {data['total_studies']}")
        print(f"Peer-reviewed: {data['peer_reviewed']}")
        print(f"Grey literature: {data['grey_literature']}")
        print(f"High quality: {data['high_quality_count']}")

        print("\nStudy Types:")
        for stype, count in data['type_distribution'].items():
            print(f"  {stype}: {count}")


def cmd_search(analyzer: EHDSAnalyzer, args):
    """Handle search command."""
    results = analyzer.search_studies(args.query)

    if not results:
        print(f"No studies found matching '{args.query}'")
        return

    print(f"\nFound {len(results)} studies matching '{args.query}':\n")

    for study in results:
        print(f"[{study.id}] {study.authors} ({study.year})")
        print(f"    {study.title}")
        print(f"    {study.journal} | {study.primary_axis.value}")
        print()


def cmd_report(analyzer: EHDSAnalyzer, args):
    """Handle report command."""
    from .export import ReportGenerator

    gen = ReportGenerator(analyzer.db)

    output_path = args.output
    if not output_path:
        ext = {'markdown': '.md', 'html': '.html', 'json': '.json'}[args.format]
        output_path = f"ehds_report{ext}"

    gen.generate_full_report(Path(output_path), format=args.format)
    print(f"Report generated: {output_path}")


def cmd_export(analyzer: EHDSAnalyzer, args):
    """Handle export command."""
    from .export import ReportGenerator

    gen = ReportGenerator(analyzer.db)

    output_path = args.output
    if not output_path:
        ext = {'csv': '.csv', 'json': '.json', 'bibtex': '.bib', 'ris': '.ris'}[args.format]
        output_path = f"ehds_studies{ext}"

    if args.format in ['csv', 'json']:
        if args.format == 'csv':
            analyzer.export_to_csv(Path(output_path))
        else:
            analyzer.export_to_json(Path(output_path))
    else:
        gen.generate_bibliography(Path(output_path), format=args.format)

    print(f"Data exported: {output_path}")


def cmd_grade(analyzer: EHDSAnalyzer):
    """Handle GRADE-CERQual command."""
    summary = analyzer.get_grade_cerqual_summary()

    print("\n" + "=" * 80)
    print("GRADE-CERQual SUMMARY OF FINDINGS")
    print("=" * 80)

    for finding in summary:
        conf = finding['confidence']
        emoji = "🟢" if conf == "HIGH" else "🟡" if conf == "MODERATE" else "🔴"

        print(f"\n{emoji} {conf}")
        print(f"   Finding: {finding['finding']}")
        print(f"   Studies: {finding['studies']}")
        print(f"   Meth. limitations: {finding['meth_limitations']}")
        print(f"   Coherence: {finding['coherence']}")
        print(f"   Adequacy: {finding['adequacy']}")
        print(f"   Explanation: {finding['explanation']}")

    print("\n" + "=" * 80)


def cmd_hypotheses(analyzer: EHDSAnalyzer):
    """Handle hypotheses command."""
    hypotheses = analyzer.get_testable_hypotheses()

    print("\n" + "=" * 60)
    print("TESTABLE HYPOTHESES FOR EHDS RESEARCH")
    print("=" * 60)

    for category, hypos in hypotheses.items():
        print(f"\n{category.upper()} HYPOTHESES:")
        for h in hypos:
            print(f"  • {h}")

    print("\n" + "=" * 60)


def cmd_prisma(analyzer: EHDSAnalyzer):
    """Handle PRISMA command."""
    stats = analyzer.generate_prisma_stats()

    print("\n" + "=" * 60)
    print("PRISMA 2020 FLOW DIAGRAM STATISTICS")
    print("=" * 60)

    print("\nIDENTIFICATION:")
    print(f"  Records from databases: {stats['records_identified']}")

    print("\nSCREENING:")
    print(f"  Duplicates removed: {stats['duplicates_removed']}")
    print(f"  Records screened: {stats['records_screened']}")
    print(f"  Excluded at screening: {stats['records_excluded_screening']}")

    print("\nELIGIBILITY:")
    print(f"  Full-text assessed: {stats['full_text_assessed']}")
    print(f"  Excluded at full-text: {stats['full_text_excluded']}")
    print("\n  Exclusion reasons:")
    for reason, count in stats['exclusion_reasons'].items():
        print(f"    - {reason.replace('_', ' ')}: {count}")

    print("\nINCLUDED:")
    print(f"  Studies in synthesis: {stats['studies_included']}")

    print("\n" + "=" * 60)


def cmd_dashboard(args):
    """Handle dashboard command."""
    try:
        import streamlit.web.cli as stcli
        import sys
        import os

        # Get the dashboard module path
        dashboard_path = os.path.join(os.path.dirname(__file__), 'dashboard.py')

        print(f"\n🚀 Launching EHDSLens Dashboard on port {args.port}...")
        print(f"   Open http://localhost:{args.port} in your browser\n")

        sys.argv = ['streamlit', 'run', dashboard_path, '--server.port', str(args.port)]
        stcli.main()

    except ImportError:
        print("Error: Streamlit is not installed.")
        print("Install it with: pip install ehdslens[dashboard]")
        sys.exit(1)


def cmd_api(args):
    """Handle API command."""
    try:
        from .api import run_api

        print(f"\n🚀 Starting EHDSLens API Server...")
        print(f"   API: http://{args.host}:{args.port}")
        print(f"   Docs: http://{args.host}:{args.port}/docs")
        print(f"   ReDoc: http://{args.host}:{args.port}/redoc\n")

        run_api(host=args.host, port=args.port, reload=args.reload)

    except ImportError:
        print("Error: FastAPI/Uvicorn is not installed.")
        print("Install it with: pip install ehdslens[api]")
        sys.exit(1)


if __name__ == '__main__':
    main()
